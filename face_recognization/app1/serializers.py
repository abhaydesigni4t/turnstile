from rest_framework import serializers
from .models import UserEnrolled

class UserEnrolledSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEnrolled
        fields = '__all__'





