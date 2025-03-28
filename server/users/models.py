from django.contrib import admin
from users.src.data.models.User import User
from users.src.data.models.UserCredential import UserCredential
from users.src.data.models.Address import Address
from users.src.data.models.PaymentMethod import PaymentMethod

admin.site.register(User)
admin.site.register(UserCredential)
admin.site.register(Address)
admin.site.register(PaymentMethod)
