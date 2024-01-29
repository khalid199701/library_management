from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm, UserUpdateForm, ChangeUserForm
from django.urls import reverse_lazy
from django.contrib import messages
from books.models import Book
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, update_session_auth_hash, logout
from django.views.generic import UpdateView
from django.views import View
from .models import UserAccount
# Create your views here.

@login_required
def profile(request):
    user_account = UserAccount.objects.get(user=request.user)
    borrowed_books = Book.objects.filter(borrowed_by=user_account)
    return render(request, 'profile.html', {'book': borrowed_books, 'user_balance': user_account.balance})

class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    
class EditProfile(UpdateView):
    form_class = ChangeUserForm
    template_name = 'update_profile.html'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'
    def get_object(self, queryset=None):
        return self.request.user