from django.db import models
from datetime import datetime as dtt
# Create your models here.


class OrderModel(models.Model):
    class Meta:
        verbose_name = 'Заявка на парсинг'
        verbose_name_plural = 'Заявки на парсинг'

    url = models.URLField('Ссылка на раздел')
    email = models.EmailField('Электронная почта')
    week_shedule = models.ImageField(null=True,
                                     blank=True,
                                     upload_to='images/orders/shedules{}'.format(str(dtt.now().year) +
                                                                                 str(dtt.now().month) +
                                                                                 str(dtt.now().day) +
                                                                                 str(dtt.now().hour) +
                                                                                 str(dtt.now().minute)))
    hour_shedule = models.ImageField(null=True,
                                     blank=True,
                                     upload_to='images/orders/shedules{}'.format(str(dtt.now().year) +
                                                                                 str(dtt.now().month) +
                                                                                 str(dtt.now().day) +
                                                                                 str(dtt.now().hour) +
                                                                                 str(dtt.now().minute)))

    def __str__(self):
        return self.email + ' ---- ' + self.url
