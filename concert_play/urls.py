from django.conf.urls import url
from django.contrib import admin
import concert_core.views as views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^get_concerts/$', views.get_concerts, name='get_concerts'),
    url(r'^create_playlist/$', views.create_playlist, name='create_playlist'),
]
