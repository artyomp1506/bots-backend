from rest_framework import routers
from .views import *
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
router = routers.SimpleRouter()
router.register(r'employees', EmployeeViewSet, basename='employees')
router.register(r'chats', ChatViewSet, basename='chats')
router.register(r'tags', TagsViewSet, basename='tags')

urlpatterns = router.urls
urlpatterns+= [
    path('chat/create/',  csrf_exempt(create_chat_sync)),
path('chat/add/<str:id>', csrf_exempt(add_users_view)),
path('chat/remove/<str:id>', csrf_exempt(remove_users_view)),
path('chat/users/<str:id>', csrf_exempt(get_users_from_chat)),


]