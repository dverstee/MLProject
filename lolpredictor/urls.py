from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^', include('lolpredictor.predictor.url', namespace='predictor')),
    url(r'^admin/', include(admin.site.urls)),

)
