from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext

import http

from django.views.generic import TemplateView

from . import models
from .forms import EmailForm, CommentForm, ContactForm, SignupForm, LoginForm


# Create your views here.

def display_blog(request):
    pass


def display_blog_post(request, post):
    post = get_object_or_404(models.Post, slug=post,
                             status='published')

    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post=post.slug)
    else:
        form = EmailForm()
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    form_comment = CommentForm()
    tags = [str(tag) for tag in post.tags.all()]
    new_comment = None

    profile_image = str(post.author.profile_image).split("staticfiles")
    prof_image = profile_image[1] if len(profile_image) >= 2 else ""
    date_human = post.publish.strftime("%Y-%m-%d")

    return render(request,
                  'single.html',
                  {'post': post,
                   'author': post.author,
                   'prof_image': prof_image,
                   'post_image': post.post_image,
                   'comments': comments,
                   'comments_len': len(comments),
                   'date_human': date_human,
                   'form': form,
                   'form_comment': form_comment,
                   'tags': tags,
                   'new_comment': new_comment})


def create_comment(request, post):
    if request.method == 'POST':
        form_comment = CommentForm(request.POST)
        print("fORM_COMMENT", form_comment.data['body'])
        if form_comment.is_valid():
            post = models.Post.objects.get(slug=post)
            author = models.Profile.objects.get(user=request.user)
            comment = models.Comment.objects.create(post=post, author=author, body=form_comment.data['body'])

            return redirect('post_detail', post=post.slug)
    else:
        form_comment = CommentForm()


# TODO make form send real emails
def contact_view(request):
    if request.method == 'POST':

        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            # email_subject = f'New contact {contact_form.cleaned_data["email"]}: {contact_form.cleaned_data["subject"]}'
            # email_message = contact_form.cleaned_data['message']
            contact_form.save()

            return redirect("thank_you")
    else:
        contact_form = ContactForm()

    context = {'form': contact_form}

    return render(request, 'contact.html', context)


def blog_index(request):
    pass


def signup(request):
    context = {'form': SignupForm, 'error': False}
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        print("signuP:", signup_form.errors.as_data())
        if signup_form.is_valid():
            signup_form.save()
            return redirect('post_detail', post="test")
        else:
            context["error"] = True
            error_message = str()
            for k, v in signup_form.errors.as_data().items():
                for err in v:
                    error_message += str(err).strip('[]\'')
            context["error_message"] = error_message
    else:
        signup_form = SignupForm()

    return render(request, 'signup.html', context)


def thank_you(request):
    return render(request, 'thank-you.html')


def login_page(request):
    # print("Executing login page")
    context = {'form': LoginForm, 'error': False}

    if request.method == 'POST':
        login_form = LoginForm(request=request.POST)
        # print("test", login_form.errors.as_data(), login_form.is_valid(), login_form.error_messages, login_form.errors)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            context["error"] = False
            login(request, user)

            return redirect('post_detail', post="test")
        else:
            context["error"] = True
            context["error_message"] = "Invalid credentials"

    else:
        login_form = LoginForm()

    return render(request, 'login.html', context)


def logout_page(request):
    logout(request)
    return redirect('post_detail', post="test")


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = models.Post.objects.all().order_by('-id')[:3]
        post_images = []

        for p in posts:
            if "staticfiles" in str(p.post_image):
                postimg = str(p.post_image).split("staticfiles")
                post_images.append(postimg[1] if len(postimg) >= 2 else "")
            else:
                post_images.append("/" + str(p.post_image))
        context["posts"] = zip(posts, post_images)
        context["first_post_slug"] = posts[0].slug

        context["testimonials"] = models.Testimonial.objects.all()
        context["author_images"] = []

        for t in context["testimonials"]:
            test = models.Profile.objects.get(user=t.user)

            if "staticfiles" in str(test.profile_image):
                postimg = str(test.profile_image).split("staticfiles")
                context["author_images"].append(postimg[1] if len(postimg) >= 2 else "")
            else:
                context["author_images"].append("/" + str(test.profile_image))

        print(context["author_images"])
        context["objects"] = zip(context["testimonials"], context["author_images"])

        return context


class BlogView(TemplateView):
    template_name = 'blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        body = get_object_or_404(models.AboutUsContent)
        context["body"] = body

        return context


class TCView(TemplateView):
    template_name = 'term-conditions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        body = get_object_or_404(models.TCContent)
        context["body"] = body

        return context


# def handler404(request, *args, **argv):
#     response = render('error-404.html', {})
#     response.status_code = 404
#     return response


class NotFoundView(TemplateView):
    template_name = 'error-404.html'

    @classmethod
    def get_rendered_view(cls):
        as_view_fn = cls.as_view()

        def view_fn(request):
            response = as_view_fn(request)
            response.render()
            return response

        return view_fn
