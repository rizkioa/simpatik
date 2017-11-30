from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^option-kbli/$', views.option_kbli, name='option_kbli')

]