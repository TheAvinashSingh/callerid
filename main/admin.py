from django.contrib import admin
from .models import ProfileUser, UserContactRelation, Contact

admin.site.register(ProfileUser)
admin.site.register(UserContactRelation)
admin.site.register(Contact)