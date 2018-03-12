from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.root, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^auth/$', views.page_auth, name='page_auth'),
    url(r'^add_post/$', views.add_post, name='add_post'),
    url(r'^logout/$', views.logout, name='page_register'),
    url(r'^register/$', views.page_register, name='page_register'),
    url(r'^edit_post/(?P<pk>\d+)/$', views.edit_post, name='edit_post'),
    url(r'^profile/(?P<pk>\d+)/$', views.page_profile, name='page_profile'),
]
