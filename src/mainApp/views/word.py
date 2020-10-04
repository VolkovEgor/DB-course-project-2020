from mainApp.my_models import *
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
import random

class WordDetailView(DetailView):
    login_url = reverse_lazy('login_page', args=[1])
    model = Word
    template_name = 'mainApp/wordPage.html'

    def get_context_data(self,**kwargs):
        cur_word = self.get_object()
        cur_word.inc_views_number()
        print(self.request.user)
        kwargs['word'] = cur_word
        kwargs['cur_url_col'] = self.request.session["cur_rev_url_for_word"]
        print(kwargs['cur_url_col'] )

        if self.request.user.is_authenticated:
            user_stat = UserStatistics.objects.get(user=self.request.user.id)
            user_stat.inc_viewed_words_number()
            kwargs['my_collections'] = Collection.own.filter_by_id(self.request.user.id)
            
            status = 0
            err_number = 0
            try:
                word_stat = UserWordStatus.objects.get(user=self.request.user.id, word=cur_word)
                err_number = word_stat.errors_number
                if word_stat.is_learned:
                    status = 2
                else:
                    status = 1
            except UserWordStatus.DoesNotExist:
                pass

            kwargs['word_stat'] = status
            kwargs['errors_number'] = err_number

        return super().get_context_data(**kwargs)


class AddWordView( DetailView):
    def dispatch(self, request, word_pk, *args, **kwargs):
        col_pk = self.request.GET.get('collection')
        print("-----", col_pk)
        col = Collection.objects.get(id=col_pk)
        word = Word.objects.get(id=word_pk)
        col.add_word(word)
        # print(col, word)
        # if not col.add_word(word):
        #     messages.success(request, 'Error updating your profile')
        # else:
        #     messages.error(request, 'Error updating your profile')

        
        return_path  = request.META.get('HTTP_REFERER','/')
        return redirect(return_path)

class RemoveWordView( DetailView):
    def dispatch(self, request, col_pk, word_pk, *args, **kwargs):
        col = Collection.objects.get(id=col_pk)
        word = Word.objects.get(id=word_pk)
        col.remove_word(word)

        
        return_path  = request.META.get('HTTP_REFERER','/')
        return redirect(return_path)