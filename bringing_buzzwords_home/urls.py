from django.conf.urls import include, url
from django.contrib import admin
from visualize import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'state', views.StateViewSet)



urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^state/(?P<state>\D+)$', views.state, name='state'),
    url(r'^json/(?P<state>\D+)$', views.state_json, name='state_json'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^county/(?P<county>\d+)$', views.county, name='county'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls))]

urlpatterns += staticfiles_urlpatterns()
