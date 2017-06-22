from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$', views.Index.as_view(), name='Index'),
    url(r'^show_result/(?P<order_number>[0-9]+)/$', views.ShowResult.as_view(), name='ShowResult'),
]
