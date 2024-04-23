from rest_framework import serializers
from .models import UserEnrolled,Asset,Exit,Site,Notification,Upload_File

class UserEnrolledSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        fields = '__all__'


class ActionStatusSerializer(serializers.Serializer):
    status = serializers.IntegerField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

class UserEnrolledSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        fields = ['name','company_name','job_role','mycompany_id','tag_id','job_location','orientation','status']
       

class ExitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exit
        fields = '__all__'

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ['id', 'name']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['subject', 'description', 'username']

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload_File
        fields = '__all__'