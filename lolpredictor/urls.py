from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lolpredictor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^LeaguePredictor/', include('lolpredictor.LeaguePredictor.url', namespace='LeaguePredictor')),
    url(r'^admin/', include(admin.site.urls)),
)
