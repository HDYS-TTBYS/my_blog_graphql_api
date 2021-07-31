from django.contrib import admin
from .models import CustomUser
from graphql_auth.models import UserStatus

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserStatus)
