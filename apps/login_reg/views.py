# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.core.urlresolvers import reverse
from ..list_item.models import *

def index(request):
    request.session["logged_in"] = False
    return render(request, "login_reg/index.html")

def user_register_process(request):
    if Users.objects.validate(request.POST,request):
        Users.objects.create_user(request.POST,request)
        return redirect(reverse("main"))
    else: 
        print "Failed"
        return redirect(reverse("main"))

def user_login_process(request):
    passw_match, user_id = Users.objects.login(request.POST,request)
    print passw_match, user_id
    if passw_match:
        request.session["user_id"] = user_id
        request.session["logged_in"] = True
        return redirect(reverse("dashboard"))
    else:
        print "Failed"
        return redirect(reverse("main"))
    
def user_logout_process(request):
    request.session.flush()
    return redirect(reverse("main"))


def dashboard(request):
    try:
        if request.session["logged_in"]:
            user_id = request.session["user_id"]
            items = Lists.objects.get_items(user_id)
            users = Users.objects.update_dictionary()
            requested_user = users[user_id]
            other_users = Items.objects.other_users(user_id)
            return render(request, "login_reg/dashboard.html",{"items":items,"users":requested_user,"other_users":other_users})
        else:
            return redirect("main")
    except KeyError:
       return redirect(reverse("main"))