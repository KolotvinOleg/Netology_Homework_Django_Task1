from django.contrib import admin
from .models import Article, Tag, Scope
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main') == True:
                count+=1
        if not count:
            raise ValidationError('Укажите основной раздел')
        if count > 1:
            raise ValidationError('Основным может быть только 1 раздел')
        return super().clean()

class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text']
    list_editable = ['text']
    inlines = [ScopeInline,]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
