from django.db import models

# Create your models here.

class Publication(models.Model):
    authors = models.CharField(max_length=1000)
    title = models.CharField(max_length=256)
    points = models.IntegerField(default=5)
	cost = models.FloatField(default=0)

    def __str__(self):
        return f'{self.authors}; {self.title}; {self.points}'
