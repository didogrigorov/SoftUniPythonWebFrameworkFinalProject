import os

from django.contrib import admin

from django import forms
from ckeditor.widgets import CKEditorWidget
from pathlib import Path
from . import models

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# class PostAdminForm(forms.ModelForm):
#     body = forms.CharField(widget=CKEditorWidget())
#     class Meta:
#         model = models.Post
#         fields = '__all__'
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'body', 'status', 'tag_list', 'publish']
    list_filter = ('status', 'created', 'body', 'publish', 'author', 'tags')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

    # body = PostAdminForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.prefetch_related('tags')
        else:
            author = models.Author.objects.filter(user=request.user).first()
            print("author:", author)
            return qs.filter(author=author)

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    class Media:
        js = ('/assets/ckeditor/ckeditor/ckeditor.js',)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created', 'active', 'body')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(models.Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'created')
    list_filter = ('user', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Category)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NewsletterEmail)
class Newsletter(admin.ModelAdmin):
    list_display = ['email']


@admin.register(models.Contact)
class Contact(admin.ModelAdmin):
    list_display = ['name', 'email', 'company', 'phone_number', 'message']


@admin.register(models.AboutUsContent)
class AboutPage(admin.ModelAdmin):
    list_display = ['about_body']


@admin.register(models.TCContent)
class TCPage(admin.ModelAdmin):
    list_display = ['tc_body']
