from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    publish_date = models.DateField()


class BookImport(models.Model):
    csv_file = models.FileField(upload_to='uploads/')
    date_added = models.DateTimeField(auto_now_add=True)
