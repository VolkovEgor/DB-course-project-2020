from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from .my_models.collection import Collection
from .my_models.word import Word
from .forms import CollectionForm, AuthUserForm, RegisterUserForm, EditUserForm
from .my_models.user import User
from .my_models.user_statistics import UserStatistics
from .my_models.rating import RelativeRating
from .my_models.exercise import Exercise
from .my_models.user_answer import UserAnswer
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .my_models.user import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .controller import SessionController
from .my_models.user_word_status import UserWordStatus
from django.core.paginator import Paginator
from .decorators import *
import random




TOPS_NUMBER = 5
COL_NUMBER_IN_PAGE = 10

class CollectionListView(ListView):
    model = Collection
    template_name = 'mainApp/homePage.html'
    main_data = None
    order_page_name = "col_order_by_page"
    filter_page_name = "col_filter_page"
    page_type = 1

    def get_main_data(self,**kwargs):
        self.main_data = self.model.objects.all()

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
                return self.main_data.filter(level=level, author__username=cur_author)
        else:
            if cur_author == "":
                return self.main_data.all()
            else:
                return self.main_data.filter(author__username=cur_author)
    
    def get_main_page_name_p2(self):
        cur_level = self.request.GET.get('level')
        cur_author = self.request.GET.get('author')

        return "?level={0}&author={1}".format(cur_level, cur_author)

class MySubscriptionsListView(CollectionListView):
    template_name = 'mainApp/mySubscriptionsPage.html'
    order_page_name = "my_subs_order_by_page"
    filter_page_name = "my_subs_filter_page"
    page_type = 3

    def get_main_data(self,**kwargs):
        self.main_data = Collection.own.filter_by_subscriber(subscr_id=self.request.user.id)

class MySubsOrderByListView(MySubscriptionsListView, ColOrderByListView):
    pass

class MySubsFilterListView(MySubscriptionsListView, ColFilterListView):
    pass

class MyCollectionListView(CreateView, CollectionListView):
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
        kwargs["all_collections_number"] = len(Collection.objects.filter(author=self.request.user.id))
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        print(instance.image)
        instance.save() 
        return CreateView.form_valid(self, form)

class MyColOrderByListView(MyCollectionListView, ColOrderByListView):
    pass

class MyColFilterListView(MyCollectionListView, ColFilterListView):
    pass

class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'mainApp/collectionPage.html'
    context_object_name = 'cur_col'
    def get_context_data(self,**kwargs):
        cur_col = self.get_object()
        cur_col.inc_views_number()
        
        words = Collection.own.get_word_from_collections(cur_col.id)
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

        return super().get_context_data(**kwargs)

class UserStatDetailView(DetailView):
    login_url = reverse_lazy('login_page')
    model = UserStatistics
    template_name = 'mainApp/userStatPage.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return UserStatistics.objects.get(user=pk)

    def get_context_data(self,**kwargs):
        cur_stat = self.get_object()
        kwargs['stat'] = cur_stat
        kwargs['error_number'] = cur_stat.relative_rating.total_answers_number - cur_stat.relative_rating.correct_answers_number
        my_word = Word.objects.filter(collec__author=self.request.user.id).distinct()
        kwargs['added_words'] = len(my_word)
        return super().get_context_data(**kwargs)


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
        

@method_decorator(collection_author_decorators, name='dispatch')
class CollectionDeleteView(DeleteView):
    model = Collection
    template_name = 'mainApp/editCollectionsPage.html'
    success_url = reverse_lazy('my_col_page', args=[1])



class AddSubscriptionView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login_page')
    model = Collection

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.add_subscriber(self.request.user)
        return_path  = request.META.get('HTTP_REFERER','/')
        return redirect(return_path)


class RemoveSubscriptionView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login_page')
    model = Collection

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.remove_subscriber(self.request.user.id)
        return_path  = request.META.get('HTTP_REFERER','/')
        return redirect(return_path)


