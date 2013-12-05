from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
 	url(r'^neural/$', views.neural, name='neural'),
 	url(r'^crawlstats/$', views.crawlstats, name='crawlstats'),
 	url(r'^crawler/$', views.crawler, name='crawler'),
 	url(r'^summoners/$', views.summoners, name='summoners'),
    url(r'^search/', views.search, name='search'),
    url(r'^test/', views.test, name='test'),
)