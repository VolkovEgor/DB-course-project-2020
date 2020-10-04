from django.db import models
from .word import Word
from .user import User


class UserWordStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status')
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='status')
    is_learned = models.BooleanField(default=False)
    errors_number = models.PositiveIntegerField(default=0)

    def change_status(self, new_status):
        self.is_learned = new_status
        self.save()
    
    def change_errors_number(self):
        self.errors_number += 1
        self.save()
