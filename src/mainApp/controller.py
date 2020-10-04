from django.db import models
from .my_models.exercise import Exercise
from .my_models.user_answer import UserAnswer


class SessionController():
    def open_session(self, request):
        try:
            ex = Exercise.objects.get(user=request.user.id)
            answers = UserAnswer.objects.filter(exercise=ex)

            request.session.set_expiry(None)
            request.session["is_ended"] = ex.is_ended
            request.session["len"] = ex.words_number
            request.session["total_answers_number"] = ex.total_answers_number
            request.session["correct_answers_number"] = ex.correct_answers_number
            request.session["collection_id"] = ex.collection.id

            print(ex.total_answers_number, ex.correct_answers_number)

            if ex.words_number:
                words_arr = []
                answers_arr = []

                for i in range (len(answers)):
                    words_arr.append(answers[i].word.id)
                    print(answers[i].id)

                    answers_arr.append(answers[i].answer)

                request.session["words"] = words_arr
                request.session["answers"] = answers_arr
        except Exercise.DoesNotExist:
            request.session.set_expiry(None)
            request.session["is_ended"] = True