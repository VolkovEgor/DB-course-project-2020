from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from functools import wraps
from mainApp.my_models import Collection

def collection_author_only(function):
    @wraps(function)
    def wrap(request, pk, *args, **kwargs):
        collection = Collection.objects.get(id=pk)
        if request.user == collection.author:
            return function(request, pk, *args, **kwargs)
        else:
            return redirect('cols_page', 1)
    return wrap

def logout_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return redirect('index')
    return wrap


collection_author_decorators = [login_required, collection_author_only]