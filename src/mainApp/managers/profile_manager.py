from django.db import models
from django.contrib.auth.models import User

class ProfileManager(models.Manager):
    def  get_profile_id_by_user_id(self, user_id):
        return self.get(user=user_id) 

