from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Person(models.Model):
    
    class GenderType(models.TextChoices):
        MALE = 'male'
        FEMALE = 'female'
        OTHERS = 'others'
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    gender = models.CharField(choices=GenderType, default=GenderType.MALE, max_length=50)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Detail'
        verbose_name_plural = 'User Details'
        
    def __str__(self) -> str:
        return f'{self.user.get_full_name()} - {self.gender}'