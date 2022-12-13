from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from djangoFinal.blog import views
from djangoFinal.blog.views import signup, login_page, logout_page, contact_view, thank_you, NotFoundView, TCView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='aboutus'),  # The CKEditor path
    path('blog/', include('djangoFinal.blog.urls')),
    path('signup/', signup, name='signup_page'),
    path('login/', login_page, name="login_page"),
    path('logout/', logout_page, name="logout_page"),
    path('contact/', contact_view, name="contact_page"),
    path('thank-you/', thank_you, name="thank_you"),
    path('terms-and-conditions/', TCView.as_view(), name="terms and conditions"),
]

urlpatterns += staticfiles_urlpatterns()
handler404 = NotFoundView.as_view()  # NotFoundView.as_view()
