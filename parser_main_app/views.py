from django.shortcuts import render
from django.views.generic import TemplateView

from .parse_defs import main_parse_process
from .forms import OrderModelForm
from .models import *

from django.core.mail import send_mail

import os
from celery import task, shared_task
import json

class Index(TemplateView):
    def get(self,request):
        form = OrderModelForm
        return render(request, 'index.html', {'form':form})
    def post(self,request):
        url = request.POST.get('url')
        user_mail = request.POST.get('email')
        current_order = OrderModel.objects.create(url = url, email=user_mail)
        current_order.save()
        post_dict = request.POST.copy()
        post_dict['order_number'] = current_order.pk
        post_dict['host_name'] = request.get_host()
        json_data = json.dumps(post_dict)

        start_parsing.delay(json_data)

        return render(request, 'thanks.html', {})


@task               
def start_parsing(data):
    normal_data = json.loads(data)
    url = normal_data.get('url')
    email = normal_data.get('email')
    current_order_pk = normal_data.get('order_number')
    host_name = normal_data.get('host_name')
    main_parse_process(url, current_order_pk) #Парсер должен сохранять изображения по нужному адресу с привязкой к объекту отчета
    send_notification(email, current_order_pk, host_name)
        
      
def send_notification(user_mail, order_number, host_name):
    mail_host = "oriflamesender@gmail.com" 
    recipients= [user_mail,]
    url_in_letter = 'http://{}/show_result/{}/'.format(host_name, str(order_number))
    message = '''Здравствуйте! Ваш запрос на сайте IRR Parser обработан. Вот ссылка на полученные графики:
    {}'''.format(url_in_letter)
    subject= 'Отчет с IRR Parser'
    
    send_mail(subject, message, mail_host, recipients, fail_silently=False)


class ShowResult(TemplateView):
    def get(self, request, order_number):
        current_order = OrderModel.objects.get(pk=order_number)
        return render(request, 'show_shedules.html', \
                    {'current_order':current_order})