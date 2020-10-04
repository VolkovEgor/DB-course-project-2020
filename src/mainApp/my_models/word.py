from django.db import models
from .rating import RelativeRating
from ..managers.word_manager import WordManager

class Word(models.Model):
    title = models.CharField(max_length=50)
    transcription = models.CharField(max_length=50)
    translation = models.CharField(max_length=60)

    views_number = models.PositiveIntegerField(default=0)
    additions_number = models.PositiveIntegerField(default=0)
    relative_rating = models.OneToOneField(RelativeRating, on_delete=models.CASCADE, related_name='word')

    objects = models.Manager()
    own = WordManager()
 
    def __str__(self):
        return '[pk={}] {}'.format(self.pk, self.title)

    def inc_views_number(self):
        self.views_number += 1
        self.save()

    def inc_additions_number(self):
        self.additions_number += 1
        self.save()    
    
    def rating_update(self, total_ans_num, correct_ans_num):
        self.relative_rating.value_update(total_ans_num, correct_ans_num)
