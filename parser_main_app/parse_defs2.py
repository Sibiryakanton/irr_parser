import requests
import os
import datetime
from matplotlib import pyplot as plt
from datetime import datetime as dtt
from bs4 import BeautifulSoup
from irr_parser.settings import MEDIA_ROOT  # Для сохранения графиков с остальными медиафайлами
from .models import *

class IrrParser():
    def __init__(self, url, order_number):
        self.url = url
        self.order_number = order_number

    def main_parse_process(self):

        self.url_for_filename = self.url.replace('/', '').replace(':', '')
        self.filename = 'output-{0}.txt'.format(self.url_for_filename)
        self.count_ads_per_hour = {}  # Кол-во объявлений на каждый час сегодняшнего дня.
        self.count_ads_per_day = {}  # Кол-во объявлений на каждый день.

        self.parse()

        # Для страниц от второй и далее в конце ссылки используется конструкция ?page[n]. вместо n будет number
        number = 2

        while True and number < 6:
            # Собираем url, получаем из него содержимое для передачи в парсер
            self.url = self.url + 'page{0}'.format(number)
            response = requests.get(url)
            if response.url == self.url or number > 2:
                break
            parse(self)
            number += 1
            print(self.url)

        self.build_shedules()

    def get_html(self):  # Получение кода страницы.
        response = requests.get(self.url)
        return response.text

    def parse(self):  # Извлечение строк с указанием времени публикации объявлений.
        soup = BeautifulSoup(self.get_html(), 'lxml')
        table = soup.find_all('div', class_='updateProduct')

        # собираем дату публикации в найденных div-контейнерах. Если не указана, значит, текст опубликован сегодня
        for elem in table:
            self.ads_span = elem.find('span')
            if self.ads_span is not None:
                self.ads_span = elem.find('span').text
            else:
                self.ads_span = 'Today'

            filter_soup = BeautifulSoup(str(elem), 'lxml')
            span_extract = filter_soup.find_all('span')
            for span in span_extract:
                span.extract()
            self.time_string = filter_soup.find('div').text.strip()

            if 'сегодня' in self.time_string:
                self.today_activity_analyze()
            self.date_activity_analyze()

    def today_activity_analyze(self):
        string = self.ads_span
        current_time = string.split(', ')[1].split(':')  # Отделяем часы от минут и слова "сегодня".
        if self.count_ads_per_hour.get(int(current_time[0])):
            self.count_ads_per_hour[int(current_time[0])] += 1
        else:
            self.count_ads_per_hour[int(current_time[0])] = 1

    def date_activity_analyze(self):
        # Форматируем строку в словарь, собираем из нее строку,
        # удобную для модули даты и времени, а затем выясняем,
        # на какой день недели выпадает число, и пополняем счетчик где надо.
        if self.ads_span == 'Today':
            ads_formatted_date = dtt.today()
        else:
            ads_date_string = self.ads_span.split(' ')
            months = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июня': 6,
                      'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12}
            ads_date = [ads_date_string[1], ads_date_string[2]]
            # Получаем номер месяца
            ads_month = months.get(ads_date[1])
            if len(ads_date_string) == 4:
                ads_year = int(ads_date_string[3])
            else:
                # В объявлении не указывается год публикации, так что за основу возьмем текущий.
                ads_year = dtt.today().year
            ads_formatted_date = datetime.date(ads_year, ads_month, int(ads_date[0]))

        week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        ads_weekday = ads_formatted_date.weekday()

        if self.count_ads_per_day.get(week[ads_weekday]):
            self.count_ads_per_day[week[ads_weekday]] += 1
        else:
            self.count_ads_per_day[week[ads_weekday]] = 1


    def build_shedules(self):
        # Часть имени директории с датой и временем
        part_dirname = str(dtt.now().year) + str(dtt.now().month) + str(dtt.now().day) +\
                       str(dtt.now().hour) + str(dtt.now().minute)

        path_for_images = os.path.join(MEDIA_ROOT, 'images', 'orders', 'shedules{}'.format(part_dirname))
        if os.path.exists(path_for_images) is False:
            os.makedirs(path_for_images)  # Создаем папку для графиков

        self.week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

        sorted_ads_count = []
        for day in week:
            ads_day_count = self.count_ads_per_day.get(day)
            sorted_ads_count.append(ads_day_count)
        self.create_image('День недели', sorted_ads_count)


        sorted_hour_activity = []
        for i in range(24):
            ads_hour_count = self.count_ads_per_hour.get(i)
            if ads_hour_count is None:
                ads_hour_count = 0

            sorted_hour_activity.append(ads_hour_count)
        self.create_image('Час', sorted_hour_activity)


        # Привяжем полученные графики к моделям объектов с помощью имен путей
        current_order = OrderModel.objects.get(pk=int(self.order_number))
        current_order.week_shedule.name = os.path.join('images/orders/shedules{}/{}-week_activity.png'.format
                                                       (part_dirname, self.url_for_filename))
        current_order.hour_shedule.name = os.path.join('images/orders/shedules{}/{}-hour_activity.png'.format
                                                       (part_dirname, self.url_for_filename))
        current_order.save()


    def create_image(self, xlabel_text, datalist):
        fig = plt.figure()

        plt.plot(datalist)
        plt.xlabel(xlabel_text)
        plt.xticks(range(7), self.week)
        plt.ylabel("Кол-во объявлений")
        path_week_shedule = os.path.join(path_for_images, '{}-week_activity.png'.format(self.url_for_filename))
        plt.savefig(path_week_shedule, fmt='png')

        # Собрали и сохранили график суточной активности
        plt.close(fig)