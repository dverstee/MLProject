from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
	url(r'^predictor/', include('lolpredictor.predictor.urls', namespace='predictor')),
    url(r'^admin/', include(admin.site.urls)),
)
