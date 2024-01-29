from django.shortcuts import render, redirect
from . import forms
from . import models
from django.views import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.

@login_required
def borrowBook(request, id):
    book = models.Book.objects.get(id=id)
    user_account = request.user.account  
    if not book.borrowed_by:
        if user_account.balance >= book.borrowing_price:
            m = user_account.balance
            user_account.balance -= book.borrowing_price
            user_account.save()

            book.borrowed_by = user_account
            book.save()
            mail_subject = 'Borrowing Message'
            message = render_to_string('borrowing_email.html', {
                'user' : request.user,
                'amount': book.borrowing_price,
                'money': m,
            })
            to_email = request.user.email
            send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
            send_email.attach_alternative(message, 'text/html')
            send_email.send()

    return redirect('profile')

@login_required
def returnBook(request, id):
    book = models.Book.objects.get(id=id)
    user_account = request.user.account

    if book.borrowed_by == user_account:
        user_account.balance += book.borrowing_price
        user_account.save()

        book.borrowed_by = None
        book.save()

    return redirect('profile')

@login_required
def borrowing_history(request):
    user_account = request.user.account
    borrowing_history = models.Book.objects.filter(borrowed_by=user_account).order_by('-timestamp')

    context = {
        'borrowing_history': borrowing_history,
    }

    return render(request, 'borrowing_history.html', context)


class DetailBookView(View):
    template_name = 'book_details.html'

    def get_object(self):
        book_id = self.kwargs.get('id')
        return get_object_or_404(models.Book, id=book_id)

    def get(self, request, *args, **kwargs):
        book_id = self.kwargs.get('id')
        book = models.Book.objects.get(id=book_id)
        review_form = forms.ReviewForm()
        reviews = book.reviews.all()

        context = {
            'book': book,
            'review_form': review_form,
            'reviews': reviews,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        review_form = forms.ReviewForm(data=self.request.POST)
        book = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            user_account = request.user.account
            new_review.borrower = user_account
            new_review.name = user_account.user.first_name
            new_review.email = user_account.user.email

            new_review.book = book
            new_review.save()
            
        return self.get(request, *args, **kwargs)

