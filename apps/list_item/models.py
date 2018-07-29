# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib import messages
from ..login_reg.models import *
from django.utils.timezone import now

class ListsManager(models.Manager):
    def get_items(self,user_id):
        "Gets all the items for the specific user; used in dashboard.html to display logged in user's wishlist"
        user_object = Users.objects.get(id=user_id)
        lists_object = self.get(user=user_object)
        items = {}
        for item in lists_object.items.all():
            items[item.id] = [item.name,item.adder.name,item.created_at,item.id]
        return items


class ItemsManager(models.Manager):
    reviews = {}
    def validate(self,posted_name,):
        "Validates the item to be created"
        new_name = posted_name
        if len(new_name) < 1:
            messages.add_message(request, messages.WARNING, "Product/Item name cannot be empty")
            return False
        if len(new_name) < 3:
            messages.add_message(request, messages.WARNING, "Product/Item name has to be more than 3 characters")
            return False
        return True

    def create_item(self,posted_name,lists_object,user_object):
        "Creates the Item"
        new_adder = user_object
        new_list = lists_object
        new_name = posted_name
        new_item = self.create(name=new_name,adder=new_adder)
        new_item.lists.add(lists_object)
        new_item.save()
        return new_item.id

    def other_users(self,user_id):
        """
        Returns all the items from lists other than the list of the current user
        """
        user_object = Users.objects.get(id=int(user_id))
        list_object = Lists.objects.get(user=user_object)
        items_list = []
        i = 0
        for item in self.all().order_by("created_at"):
            """
            Outter loop: runs through all the items in the order they were created
            Inner loop: runs trhough all the lists that item is associated with
            Inner if: if the any of the lists the current item is associated with 
            is the current logged in users wishlist then the result variable is false
            Outter if: If the result variable is false then do not add the current item to the dictionary
            """
            result = True
            for listy in item.lists.all():
                if listy == list_object:
                    result = False
            if result:
                items_list.append([item.name,item.created_at,item.adder.username,item.id,item.adder.id])
        return items_list
    
    def get_users_by_item(self,item_id):
        """
        Gets the user information for given item; used in show_item.html to present the number of users that the item has been added 
        to their list by
        """
        items = []
        for lists in self.get(id=item_id).lists.all():
            items.append(lists.user.username)
        return set(items)

    def remove_list(self,item_id,user_id):
        "Removes the given list from being associated with the item"
        user_object = Users.objects.get(id=int(user_id))
        lists_object = Lists.objects.get(user=user_object)
        remove_from = self.get(id=item_id)
        remove_from.lists.remove(lists_object)
        return item_id
    
    def add_list(self,item_id,user_id):
        "Adds the given list to an item"
        user_object = Users.objects.get(id=user_id)
        list_object = Lists.objects.get(user=user_object)
        add_to = self.get(id=item_id)
        add_to.lists.add(list_object)
        return item_id
    
    def delete(self,item_id):
        "deletes an item"
        to_delete = self.get(id=item_id)
        to_delete.delete()
        return 


class Lists(models.Model):
    user = models.OneToOneField(Users,on_delete=models.CASCADE,primary_key=True,)
    created_at = models.DateField(default=now)
    def __repr__(self):
        return "<Lists object:{} {}>".format(self.user.name, self.created_at)

    objects = ListsManager()

class Items(models.Model):
    name = models.CharField(max_length=50)
    adder = models.ForeignKey(Users, related_name="items")
    lists = models.ManyToManyField(Lists, related_name="items")
    created_at = models.DateField(default=now)
    def __repr__(self):
        return "<Items object:{} {} {} {} {}>".format(self.id, self.name, self.adder.name, self.lists, self.created_at)
    
    objects = ItemsManager()