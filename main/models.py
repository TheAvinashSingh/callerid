from django.db import models
from django.contrib.auth.models import User

class ProfileUser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
	phone = models.CharField(max_length=10,null=False, unique=True)
	spam = models.BooleanField(default=False)

	def __str__(self):
		return self.user

class Contact(models.Model):
	name = models.CharField(max_length=50, null=False)
	email = models.EmailField(max_length=50, null=False)
	phone = models.CharField(max_length=10, null=False)
	spam = models.BooleanField(default=False)

	def __str__(self):
		return self.name

class UserContactRelation(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
	contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=False)

	def __str__(self):
		return str(self.user) + ' | ' + str(self.contact)