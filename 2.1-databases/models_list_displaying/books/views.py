from django.shortcuts import render, get_object_or_404
from .models import Book
from django.core.paginator import Paginator

def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.order_by('pub_date')
    # for book in books:
    #     book.save()
    context = {'books': books}
    return render(request, template, context)


def get_info_about_books_by_date(request, pub_date: str):
    books = Book.objects.filter(pub_date=pub_date)
    context = {'books': books}
    left_page = Book.objects.filter(pub_date__lt=pub_date).values('pub_date').first()
    right_page = Book.objects.filter(pub_date__gt=pub_date).values('pub_date').first()
    if left_page:
        context['left_page'] = left_page['pub_date']
    if right_page:
        context['right_page'] = right_page['pub_date']
    return render(request, 'books/book_by_date.html', context=context)


def get_info_about_book(request, name_book):
    book = get_object_or_404(Book, slug=name_book)
    context = {'book': book}
    return render(request, 'books/one_book.html', context=context)

