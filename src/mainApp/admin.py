from django.contrib import admin

from .my_models.word import Word
from .my_models.user import User
from .my_models.user_statistics import UserStatistics
from .my_models.collection import Collection
from .my_models.exercise import Exercise
from .my_models.rating import RelativeRating
from .my_models.user_answer import UserAnswer
from .my_models.user_word_status import UserWordStatus

admin.site.register(UserStatistics)
admin.site.register(User)
admin.site.register(Word)
admin.site.register(Collection)
admin.site.register(Exercise)
admin.site.register(RelativeRating)
admin.site.register(UserAnswer)
admin.site.register(UserWordStatus)
