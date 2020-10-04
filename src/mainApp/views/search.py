from mainApp.my_models import *
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.core.paginator import Paginator
import random
from mainApp.const import *


class SearchResultListView(ListView):
    model = Word
    template_name = 'mainApp/searchPage.html'
    is_success = True

    def get_queryset(self): # новый
        query = self.request.GET.get('search')
        object_list = Word.own.search_by_title(query)
        if not object_list:
            object_list = Word.own.search_by_translation(query)
        if not object_list:
            self.is_success = False
        self.request.session["cur_rev_url_for_word"] = "/search/page/1?search=" + str(query)
        return object_list
    
    def get_main_page_name_p2(self):
        query = self.request.GET.get('search')
        return "?search=" + str(query)

    def get_context_data(self,**kwargs):
        kwargs['is_success'] = self.is_success
        kwargs['my_collections'] = Collection.own.filter_by_id(self.request.user.id)

        cur_page = Paginator(self.get_queryset(), COL_NUMBER_IN_PAGE)
        pos = self.request.path.rfind("/")
        number = int(self.request.path[(pos + 1):])
        kwargs['object_list'] = cur_page.page(number)

        kwargs['main_page_name_p1'] = self.request.path[:pos]
        kwargs['main_page_name_p2'] = self.get_main_page_name_p2()
        
        return super().get_context_data(**kwargs)