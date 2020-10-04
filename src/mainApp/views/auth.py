from mainApp.my_models import *
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from mainApp.forms import CollectionForm, AuthUserForm, RegisterUserForm, EditUserForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from mainApp.controller import SessionController
from django.contrib.auth import authenticate, login
from .decorators import *

@method_decorator(logout_only, name='dispatch')
class LoginUserView(LoginView, SessionController):
    template_name = 'mainApp/loginPage.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('cols_page', args=[1])

    def get_success_url(self):
        super().open_session(self.request)
        return self.success_url

@method_decorator(logout_only, name='dispatch')
class RegisterUserView(CreateView, SessionController):
    model = User
    template_name = 'mainApp/registerPage.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('cols_page', args=[1])
    
    def form_valid(self,form):
        form_valid = super().form_valid(form)

        new_user = form.save(commit=False)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        new_user.set_password(password)
        new_user.save()

        rat = RelativeRating.objects.create()
        stat = UserStatistics.objects.create(user=new_user, relative_rating=rat)
        # User.objects.create(user=new_user, statistics=stat)

        
        aut_user = authenticate(username=username,password=password)
        login(self.request, aut_user)
        super().open_session(self.request)
        
        return form_valid

@method_decorator(login_required, name='dispatch')
class LogoutUserView(LogoutView):
    next_page = reverse_lazy('cols_page', args=[1])

    def dispatch(self, request, *args, **kwargs):

        try:
            ex = Exercise.objects.get(user=request.user.id)
            print("------------", ex)
            answers = UserAnswer.objects.filter(exercise=ex)

            if "is_ended" in self.request.session:
                is_ended = self.request.session["is_ended"]
                words_number = self.request.session["len"]
                tot_ans_num = self.request.session["total_answers_number"]
                cor_ans_num = self.request.session["correct_answers_number"]
                col_id = self.request.session["collection_id"]
                
                ex.update(is_ended, words_number, tot_ans_num, cor_ans_num, col_id)

                if words_number:
                    words_arr = self.request.session["words"] 
                    answers_arr = self.request.session["answers"]
                    print("lennnnn", len(words_arr), len(answers_arr), cor_ans_num, tot_ans_num)
                    if answers:
                        for ans in answers:
                            ans.delete()
                
                    for i in range(len(words_arr)):
                        word = Word.objects.get(id=words_arr[i])
                        print("len ans", len(answers_arr))
                        if (i < tot_ans_num):
                            UserAnswer.objects.create(exercise=ex, word=word, answer=answers_arr[i])
                        else:
                            UserAnswer.objects.create(exercise=ex, word=word, answer="---")
        except Exercise.DoesNotExist:
            pass

        return super().dispatch(request, *args, **kwargs)