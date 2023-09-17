from django.shortcuts import render, get_object_or_404
from .tg_client import TelegramClient
from rest_framework import viewsets, mixins, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework import generics
from adrf.decorators import api_view
from asgiref.sync import async_to_sync, sync_to_async
from .models import Employee, Chat, ChatTag
from .serializers import *
import asyncio
from django.db.models.functions import Lower

class ChatViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Chat.objects.all()
        serializer = ChatSerializer(queryset, many=True)
        return Response(serializer.data)
    def destroy(self, request, pk=None):
        chat = Chat.objects.get(pk=pk)
        self.remove_chat(chat.chat_id)
        chat.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    @async_to_sync
    async def remove_chat(self, id):
            client = TelegramClient()
            await client.delete_chat(id)
            
    def retrieve(self, request, pk=None):
        queryset = Chat.objects.all()
        chat = get_object_or_404(queryset, pk=pk)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)
class EmployeeViewSet(viewsets.ModelViewSet ):
    queryset = Employee.objects.all()
    def get_serializer_class(self):
        if self.action=='list':
            return EmployeesListSerializer
        if self.action=='retrieve':
            return EmployeesRetrieveSerializer
        return EmployeesCreateSerializer
        
    def destroy(self, request, *args, **kwargs):
        instanse = self.get_object()
        ids = list(map(lambda chat:chat.chat_id, instanse.chats.all()))
        for id in ids:
            print(id)
        print(instanse.tg_username)
        self.remove_from_all_chats(ids, instanse.tg_username.lower())
        self.perform_destroy(instanse)
        return Response(status=HTTP_204_NO_CONTENT)
    @async_to_sync
    async def remove_from_all_chats(self, ids, tg_username):
        client = TelegramClient()
        for chat in ids:
            await client.remove_from_group(chat, [tg_username])        
class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer





@api_view(['POST'])
async def create_chat_sync(request):
    if request.method == 'POST':
        client = TelegramClient()
        title = request.data['title']
        id, link, owner = await client.create_chat(title)
        
        
        chat = await sync_to_async(Chat.objects.create)(chat_id=id, name=title, number_emp=0, tg_link=link, owner=owner)
        pk = await sync_to_async(chat.get_pk)()
        return Response({'Status': 'Succsess'})


@api_view(['POST'])
async def add_users_view(request, id):
    client = TelegramClient()
    tg_usernames = []
    chat = await sync_to_async(Chat.objects.get)(pk=id)
    for user_id in request.data['users']:
        employee = await sync_to_async(Employee.objects.get)(pk=user_id)
        await sync_to_async(employee.chats.add)(chat)
        await sync_to_async(employee.save)()
        tg_usernames.append(employee.tg_username)
    if request.method == 'POST':
        await client.add_to_group(chat.chat_id, tg_usernames)
        return Response({'Status': 'Succsess'})

@async_to_sync
async def remove_users(id, users):
    client = TelegramClient()
    await client.remove_from_group(id, users)
@async_to_sync
async def get_usernames_from_chat(id):
    client = TelegramClient()
    usernames = await client.get_chat_usernames(id)
    return [username.lower() for username in usernames]
@api_view(['GET'])
def get_users_from_chat(request, id):
    chat = Chat.objects.get(pk=id)
    usernames = get_usernames_from_chat(chat.chat_id)
    lower_tg_employees = Employee.objects.annotate(tg_username_lower=
    Lower('tg_username'))
    employees = lower_tg_employees.filter(tg_username_lower__in=usernames)
    print(type(employees))
    return Response(EmployeesRetrieveSerializer(employees, many=True).data)
@api_view(['POST'])
def remove_users_view(request, id):
    usernames = []
    chat = Chat.objects.get(pk=id)
    for user in request.data['users']:
        employee = Employee.objects.get(pk=user)
        employee.chats.remove(chat)
        usernames.append(employee.tg_username)
    remove_users(chat.chat_id, usernames)
    return Response({'Status': 'Succsess'})