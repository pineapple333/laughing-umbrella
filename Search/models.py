from django.db import models


# Create your models here.
class Publication:
    def __init__(self):
        self.authors = []
        self.title = ""
        self.points = 0

    def __repr__(self):
        return f'\n\tAuthors: {self.authors},\n\tTitle: {self.title},\n\tPoints: {self.points}'
