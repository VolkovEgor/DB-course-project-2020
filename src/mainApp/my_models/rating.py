from django.db import models

class RelativeRating(models.Model):
    total_answers_number = models.PositiveIntegerField(default=0)
    correct_answers_number = models.PositiveIntegerField(default=0)
    value = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    def value_update(self, total_ans_num, correct_ans_num):
        print('--------- rating', total_ans_num, correct_ans_num)

        self.total_answers_number += total_ans_num
        self.correct_answers_number += correct_ans_num
        if not self.total_answers_number:
            self.value = 0
        else:
            self.value = self.correct_answers_number / self.total_answers_number * 10
        self.save()