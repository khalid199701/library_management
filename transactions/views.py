from django.shortcuts import render
from .models import Transaction
from django.views.generic import CreateView, ListView
from transactions.forms import DepositForm, TransactionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from datetime import datetime
from django.db.models import Sum
# Create your views here.
class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs



class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields=[
                'balance'
            ]
        )
        mail_subject = 'Deposit Message'
        message = render_to_string('deposite_email.html', {
            'user' : self.request.user,
            'amount': amount,
        })
        to_email = self.request.user.email
        send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()
        return super().form_valid(form)
    
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    balance = 0 # filter korar pore ba age amar total balance ke show korbe
    context_object_name = 'report_list'
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(timestamp__date__gte=start_date, timestamp__date__lte=end_date)
            self.balance = Transaction.objects.filter(
                timestamp__date__gte=start_date, timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.account.balance
       
        return queryset.distinct() # unique queryset hote hobe
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account
        })

        return context