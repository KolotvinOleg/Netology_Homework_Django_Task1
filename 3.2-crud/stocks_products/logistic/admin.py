from django.contrib import admin
from .models import Product, Stock, StockProduct


# Register your models here.

class StockInline(admin.TabularInline):
    model = StockProduct
    extra = 0
    verbose_name = 'Продукт'
    verbose_name_plural = 'Продукты'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    list_editable = ['description']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['address']
    inlines = [StockInline, ]
