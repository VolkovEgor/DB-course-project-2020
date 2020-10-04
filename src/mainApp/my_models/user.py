from django.db import models
from ..managers.profile_manager import ProfileManager

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    photo = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, verbose_name = 'Изображение', default='default_photo.png')

    def __str__(self):
        return self.username

    def change_photo(self, image):
        self.photo = image
        self.save()
    

