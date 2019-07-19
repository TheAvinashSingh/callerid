from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserContactRelation, ProfileUser, Contact


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = '__all__'


class UserContactRelationSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserContactRelation
		fields = '__all__'


class ProfileUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProfileUser
		fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contact
		fields = '__all__'
