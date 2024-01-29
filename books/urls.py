from django.urls import path
from . import views
urlpatterns = [
    path('details/<int:id>/', views.DetailBookView.as_view(), name='detail_book'),
    path('details/borrow/<int:id>/', views.borrowBook, name='borrow_book'),
    path('details/borrowing_history/', views.borrowing_history, name='borrowing_history'),
    path('details/borrow/return/<int:id>/', views.returnBook, name='return_book'),
]