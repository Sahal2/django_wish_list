from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name="main"),
    url(r'^dashboard$', views.dashboard, name="dashboard"),
    url(r'^login_process$', views.user_login_process, name="login"),
    url(r'^register_process$', views.user_register_process, name="register"),
    url(r'^logout_process$', views.user_logout_process, name="logout"),
]