from django.conf.urls import url
from tweet import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
