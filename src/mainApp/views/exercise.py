
from mainApp.my_models import *
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
import random
from mainApp.const import *
from mainApp.controller import *

class ExerciseStartView(DetailView):
    def dispatch(self, request, col_id, *args, **kwargs):
        
        try:
            ex = Exercise.objects.get(user=self.request.user.id)
            ex.collection = Collection.objects.get(id=col_id)
            ex.save()
        except Exercise.DoesNotExist:
            col = Collection.objects.get(id=col_id)
            Exercise.objects.create(user=self.request.user, collection=col)
            controller = SessionController()
            controller.open_session(self.request)

        learned_word_id = UserWordStatus.objects.filter(user=request.user, is_learned=True).values('word')
        words = Collection.own.get_word_from_collections(col_id).exclude(id__in=learned_word_id).order_by("title")
        print(words)

        indexes_arr = [i for i in range (words.count())]
        print("indexes", indexes_arr)
        random.shuffle(indexes_arr)
        print("indexes", indexes_arr)

        if len(indexes_arr) > WORDS_IN_EXERCISE:
            indexes_arr = indexes_arr[:WORDS_IN_EXERCISE]

        cur_len= len(indexes_arr)
        arr_words = []
        for i in range (cur_len):
            cur_index = indexes_arr[i]
            arr_words.append(words[cur_index].id)
            print(words)
            print("cur", cur_index, words[cur_index])

        self.request.session["total_answers_number"] = 0
        self.request.session["correct_answers_number"] = 0
        print("start_number_ans", self.request.session["total_answers_number"])
        
        request.session["words"] = arr_words
        request.session["answers"] = [None for i in range(cur_len)]
        request.session["is_ended"] = False
        request.session["len"] = cur_len
        request.session["collection_id"] = col_id
        return redirect("exercise_step_page", 1)

class ExerciseStepView(DetailView):
    def dispatch(self, request, step_id, *args, **kwargs):

        word = Word.objects.get(id=request.session["words"][step_id - 1])
        if request.method == 'GET':
            answer = request.GET.get('answer')
            
            if(answer):                    
                answers = request.session["answers"]
                answers[step_id - 1] = answer
                request.session["answers"] = answers
                print(request.session["answers"])

                self.request.session["total_answers_number"] += 1
                print("number_ans", self.request.session["total_answers_number"], " step ", step_id)

                if (step_id == request.session["len"]):
                    return redirect("exercise_res_page")
                else:
                    return redirect("exercise_step_page", step_id + 1)
    

        return render(request, "mainApp/exerciseStep.html", {"word": word.translation, 
            "len":request.session["len"],
            "step":step_id,
            })

class ExerciseResultView(ListView):
    def dispatch(self, request, *args, **kwargs):
        user=request.user
        request.session["is_ended"] = True
        words = request.session["words"]
        answers = request.session["answers"]
        print(request.session["answers"])
        correct_answers_number = 0
        table = []    
        for i in range(len(words)):
            word = Word.objects.get(id=request.session["words"][i])
            title = word.title
            translation = word.translation


            bool_answer = (title == answers[i])
            if bool_answer:
                word.rating_update(1, 1)
                correct_answers_number += 1
            else:
                word.rating_update(1, 0)
            table.append({"bool_answer":bool_answer, "title":title, "translation":translation, "answer":answers[i]})

            try:
                user_stat = UserWordStatus.objects.get(user=user, word=words[i])
                
                if bool_answer and not user_stat.is_learned:
                    user_stat.change_status(True)
                if not bool_answer:
                    user_stat.change_errors_number()
            except UserWordStatus.DoesNotExist:
                if bool_answer:
                    UserWordStatus.objects.create(user=user, word=word, is_learned=True)
                else:
                    UserWordStatus.objects.create(user=user, word=word, is_learned=False, errors_number = 1)

        stat = UserStatistics.objects.get(user=user)
        print(stat)
        total_answers_number = request.session["len"]
        stat.statistics_update(total_answers_number, correct_answers_number)

        col_id = request.session["collection_id"]
        user_words_id = UserWordStatus.objects.filter(user=request.user, is_learned=True).values('word')
        all_learned_words_in_col = Collection.own.get_word_from_collections(col_id).filter(id__in=user_words_id).count()
        all_words_in_col = Collection.own.get_word_from_collections(col_id).count()
        print(all_learned_words_in_col, all_words_in_col)

        words_is_remained = True
        if all_learned_words_in_col == all_words_in_col:
            words_is_remained = False

        return render(request, "mainApp/exerciseResultPage.html", {"table": table, 
            "correct_number":correct_answers_number,
            "total_number":total_answers_number,
            "col_id":col_id,
            "cur_url_col":self.request.session["cur_rev_url_for_word"],
            "words_is_remained":words_is_remained})



class ResetProgressView(ListView):
    def dispatch(self, request, col_id, *args, **kwargs):
        col_word_id = Collection.objects.get(id=col_id).words.all()
        err_answers = 0
        correct_answers = 0
        for cur_word in col_word_id:
            try:
                cur_answer = UserWordStatus.objects.get(user=request.user, word=cur_word)
                if cur_answer.is_learned:
                    correct_answers += 1
                err_answers += cur_answer.errors_number
                print(cur_answer.word.title, cur_answer.errors_number)
                cur_answer.delete()
            except UserWordStatus.DoesNotExist:
                pass
        
        stat = UserStatistics.objects.get(user=request.user)
        stat.relative_rating.value_update(- correct_answers - err_answers, -correct_answers)

        return redirect("col_page", col_id)