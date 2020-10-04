from django.db import models
from .user import User
from .collection import Collection

class Exercise(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='exercise')
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    is_ended = models.BooleanField(default=True)
    words_number = models.PositiveIntegerField(default=0)
    total_answers_number = models.PositiveIntegerField(default=0)
    correct_answers_number = models.PositiveIntegerField(default=0)

    def update(self, is_ended, words_number, tot_ans_num, cor_ans_num, col_id):
        self.is_ended = is_ended
        self.words_number = words_number
        self.total_answers_number = tot_ans_num
        self.correct_answers_number = cor_ans_num
        self.collection_id = col_id
        self.save()

    # def save_words(self, cur_words):
    #     self.words.clear()
    #     for w in cur_words:
    #         self.words.add(w)
    #         self.save()

    # def save_stat(self, total_ans_num, correct_ans_num):
    #     if (total_ans_num == words_number):
    #         self.is_ended = True
    #     else:
    #         self.is_ended = False

    #     self.total_answers_number = total_ans_num
    #     self.correct_answers_number = correct_ans_num
    #     self.save()
