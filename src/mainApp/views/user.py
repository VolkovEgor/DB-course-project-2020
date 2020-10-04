from mainApp.my_models import *
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from mainApp.forms import EditUserForm
from django.views.generic import DetailView, CreateView, UpdateView
from .decorators import *

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = User
    template_name = 'mainApp/editProfilePage.html'
    form_class = EditUserForm
    success_url = reverse_lazy('cols_page', args=[1])
    
@method_decorator(login_required, name='dispatch')
class UserStatDetailView(DetailView):
    login_url = reverse_lazy('login_page')
    model = UserStatistics
    template_name = 'mainApp/userStatPage.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        user = User.objects.get(id=1)
        print("user", user.photo)
        return UserStatistics.objects.get(user=pk)

    def get_context_data(self,**kwargs):
        cur_stat = self.get_object()
        kwargs['stat'] = cur_stat
        kwargs['error_number'] = cur_stat.relative_rating.total_answers_number - cur_stat.relative_rating.correct_answers_number
        my_word = Word.objects.filter(words_in_col__author=self.request.user.id).distinct()
        kwargs['added_words'] = len(my_word)
        kwargs['user_col_numbers'] = Collection.objects.filter(author=self.request.user.id).count()
        return super().get_context_data(**kwargs)
