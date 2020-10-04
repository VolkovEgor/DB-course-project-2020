from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from mainApp.forms import CollectionForm
from mainApp.my_models import *
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .decorators import *
from mainApp.const import *

class CollectionListView(ListView):
    model = Collection
    template_name = 'mainApp/homePage.html'
    main_data = None
    order_page_name = "col_order_by_page"
    filter_page_name = "col_filter_page"
    page_type = 1

    def get_main_data(self,**kwargs):
        self.main_data = self.model.objects.filter(is_public=True)

    def filter(self,**kwargs):
        return self.main_data

    def get_main_page_name_p2(self):
        return ""

    def get_all_data(self, **kwargs):
        self.request.session["cur_rev_url_for_word"] = self.request.path
        self.request.session["cur_url_col_list"] = self.request.path

        kwargs["users"] = User.objects.order_by("username")
        tmp = UserStatistics.objects.order_by('-relative_rating__correct_answers_number')[:TOPS_NUMBER]
        users_top = []
        for i in range(TOPS_NUMBER):
            users_top.append({"position":i+1, "stat":tmp[i]})
        kwargs["users_top"] = users_top

        tmp = Word.objects.order_by('-views_number')[:TOPS_NUMBER]
        words_top = []
        for i in range(TOPS_NUMBER):
            words_top.append({"position":i+1, "stat":tmp[i]})
        kwargs["words_top"] = words_top
        print(words_top)

        self.get_main_data(**kwargs)
        cur_page = Paginator(self.filter(**kwargs), COL_NUMBER_IN_PAGE)
        pos = self.request.path.rfind("/")
        number = int(self.request.path[(pos + 1):])
        kwargs['list_collections'] = cur_page.page(number)
        kwargs['collections_number'] = len(kwargs['list_collections'])

        print(kwargs['list_collections'])
        kwargs["page_type"] = self.page_type
        kwargs['is_success'] = True
        if not len(kwargs['list_collections']):
            kwargs['is_success'] = False

        kwargs['main_page_name_p1'] = self.request.path[:pos]
        kwargs['main_page_name_p2'] = self.get_main_page_name_p2()
        kwargs['order_page_name'] = self.order_page_name
        kwargs['filter_page_name'] = self.filter_page_name

        return kwargs
        

    def get_context_data(self,**kwargs):
        kwargs = self.get_all_data(**kwargs)
        return super().get_context_data(**kwargs)

class ColOrderByListView(CollectionListView):
    main_page_name = "col_filter_by_page"
    def filter(self,**kwargs):
        pos1 = self.request.path.rfind("/page")
        pos2 = self.request.path.rfind("/order_by")
        print(pos1, pos2)
        field_sort = self.request.path[:(pos1)]
        field_sort = int(field_sort[(pos2 + 10):])
        if field_sort == 1:
            return self.main_data.order_by('-date')
        elif field_sort == 2:
            # arr = self.main_data.order_by('title')
            # sort_arr = []
            # for i in range(len(arr)):
            #     sort_arr.append([arr[i], arr[i].title])
            # print("ARR", sort_arr[:10])
            return self.main_data.order_by('title')
        elif field_sort == 3:
            return self.main_data.order_by('-views_number')
        elif field_sort == 4:
            return self.main_data.order_by('-additions_number')

class ColFilterListView(CollectionListView):
    main_page_name = "col_order_by_page"
    def filter(self,**kwargs):
        cur_level = self.request.GET.get('level')
        cur_author = self.request.GET.get('author')

        self.request.session["cur_rev_url_for_word"] = self.request.path + "?level={0}&author={1}".format(cur_level, cur_author)
        self.request.session["cur_url_col_list"] = self.request.path + "?level={0}&author={1}".format(cur_level, cur_author)
        print("++++++", self.request.session["cur_url_col_list"])
        print("++++++", self.request.path)

        if cur_level != "...":
            print("====", cur_level)
            cur_level = int(cur_level)

            level = 'e'
            if cur_level == 2:
                level = 'm'
            elif cur_level == 3:
                level = 'h'
            print(level)
            
            if cur_author == "":
                return self.main_data.filter(level=level)
            else:
                return self.main_data.filter(level=level, author__username__istartswith=cur_author)
        else:
            if cur_author == "":
                return self.main_data.all()
            else:
                return self.main_data.filter(author__username__istartswith=cur_author)
    
    def get_main_page_name_p2(self):
        cur_level = self.request.GET.get('level')
        cur_author = self.request.GET.get('author')

        return "?level={0}&author={1}".format(cur_level, cur_author)

