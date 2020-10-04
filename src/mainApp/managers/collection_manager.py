from django.db import models

class CollectionManager(models.Manager):
    def filter_by_id(self, id):
        return self.filter(
            author__id=id,
        )
    
    def filter_by_subscriber(self, subscr_id):
        return self.filter(
            subscribers__id=subscr_id,
        )

    def filter_by_level(self, level):
        return self.filter(
            level=level
        )
    
    def order_by_title(self):
        return self.order_by('title')

    def order_by_views_number(self):
        return self.order_by('-views_number')
    
    def order_by_date(self):
        return self.order_by('-date')

    def get_word_from_collections(self, col_id):
        col = self.get(id=col_id)
        return col.words.all()