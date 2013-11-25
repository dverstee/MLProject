from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
 	url(r'^neural/$', views.neural, name='neural'),
 	url(r'^crawler/$', views.crawler, name='crawler'),
    url(r'^search/', views.search, name='search'),
 	
)