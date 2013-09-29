import re
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from game.views import GameDemoView, MainView, AboutView, GameView, create_game

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'game.views.home_view', name='home'),
    url("", include("django_socketio.urls")),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^singlegame/$', GameDemoView.as_view()),
    url(r'^game/(?P<game_id>\d+)/$', GameView.as_view()),
    url(r'^about/$', AboutView.as_view()),
    url(r'^mainview/$', MainView.as_view()),
    url(r'^create_game/$', create_game),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')),
        'django.views.static.serve', {'document_root':settings.STATIC_ROOT}),
)

