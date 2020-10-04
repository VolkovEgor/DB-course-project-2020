from django.db import models
from .rating import RelativeRating
from .user import User
from .word import Word

class UserStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_statistics', default=None)

    viewed_words_number = models.PositiveIntegerField(default=0)
    added_words_number = models.PositiveIntegerField(default=0)

    ended_exercise_number = models.PositiveIntegerField(default=0)
    relative_rating = models.OneToOneField(RelativeRating, on_delete=models.CASCADE, related_name='statistics', default='')

    def inc_viewed_words_number(self):
        self.viewed_words_number += 1
        self.save()

    def inc_added_words_number(self):
        self.added_words_number += 1
        self.save()   

    def statistics_update(self, total_ans_num, correct_ans_num):
        self.ended_exercise_number += 1
        self.relative_rating.value_update(total_ans_num, correct_ans_num)
        self.save()   

    # def add_word(self, words):
    #     for word in words:
    #         if not word in self.word_from_exercise.all():
    #             self.word_from_exercise.add(word)
    #             self.save()
    #             return True
    #         else:
    #             return False