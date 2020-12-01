from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse

from datetime import date
import uuid


# Create your models here.


class Book(models.Model):
    title = models.CharField(max_length=200, help_text="Enter book title")
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief summary of book")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField('Genre', help_text='Enter the genre')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class Genre(models.Model):
    name = models.TextField(max_length=100, help_text="Enter a genre like, Science, Fiction")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])


class BookInstance(models.Model):
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for book instance")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    availability = models.CharField(max_length=1, choices=LOAN_STATUS, default='m', blank=True,
                                    help_text="Book availability")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (('can_marked_returned', 'Set book as returned'),)

    def __str__(self):
        return f"{self.id} ({self.book.title})"

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
