from django.db import models

from administration.models import Librarian
from books.models import Book
# Create your models here.

class Loan(models.Model):
    borrower_name = models.CharField(max_length=100)
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    librarian = models.ForeignKey(Librarian, on_delete=models.CASCADE, related_name='loans')

    def __str__(self):
        return f"{self.book_title} borrowed by {self.borrower_name}"


class Return(models.Model):
    loan = models.OneToOneField(Loan, on_delete=models.CASCADE, related_name='return')
    return_date = models.DateField(auto_now_add=True)
    condition_notes = models.TextField(blank=True)

    loan = models.OneToOneField(Loan, on_delete=models.CASCADE, related_name='return_record')

    def mark_as_returned(self):
        self.loan.is_returned = True
        self.loan.return_date = self.return_date
        self.loan.save()

    def __str__(self):
        return f"Return of {self.loan.book.title} on {self.return_date}"