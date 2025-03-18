from django.db import models
from users.src.data.models.User import User


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.IntegerField(default=0, blank=False, null=False)
    street = models.CharField(max_length=100, blank=False, null=False)
    number = models.CharField(max_length=10, blank=False, null=False)
    complement = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=10, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    region = models.CharField(max_length=2, blank=False, null=False)
    country = models.CharField(max_length=2, blank=False, null=False)
    
    def to_json(self):
        return {
            "userId": self.user.id,
            "type": self.type,
            "street": self.street,
            "number": self.number,
            "complement": self.complement,
            "zip_code": self.zip_code,
            "city": self.city,
            "region": self.region,
            "country": self.country
        }
