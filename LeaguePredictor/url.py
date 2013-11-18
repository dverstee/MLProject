from django.conf.urls import patterns, url

from LeaguePredictor import views

urlpatterns = patterns('',

    url(r'^$', views.index, name='index'),
 	url(r'^neural/$', views.neural, name='neural'),

)