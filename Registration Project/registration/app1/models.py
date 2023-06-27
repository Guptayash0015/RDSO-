from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class app1(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    Email = models.CharField(max_length=150)
    Password=models.CharField(max_length=150)
    Password2=models.CharField(max_length=150)
    
    
    def __str__(self) -> str:
        return self.user.username