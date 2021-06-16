from django.db import models


class Publication:
	def __init__(self):
		self.id = ""
		self.authors = []
		self.title = ""
		self.points = 0
		self.P = 0
		self.year = 0
		self.cost = 0
		self.m = 0
		self.affiliated_authors = []

	def __repr__(self):
		return f'\n\tAuthors: {self.authors},\n\tTitle: {self.title},\n\tPoints: {self.points},\n\tYear: {self.year}'


class Author:
	def __init__(self):
		self.name_surname = ""
		self.publications = []
		self.best_publications = []
		self.max_points = 0
