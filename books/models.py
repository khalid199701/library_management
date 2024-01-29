from django.db import models
from book_category.models import Category
from accounts.models import UserAccount
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    borrowing_price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    borrowed_by = models.ForeignKey(UserAccount,on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    borrower = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # Assuming the name is a text field
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return f"Reviewed by {self.name}"
