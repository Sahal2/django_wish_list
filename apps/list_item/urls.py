from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^(?P<id>\d+)$', views.show_item,name="show_item"),
    url(r'^create$', views.add_items,name="add_items"),
    url(r'^create/process$', views.add_items_process,name="add_items_process"),
    url(r'^(?P<item_id>\d+)/add$',views.add_to_list,name="add_to_list"),
    url(r'^(?P<rem_item_id>\d+)/remove_from_list$', views.remove_from_list,name="remove_from_list" ),
    url(r'^(?P<delete_item_id>\d+)/delete$', views.delete, name="delete")
]