from django.conf.urls import include, url
from django.contrib import admin
from visualize import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^state/(?P<state>\D+)$', views.state, name='state'),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += staticfiles_urlpatterns()
