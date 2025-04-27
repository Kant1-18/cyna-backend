from django.contrib import admin
from users.src.data.models.User import User
from users.src.data.models.UserCredential import UserCredential
from users.src.data.models.Address import Address

admin.site.register(User)
admin.site.register(UserCredential)
admin.site.register(Address)
