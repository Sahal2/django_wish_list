# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt
from django.utils.timezone import now
from datetime import datetime 

class UsersManager(models.Manager):
    def login(self,postData,request):
        "loops through all the users in the database and checks if the username mathces the password and result variable is True if they match"
        reg_username = postData["username"]
        reg_raw_passw = str(postData["passw"])
        user_id = "None"
        for user in self.all():
            if user.username == reg_username:
                if bcrypt.checkpw(reg_raw_passw.encode(), user.passw.encode()):
                    result = True
                    user_id = int(user.id)
                    break
                else:
                    result = False
        if not result:
            messages.add_message(request, messages.WARNING, "Username doesn't exist or password doesn't match")
        return (result, user_id)

    def create_user(self,postData,request):
        "Creates a new user and returns the id of the newly created user"
        new_name = postData['name']
        new_username = postData['username']
        raw_passw = postData['passw']
        new_passw = bcrypt.hashpw(raw_passw.encode(), bcrypt.gensalt())
        new_date =  datetime.strptime(postData['date'], '%Y-%m-%d') #date in unicode so conversion to datetime format of python for data entry
        new_user = self.create(name=new_name,username=new_username,passw=new_passw,date=new_date)
        new_user.save()
        return new_user.id

    def validate(self,postData,request):
        "Validates"
        new_name = postData['name']
        new_username = postData['username']
        passw = postData['passw']
        confirm_passw = postData['confirm_passw']
       
        if passw != confirm_passw:
            messages.add_message(request, messages.INFO, "Passwords do not match")
        if len(passw) < 8:
            messages.add_message(request, messages.INFO, "Password cannot be less than 8 characters")
        if len(new_username) < 3:
            messages.add_message(request, messages.INFO, "Username has to at least 3 characters")
        if len(new_name) < 3:
            messages.add_message(request, messages.INFO, "Name has to be at least 3 characters")
        for user in self.all():
            if new_name == user.name:
                messages.add_message(request, messages.INFO, "Name already exists")
            if new_username == user.username:
                messages.add_message(request, messages.INFO, "Username already exists")
            if new_name == user.passw:
                messages.add_message(request, messages.INFO, "Pasword already exists")
        storage = messages.get_messages(request)
        if storage:
            return False
        else:
            return True

    def update_dictionary(self):
        """
        Creates a dictionary of all the user items that can be accessed via the user.id; 
        Used to pass along info of logged in user to the template in dashboard.html
        """
        users = {}
        for user in self.all():
            users[user.id] = [user.name,user.username]
        return users

class Users(models.Model):
    
    name = models.CharField(max_length=50, default="no name")
    username = models.CharField(max_length=50, default='no username')
    date = models.DateField(default=now)
    passw = models.CharField(max_length=50,default="1234")
    def __repr__(self):
        return "<Users object:{} {} {} {} {}>".format(self.id, self.name, self.username, self.passw, self.date)

    objects = UsersManager()
