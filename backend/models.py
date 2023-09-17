# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
class Banword(models.Model):
    name = models.CharField(max_length=50)
class Opportunities(models.Model):
    name = models.CharField(max_length=30)

    
class Tag(models.Model):
    name = models.CharField(blank=True, null=True)
class ChatTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
class Chat(models.Model):
    chat_id = models.CharField(max_length=30, default=None)
    name = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)
    censor = models.BooleanField(default=True)
    number_emp = models.IntegerField()
    tg_link = models.CharField(max_length=30)
    tags = models.ManyToManyField(ChatTag, null=True)
    def get_id(self):
        return self.chat_id
    def get_pk(self):
        return self.pk

   


class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, null=True)
    chats = models.ManyToManyField(Chat, null=True)
    tags = models.ManyToManyField(Tag, null=True)
    tg_username = models.CharField(max_length=30, blank=True)
    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'
    def get_username(self):
        return self.user.get_username() if self.user!=None else "null"
    def get_ids(self):
            ids = []
            for chat in self.chats.all():
                ids.append(chat.get_id())
            return ids
    


class Message(models.Model):
    employee = models.ForeignKey(Employee, models.DO_NOTHING, blank=True, null=True)
    data_time = models.DateTimeField()
    text = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=30)
    chat = models.ForeignKey(Chat, models.DO_NOTHING, blank=True, null=True)
    pinned = models.BooleanField(blank=True, null=True)


class File(models.Model):
    message = models.ForeignKey(Message, models.DO_NOTHING, blank=True, null=True)
    body = models.CharField()
    format = models.CharField(max_length=30)


class Ban(models.Model):
    chat = models.ForeignKey(Chat, models.DO_NOTHING)
    employee = models.ForeignKey(Employee, models.DO_NOTHING)
    ban_period = models.DateTimeField(blank=True, null=True)
    opportunities = models.ForeignKey(Opportunities, models.DO_NOTHING)
    banword = models.ForeignKey(Banword, models.DO_NOTHING, blank=True, null=True)
    mеssage = models.ForeignKey(Message, models.DO_NOTHING, blank=True, null=True)
