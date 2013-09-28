from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from game.views import GameDemoView, MainView 


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'game.views.home_view', name='home'),
    # url(r'^memo/', include('memo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^gameuidemo/$', GameDemoView.as_view()),
    url(r'^mainview/$', MainView.as_view()),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

