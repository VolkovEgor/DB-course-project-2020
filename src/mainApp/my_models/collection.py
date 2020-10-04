from django.db import models
from .user import User
from ..managers.collection_manager import CollectionManager
from .word import Word  

class Collection(models.Model):
    LEVEL = (
        ('e', 'easy'),
        ('m', 'medium'),
        ('h', 'hard'),
    )
    title = models.CharField(max_length=50, verbose_name='Название')
    level = models.CharField(max_length=10, choices=LEVEL, default='easy', verbose_name='Уровень сложности')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, verbose_name = 'Изображение', default='default_col_image.png')

    words = models.ManyToManyField(Word, related_name='words_in_col')
    words_number = models.PositiveIntegerField(default=0)

    is_public = models.BooleanField(default=False, verbose_name='Общедоступная')
    subscribers = models.ManyToManyField(User, related_name='col')
    
    views_number = models.PositiveIntegerField(default=0)
    additions_number = models.PositiveIntegerField(default=0)

    objects = models.Manager()
    own = CollectionManager()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return '[pk={}] {}'.format(self.pk, self.title)
    
    def change_title(self, title):
        if title != '':
            self.title = title
            self.save()
    
    def change_level(self, level):
        if level == 'easy' or level == 'medium' or level == 'hard':
            self.level = level
            self.save()

    def add_word(self, word):
        if not word in self.words.all():
            self.words.add(word)
            self.words_number += 1
            word.inc_additions_number()
            self.save()
            return True
        else:
            return False

    def remove_word(self, word):
        if word in self.words.all():
            self.words.remove(word)
            self.words_number -= 1
            self.save()
            return True
        else:
            return False

    def add_subscriber(self, subscriber):
        if not subscriber in self.subscribers.all():
            self.subscribers.add(subscriber)
            self.additions_number += 1
            self.save()
            return True
        else:
            return False

    def remove_subscriber(self, subscriber):
        if not subscriber in self.subscribers.all():
            self.subscribers.remove(subscriber)
            self.additions_number -= 1
            self.save()
            return True
        else:
            return False



    def inc_views_number(self):
        self.views_number += 1
        self.save()

