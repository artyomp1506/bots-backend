from .models import Employee, Tag, Chat
from rest_framework import serializers
class TagsSerializer(serializers.ModelSerializer):
        class Meta:
            model = Tag
            fields = '__all__'
class ChatSerializerForEmployee(serializers.ModelSerializer):
        
         class Meta:
            model = Chat
            fields = ('chat_id',)
class ChatSerializer(serializers.ModelSerializer):
        class Meta:
            model = Chat
            fields = '__all__'
            
class EmployeesListSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    full_name = serializers.CharField(source = 'get_full_name')
    username = serializers.CharField(source = 'get_username')
    ids = serializers.ListField(source = 'get_ids')


    class Meta:
        model = Employee
        fields = ('id', 'full_name', 'username', 'tg_username', 'tags', 'ids')
        depth = 1
class EmployeesRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
    tags = TagsSerializer(many=True)
class EmployeesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
class ChatEmployeesSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source = 'get_full_name')
    tags = TagsSerializer(many=True)
    class Meta:
        model = Employee
        fields = '__all__'