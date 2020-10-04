from django.db import models

class WordManager(models.Manager):
    def order_by_title(self):
        return self.order_by('title')
    
    def order_by_rating(self):
        return self.order_by('-rating')

    def search_by_title(self, word):
        return self.filter(title__istartswith=word).order_by('title')

    def search_by_translation(self, word):
        return self.filter(translation__istartswith=word).order_by('title')
