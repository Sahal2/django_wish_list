# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import *
from ..login_reg.models import *
from django.core.urlresolvers import reverse
    
def add_items(request):
    return render(request, "login_reg/new_item.html")

def add_items_process(request):
    item_name = request.POST["item_name"]
    user_id = int(request.session['user_id'])
    user_object = Users.objects.get(id=user_id)
    list_object = Lists.objects.get(user=user_object)
    if Items.objects.validate(item_name):
        Items.objects.create_item(item_name,list_object,user_object)
        return redirect(reverse("dashboard"))
    else:
        redirect("add_item")

def show_item(request,id):
    item_id = int(id)
    request.session['item_name'] = str(Items.objects.get(id=item_id).name)
    users = Items.objects.get_users_by_item(item_id)
    return render(request,"login_reg/show_item.html",{"users":users})
    
def remove_from_list(request,rem_item_id):
    user_id = int(request.session["user_id"])
    Items.objects.remove_list(add_item_id,user_id)
    return redirect(reverse("dashboard"))

def add_to_list(request,item_id):
    user_id = int(request.session["user_id"])
    add_item_id = Items.objects.add_list(item_id,user_id)
    return redirect(reverse("dashboard"))

def delete(request,delete_item_id):
    item_id = delete_item_id
    Items.objects.delete(item_id)
    return redirect(reverse("dashboard"))