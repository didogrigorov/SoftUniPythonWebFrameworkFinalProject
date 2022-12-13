from django.urls import path, include

from djangoFinal.blog import views
from djangoFinal.blog.views import display_blog, display_blog_post, create_comment, signup, contact_view, thank_you, \
    login_page, logout_page

urlpatterns = [
    # path(r'^post/', views.display_blog, name='post_index')
    # path('/', views.display_blog_post, name='post_detail')
    # path('', display_blog, name='post_list'),
    # path('tag/<slug:tag_slug>/', display_blog_post, name='post_list_by_tag'),

    path('<slug:post>/', display_blog_post, name='post_detail'),
    path('create-comment/<slug:post>/', create_comment, name='create_comment'),

]