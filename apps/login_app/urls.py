from django.conf.urls import url
from . import views

urlpatterns =[
    url(r'^$', views.index),
    url(r'^success$', views.success),
    url(r'^add$', views.add),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^process$', views.process),
    url(r'^users/(?P<userId>\d+)/$', views.users)
]
