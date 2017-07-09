import requests
import os
import datetime
from matplotlib import pyplot as plt
from datetime import datetime as dtt
from bs4 import BeautifulSoup
from irr_parser.settings import MEDIA_ROOT #Для сохранения графиков с остальными медиафайлами


from .models import *

def main_parse_process(url, order_number):
    url_for_filename = url.replace('/','').replace(':','')
    filename = 'output-{0}.txt'.format(url_for_filename)
    
    count_ads_per_hour = {} #Создаем словарь, в котором будем хранить кол-во объявлений на каждый час.
    count_ads_per_day = {} #Словарь для кол-ва объявления на каждый день.
    parse(get_html(url), filename, count_ads_per_hour, count_ads_per_day) 
    number = 2
    root_url = url
    print(url)
    while True:
        url = root_url + 'page{0}'.format(number)
        response = requests.get(url)
        if response.url == root_url or number>2:
            print('Проверка завершена!')
            break
        parse(get_html(url), filename, count_ads_per_hour, count_ads_per_day) 
        
        number+=1
        print(url)
    
    
    build_shedules(count_ads_per_day, count_ads_per_hour, url_for_filename, order_number)
    
def get_html(url): #Получение кода страницы.
    response = requests.get(url)
    return response.text

    
def parse(html, filename, count_ads_per_hour, count_ads_per_day): #Извлечение строк с указанием времени публикации объявлений.
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('div', class_='updateProduct')

    for elem in table:
        ads_span = elem.find('span')
        if ads_span!=None:
            ads_span = elem.find('span').text
        else:
            ads_span = 'Today'
            
        filter_soup = BeautifulSoup(str(elem), 'lxml')
        span_extract = filter_soup.find_all('span')
        for span in span_extract:
           span.extract()
           
        time_string= filter_soup.find('div').text.strip()
            
        if 'сегодня' in time_string:
            today_activity_analyze(time_string, count_ads_per_hour, count_ads_per_day)
        date_activity_analyze(ads_span, count_ads_per_day)


def today_activity_analyze(string, count_ads_per_hour, count_ads_per_day):
    current_time = string.split(', ')[1].split(':') #Отделяем часы от минут и слова "сегодня".
    if count_ads_per_hour.get(int(current_time[0])):
        count_ads_per_hour[int(current_time[0])] += 1
    else:
        count_ads_per_hour[int(current_time[0])] = 1
   
def date_activity_analyze(string, count_ads_per_day): #Форматируем строку в словарь, собираем из нее строку, 
    #удобную для модули даты и времени, а затем выясняем, на какой день недели выпадает число, и пополняем счетчик где надо.
    if string=='Today':
        ads_formatted_date = dtt.today()
    else:
        ads_date_string = string.split(' ')
        months = {'января':1, 'февраля':2, 'марта':3, 'апреля':4, 'мая':5, 'июня':6, 'июля':7, 'августа':8, 'сентября':9,\
                    'октября':10, 'ноября':11, 'декабря':12}
        ads_date = [ads_date_string[1], ads_date_string[2]]
        ads_month = months.get(ads_date[1]) #Получаем номер месяца
        if len(ads_date_string)==4:
            ads_year = int(ads_date_string[3])
        else:
            ads_year = dtt.today().year #В объявлении не указывается год публикации, так что за основу возьмем текущий.
        ads_formatted_date = datetime.date(ads_year,ads_month,int(ads_date[0]))
    
    week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    ads_weekday = ads_formatted_date.weekday()
    
    if count_ads_per_day.get(week[ads_weekday]):
        count_ads_per_day[week[ads_weekday]] += 1
    else:
        count_ads_per_day[week[ads_weekday]] = 1

def build_shedules(count_ads_per_day, count_ads_per_hour, url_for_filename, order_number):
    part_dirname = str(dtt.now().year) + str(dtt.now().month) + str(dtt.now().day) +\
                    str(dtt.now().hour) + str(dtt.now().minute)
                    #Часть имени директории с датой и временем
    path_for_images = os.path.join(MEDIA_ROOT,'images','orders','shedules{}'.format(part_dirname))
    if os.path.exists(path_for_images)==False:
        os.makedirs(path_for_images) #Создаем папку для графиков
    
    week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    sorted_ads_count = []
    for day in week:
        ads_day_count = count_ads_per_day.get(day)
        sorted_ads_count.append(ads_day_count)    
    fig = plt.figure()
    plt.xlabel('День недели')
    plt.ylabel('Количество объявлений')
    plt.plot(sorted_ads_count)
    plt.xticks(range(7), week)
    path_week_shedule = os.path.join(path_for_images,'{}-week_activity.png'.format(url_for_filename))
    plt.savefig(path_week_shedule, fmt='png') #Собрали и сохранили график суточной активности
    plt.close(fig)
    
    fig = plt.figure()
    sorted_hour_activity = []
    for i in range(24):
        ads_hour_count = count_ads_per_hour.get(i)
        if ads_hour_count ==None:
            ads_hour_count = 0
        
        sorted_hour_activity.append(ads_hour_count)
        
    plt.plot(sorted_hour_activity)
    plt.xticks(range(24))
    plt.xlabel('Час')
    plt.ylabel('Количество объявлений')
    path_hour_shedule = os.path.join(path_for_images,'{}-hour_activity.png'.format(url_for_filename))
    plt.savefig(path_hour_shedule, fmt='png')#Собрали и сохранили график недельной активности
    
    #Привяжем полученные графики к моделям объектов с помощью имен путей
    current_order = OrderModel.objects.get(pk=int(order_number))
    current_order.week_shedule.name = os.path.join('images/orders/shedules{}/{}-week_activity.png'.format \
                                                (part_dirname,url_for_filename))
    current_order.hour_shedule.name = os.path.join('images/orders/shedules{}/{}-hour_activity.png'.format \
                                                (part_dirname,url_for_filename))
    current_order.save()
    plt.close(fig)
    