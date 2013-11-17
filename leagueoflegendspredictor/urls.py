from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'leagueoflegendspredictor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
	url(r'^LeaguePredictor/', include('LeaguePredictor.url', namespace="LeaguePredictor")),
    url(r'^admin/', include(admin.site.urls)),
)
