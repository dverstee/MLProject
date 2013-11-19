from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lolpredictor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', direct_to_template, {'template': 'home.html'}),
	url(r'^predictor/', include('lolpredictor.predictor.url', namespace='predictor')),
    url(r'^admin/', include(admin.site.urls)),

)
