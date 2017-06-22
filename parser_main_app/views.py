from django.shortcuts import render
from django.views.generic import TemplateView

from .parse_defs import main_parse_process
from .forms import OrderModelForm
from .models import *

from django.core.mail import send_mail

import os
from celery import task

class Index(TemplateView):
    def get(self,request):
        form = OrderModelForm
        return render(request, 'index.html', {'form':form})
    def post(self,request):
        url = request.POST.get('url', '')
        user_mail = request.POST.get('email', '')
        current_order = OrderModel.objects.create(url = url, email=user_mail)
        current_order.save()
        start_parsing(request, url, user_mail, current_order.pk)
        
        return render(request, 'thanks.html', {})

class ShowResult(TemplateView):
    def get(self, request, order_number):
        current_order = OrderModel.objects.get(pk=order_number)
        return render(request, 'show_shedules.html', \
                    {'current_order':current_order})

@task                    
def start_parsing(request, url, user_mail, order_number):
    main_parse_process(url, order_number) #Парсер должен сохранять изображения по нужному адресу с привязкой к модели
    send_notification(request, user_mail, order_number)
        
    
#####   
def send_notification(request, user_mail, order_number):
    mail_host = "oriflamesender@gmail.com" 
    recipients= [user_mail,]
    url_in_letter = 'http://{}/show_result/{}/'.format(request.get_host(),format(str(order_number)))
    message = '''Здравствуйте! Ваш запрос на сайте IRR Parser обработан. Вот ссылка на полученные графики:
    {}'''.format(url_in_letter)
    subject= 'Отчет с IRR Parser'
    
    send_mail(subject, message, mail_host, recipients, fail_silently=False)