class AddWordView( DetailView):
    # login_url = reverse_lazy('login_page')
    # model = Collection
 
# def get_object(self, queryset=None):
#     id_col, id_word = self.kwargs.get(self.pk_url_kwarg)
#     print('---------------------', id_col, id_word)

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
    # login_url = reverse_lazy('login_page')
    # model = Collection
 
# def get_object(self, queryset=None):
#     id_col, id_word = self.kwargs.get(self.pk_url_kwarg)
#     print('---------------------', id_col, id_word)

    def dispatch(self, request, col_pk, word_pk, *args, **kwargs):
        col = Collection.objects.get(id=col_pk)
        word = Word.objects.get(id=word_pk)
        col.remove_word(word)

        
        return_path  = request.META.get('HTTP_REFERER','/')
        return redirect(return_path)


class ResetProgressView(ListView):
    def dispatch(self, request, col_id, *args, **kwargs):
        user_words_id = UserWordStatus.objects.filter(user=request.user).values('word')
        all_learned_words_in_col = Collection.own.get_word_from_collections(col_id).filter(id__in=user_words_id).len()
        all_words_in_col = Collection.own.get_word_from_collections(col_id).len()
        print(all_learned_words_in_col, all_words_in_col)


        print(words)

        return redirect("col_page", col_id)


            




# # @login_required
# def edit(request):
#     if request.method == 'POST':
#         user_form = UserEditForm(instance=request.user,data=request.POST)
#         profile_form = ProfileEditForm(
#         data=request.POST,
#         files=request.FILES)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#     else:
#         user_form = UserEditForm(instance=request.user)
#         profile_form = ProfileEditForm()
#     return render(request,'mainApp/editProfilePage.html',
#     {'user_form': user_form,'profile_form': profile_form})


# class ProfileUpdateView(UpdateView):
#     model = User
#     template_name = 'mainApp/editProfilePage.html'
#     # form_class = ProfileEditForm
#     #     #  ProfileEditForm
#     success_url = "/"
#     # context_object_name = 'my_profile'

#     # @login_required
#     def dispatch(self, request, *args, **kwargs):
#         if request.method == 'POST':
#             user_form = UserEditForm(instance=request.user,data=request.POST)
#             profile_form = ProfileEditForm(data=request.POST, files=request.FILES)
#             if user_form.is_valid() and profile_form.is_valid():
#                 user_form.save()
#                 prof = profile_form.save(commit=False)
                
#                 cur_user = self.get_object()
#                 # print("------------------", str(cur_user), cur_user.id)
#                 cur_prof = User.own.get_profile_id_by_user_id(cur_user)
#                 # print("------------------", str(cur_user), cur_user.id)
#                 cur_prof.photo = prof.photo
#                 print("------------------", str(cur_prof), cur_prof.photo, prof.photo)
#                 cur_prof.save()
#                 # print(str(cur_prof))
#                 # cur_prof.change_photo(photo)

#         else:
#             user_form = UserEditForm(instance=request.user)
#             profile_form = ProfileEditForm()
        
#         # if request.method.lower() in self.http_method_names:
#         #     handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
#         # else:
#         #     handler = self.http_method_not_allowed
#         return render(request,'mainApp/editProfilePage.html',
#             {'user_form': user_form,'profile_form': profile_form})


#     def get_object(self):
#         object = super(ProfileUpdateView, self).get_object(queryset=None)
#         return object

# def login(request):
#     argc = {}
#     argc.update(csrf(request))
#     if update.POST:
#         username = request.POST.get('username', '')
#         password = request.POST.get('password', '')
#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             return redirect('/')
#         else:
#             argc['login_error'] = "Пользователь не найден"
#             return render('mainApp/loginPage.html', argc)
#     else:
#         return render('mainApp/loginPage.html', argc)
#     # return render(request, 'mainApp/loginPage.html')

# def logout(request):
#     auth.logout(request)
#     return redirect("/")

    # return render(request, 'mainApp/logoutPage.html')
    