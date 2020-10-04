from django.test import TestCase
from django.contrib.auth.models import User

from .models.profile import Profile
from .models.user_statistics import UserStatistics
from .models.word import Word
from .models.collection import Collection
from .models.exercise import Exercise
from .models.rating import Rating

class RatingTests(TestCase):
    def test_change_raiting(self):
        # Создание рейтинга
        rat = Rating.objects.create()

        self.assertEqual(rat.total_answers_number, 0)
        self.assertEqual(rat.correct_answers_number, 0)
        self.assertEqual(rat.value, 0)

        # Обновление рейтинга
        rat.value_update(10, 7)

        self.assertEqual(rat.total_answers_number, 10)
        self.assertEqual(rat.correct_answers_number, 7)
        self.assertEqual(rat.value, 7)

        rat.value_update(5, 5)

        self.assertEqual(rat.total_answers_number, 15)
        self.assertEqual(rat.correct_answers_number, 12)
        self.assertEqual(rat.value, 8)
        
class UserStatisticsTests(TestCase):
    def test_change_statistics(self):
        # Создание пользовательской статистики
        rat = Rating.objects.create()
        stat = UserStatistics.objects.create(rating=rat)

        self.assertEqual(stat.viewed_words_number, 0)
        self.assertEqual(stat.added_words_number, 0)
        self.assertEqual(stat.ended_exercise_number, 0)
        self.assertEqual(stat.rating.value, 0)

         # Обновление пользовательской статистики
        stat.inc_viewed_words_number()
        stat.inc_added_words_number()
        stat.inc_viewed_words_number()
        stat.stat_update(10, 7)

        self.assertEqual(stat.viewed_words_number, 2)
        self.assertEqual(stat.added_words_number, 1)
        self.assertEqual(stat.ended_exercise_number, 1)
        self.assertEqual(stat.rating.value, 7)


class ProfileTests(TestCase):
    def test_create_profil(self):
        # Создание профиля
        rat = Rating.objects.create()
        stat = UserStatistics.objects.create(rating=rat)
        user = User.objects.create_user('egor')
        profile = Profile.objects.create(user=user, statistics=stat)
        self.assertEqual(str(profile), 'egor')
        self.assertEqual(profile.id, 1)


class WordTests(TestCase):
    def test_create_word(self):
        # Создание слова
        rat = Rating.objects.create()
        word = Word.objects.create(
            title='cat',
            transcription='caet',
            translation='кошка',
            rating=rat
        )

        self.assertEqual(word.title, 'cat')
        self.assertEqual(word.transcription, 'caet')
        self.assertEqual(word.translation, 'кошка')
        self.assertEqual(word.rating.value, 0)

        # Обновление полей
        word.inc_additions_number()
        word.inc_views_number()
        word.inc_additions_number()
            
        self.assertEqual(word.additions_number, 2)
        self.assertEqual(word.views_number, 1)

        # Создание слов
        rat = Rating.objects.create(value=3.22)
        word = Word.objects.create(
            title='mouse',
            transcription='maus',
            translation='мышь',
            rating=rat
        )

        rat = Rating.objects.create(value=7.5)
        word = Word.objects.create(
            title='apple',
            transcription='apple',
            translation='яблоко',
            rating=rat
        )

        # Сортировка
        res = Word.own.order_by_title()
        self.assertEqual(res[0].title, 'apple')
        self.assertEqual(res[1].title, 'cat')
        self.assertEqual(res[2].title, 'mouse')

        res = Word.own.order_by_rating()
        self.assertEqual(res[0].title, 'apple')
        self.assertEqual(res[1].title, 'mouse')
        self.assertEqual(res[2].title, 'cat')

        # Поиск слова
        res = Word.own.search_by_title('mo')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].title, 'mouse')

class CollectionTests(TestCase):
    def test_create_collection(self):
        # Создание подборки
        rat = Rating.objects.create()
        stat = UserStatistics.objects.create(rating=rat)
        user = User.objects.create_user('egor')
        profile = Profile.objects.create(user=user, statistics=stat)

        col = Collection.objects.create(
            title='Animals',
            author=profile,
            views_number=3
        )

        self.assertEqual(col.title, 'Animals')
        self.assertEqual(str(col.author), 'egor')

        # фильтрация по id
        res_col = Collection.own.filter_by_id(id=profile.id)
        self.assertEqual(len(res_col), 1)

        # Изменение значений полей
        col.change_title('Not animals')
        col.change_level('hard')
        col.inc_views_number()
        
        self.assertEqual(col.title, 'Not animals')
        self.assertEqual(col.level, 'hard')
        self.assertEqual(col.views_number, 4)

        # Добавление слова в подборку
        rat = Rating.objects.create()
        word = Word.objects.create(
            title='cat',
            transcription='caet',
            translation='кошка',
            rating=rat
        )
        col.add_word(word)
        self.assertEqual(col.words_number, 1)

        # Удаление слова из подборки
        col.remove_word(word)
        self.assertEqual(col.words_number, 0)

        # Добавление подписчика на подборку
        rat = Rating.objects.create()
        stat = UserStatistics.objects.create(rating=rat)
        user = User.objects.create_user('ivan')
        profile2 = Profile.objects.create(user=user, statistics=stat)
        col.add_subscriber(profile2)
        res_col = Collection.own.filter_by_subscriber(subscr_id=profile2.id)
        self.assertEqual(len(res_col), 1)
        self.assertEqual(res.name, "ivan")

        # Удаление подписчика
        col.remove_subscriber(profile2)
        res_col = Collection.own.filter_by_subscriber(subscr_id=profile2.id)
        self.assertEqual(len(res_col), 0)

        # Создание коллекций
        col = Collection.objects.create(
            title='Home',
            author=profile,
            views_number=5
        )

        col = Collection.objects.create(
            title='Family',
            author=profile,
            views_number=1
        )

        # Сортировка
        res = Collection.own.order_by_views_number()
        self.assertEqual(res[0].title, 'Home')
        self.assertEqual(res[1].title, 'Not animals')
        self.assertEqual(res[2].title, 'Family')

        




class ExerciseTests(TestCase):
    def test_change_execise(self):
        # Создание упражнения
        rat = Rating.objects.create()
        stat = UserStatistics.objects.create(rating=rat)
        user = User.objects.create_user('egor')
        profile = Profile.objects.create(user=user, statistics=stat)

        ex = Exercise.objects.create(user=profile)

        # Создание и добавление слов в упражнение
        rat = Rating.objects.create()
        word_1 = Word.objects.create(
            title='cat',
            transcription='caet',
            translation='кошка',
            rating=rat
        )

        rat = Rating.objects.create()
        word_2 = Word.objects.create(
            title='dog',
            transcription='dog',
            translation='собака',
            rating=rat
        )

        rat = Rating.objects.create()
        word_3 = Word.objects.create(
            title='mouse',
            transcription='maus',
            translation='мышь',
            rating=rat
        )

        lst = [word_1, word_2, word_3]
        ex.save_words(lst)

        # Cохранение статистики упражнения
        ex.save_stat(10, 3)
        self.assertEqual(ex.is_ended, True)
        self.assertEqual(ex.total_answers_number, 10)
        self.assertEqual(ex.correct_answers_number, 3)

