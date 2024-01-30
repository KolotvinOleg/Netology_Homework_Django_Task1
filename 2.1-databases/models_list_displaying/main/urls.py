"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, register_converter

from books.views import books_view, get_info_about_books_by_date, get_info_about_book
import books.converters

register_converter(books.converters.DateConverter, 'my_date')

urlpatterns = [
    path('books/', books_view, name='books'),
    path('books/<str:name_book>', get_info_about_book, name='book'),
    path('books/<my_date:pub_date>/', get_info_about_books_by_date, name='books-by-date'),
    path('admin/', admin.site.urls),
]