class UserSubscriptionsListView(CollectionListView):
    template_name = 'mainApp/mySubscriptionsPage.html'
    order_page_name = "my_subs_order_by_page"
    filter_page_name = "my_subs_filter_page"
    page_type = 3

    def get_main_data(self,**kwargs):
        self.main_data = Collection.own.filter_by_subscriber(subscr_id=self.request.user.id)
    
    def get_context_data(self,**kwargs):
        kwargs = self.get_all_data(**kwargs)
        kwargs["all_collections_number"] = len(self.main_data)
        return super().get_context_data(**kwargs)

class UserSubsOrderByListView(UserSubscriptionsListView, ColOrderByListView):
    pass

class UserSubsFilterListView(UserSubscriptionsListView, ColFilterListView):
    pass

class UserCollectionListView(CreateView, CollectionListView):
    model = Collection
    template_name = 'mainApp/myCollectionsPage.html'
    form_class = CollectionForm
    success_url = reverse_lazy('my_col_page', args=[1])
    order_page_name = "my_col_order_by_page"
    filter_page_name = "my_col_filter_page"
    page_type = 2

    def get_main_data(self,**kwargs):
        self.main_data = Collection.objects.filter(author=self.request.user.id)
        print(self.main_data)

    def get_context_data(self,**kwargs):
        kwargs = self.get_all_data(**kwargs)
        kwargs["all_collections_number"] = len(self.main_data)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        print(instance.image)
        instance.save() 
        return CreateView.form_valid(self, form)

class UserColOrderByListView(UserCollectionListView, ColOrderByListView):
    pass

class UserColFilterListView(UserCollectionListView, ColFilterListView):
    pass

class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'mainApp/collectionPage.html'
    context_object_name = 'cur_col'
    def get_context_data(self,**kwargs):
        cur_col = self.get_object()
        cur_col.inc_views_number()
        
        words = Collection.objects.get(id=cur_col.id).words.all().order_by("title")

        words_dict = words.values("id", "title", "transcription", "translation")

        if self.request.user.is_authenticated:
            user = self.request.user.id
            if words:
                for word in words_dict:
                    status = "not learned"
                    try:
                        user_stat = UserWordStatus.objects.get(user=user, word=word["id"])
                        
                        if user_stat.is_learned:
                            status = "learned"
                        else:
                            status = "failed"
                    except UserWordStatus.DoesNotExist:
                        pass
                    
                    tmp = {"status":status}
                    word.update(tmp)

            learned_word_id = UserWordStatus.objects.filter(user=self.request.user, is_learned=True).values('word')
            new_words = Collection.own.get_word_from_collections(cur_col.id).exclude(id__in=learned_word_id)

            kwargs['new_words_number'] = len(new_words)
            kwargs['exercise_is_ended'] = self.request.session["is_ended"]
            if not kwargs['exercise_is_ended']:
                kwargs['next_step'] = self.request.session["total_answers_number"] + 1
            else:
                kwargs['next_step'] = 1

        kwargs['words_number'] = len(words_dict)
        kwargs['words'] = words_dict


        kwargs['cur_url_col_list'] = self.request.session["cur_url_col_list"]
        self.request.session["cur_rev_url_for_word"] = self.request.path
        return super().get_context_data(**kwargs)
    
    def get_object(self):
        object = super(CollectionDetailView, self).get_object()
        # if not self.request.user.is_authenticated():
        #     raise Http404
        return object


@method_decorator(collection_author_decorators, name='dispatch')
class CollectionUpdateView(UpdateView):
    model = Collection
    template_name = 'mainApp/editCollectionPage.html'
    form_class = CollectionForm
    success_url = reverse_lazy('my_col_page', args=[1])

    def get_context_data(self,**kwargs):
        cur_col = self.get_object()
        kwargs['cur_col'] = Collection.objects.get(id=cur_col.id)
        return super().get_context_data(**kwargs)
    
    # def get_object(self):
    #     object = super(CollectionUpdateView, self).get_object()
    #     # if not self.request.user.is_authenticated():
    #     #     raise Http404
    #     return object



@method_decorator(collection_author_decorators, name='dispatch')
class CollectionDeleteView(DeleteView):
    model = Collection
    template_name = 'mainApp/editCollectionsPage.html'
    success_url = reverse_lazy('my_col_page', args=[1])

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        print("------------------------------------------------")
        try:
            ex = Exercise.objects.get(user = request.user, collection=self.object)
            print("DELETE ---", ex)
            ex.delete()
            request.session["is_ended"] = True
        except Exercise.DoesNotExist:
            pass

        self.object.delete()
        return redirect(success_url)


class AddSubscriptionView(DetailView):
    login_url = reverse_lazy('login_page')
    model = Collection

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.add_subscriber(self.request.user)
        return_path = request.META.get('HTTP_REFERER','/')
        return redirect(return_path)


class RemoveSubscriptionView(DetailView):
    login_url = reverse_lazy('login_page')
    model = Collection

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.remove_subscriber(self.request.user.id)
        return_path  = request.META.get('HTTP_REFERER','/')
        return redirect(return_path)






            

