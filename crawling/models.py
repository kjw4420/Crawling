from django.db import models

class CrawlingModel(models.Model):
    title = models.CharField(max_length=50, default ="")
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title
    
# class CrawlindData(models.Model):
#     news = models.CharField(max_length =200, default ="")    

#     def __str__(self):
#         return self.news
    
    
    #Redis??