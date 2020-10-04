from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('collections/page/<int:pk>', views.CollectionListView.as_view(), name='cols_page'),
    path('user_collections/page/<int:pk>', views.UserCollectionListView.as_view(), name='my_col_page'),
    path('user_subscriptions/page/<int:pk>', views.UserSubscriptionsListView.as_view(), name='my_subs_page'),
    path('collection/<int:pk>', views.CollectionDetailView.as_view(), name='col_page'),
    path('edit_collection/<int:pk>', views.CollectionUpdateView.as_view(), name='edit_col_page'),
    path('delete_collection/<int:pk>', views.CollectionDeleteView.as_view(), name='delete_col_page'),
    path('search/page/<int:pk>', views.SearchResultListView.as_view(), name='search_page'),
    path('login', views.LoginUserView.as_view(), name='login_page'),
    path('register', views.RegisterUserView.as_view(), name='register_page'),
    path('logout', views.LogoutUserView.as_view(), name='logout_page'),
    path('edit_profile/<int:pk>', views.ProfileUpdateView.as_view(), name='edit_profile_page'),
    path('add_subscription/<int:pk>', views.AddSubscriptionView.as_view(), name='add_subscription_page'),
    path('remove_subscription/<int:pk>', views.RemoveSubscriptionView.as_view(), name='remove_subscription_page'),

    path('collection/order_by/<int:ord>/page/<int:pk>', views.ColOrderByListView.as_view(), name='col_order_by_page'),
    path('collection/filter/page/<int:pk>', views.ColFilterListView.as_view(), name='col_filter_page'),

    path('user_collections/order_by/<int:ord>/page/<int:pk>', views.UserColOrderByListView.as_view(), name='my_col_order_by_page'),
    path('user_collections/filter/page/<int:pk>', views.UserColFilterListView.as_view(), name='my_col_filter_page'),

    path('user_subscriptions/order_by/<int:ord>/page/<int:pk>', views.UserSubsOrderByListView.as_view(), name='my_subs_order_by_page'),
    path('user_subscriptions/filter/page/<int:pk>', views.UserSubsFilterListView.as_view(), name='my_subs_filter_page'),

    path('add_word/<int:word_pk>', views.AddWordView.as_view(), name='add_word_page'),
    path('remove_word/<int:col_pk>/rem/<int:word_pk>', views.RemoveWordView.as_view(), name='remove_word_page'),

    path('word/<int:pk>', views.WordDetailView.as_view(), name='word_page'),
    path('user_statistics/<int:pk>', views.UserStatDetailView.as_view(), name='stat_page'),

    path('exercise_start/<int:col_id>', views.ExerciseStartView.as_view(), name='exercise_start_page'),
    path('exercise_step/<int:step_id>', views.ExerciseStepView.as_view(), name='exercise_step_page'),
    path('exercise/result>', views.ExerciseResultView.as_view(), name='exercise_res_page'),

    path('reset_progress_in_collection/<int:col_id>', views.ResetProgressView.as_view(), name='reset_progress_page'),
    
    ]

    
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('my_collections/<int:id>', views.my_col_page, name='my_col_page'),

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)