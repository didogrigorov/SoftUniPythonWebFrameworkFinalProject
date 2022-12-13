from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login

from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form

from django.contrib.auth.models import User
from djangoFinal.blog.models import NewsletterEmail, Comment, Contact, Profile, Author


class EmailForm(forms.ModelForm):
    email = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter your email to subscribe...'}
    ), label='')

    class Meta:
        model = NewsletterEmail
        fields = ['email']


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Enter your comment here...',
               'class': 'border border-gray-200 resize-none rounded-2xl w-full max-h-[140px] p-[26px] mb-[33px]'}
    ), label='')

    class Meta:
        model = Comment
        fields = ['body']


class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter your name...',
               'class': 'outline-none flex-1 placeholder:text-gray-400 placeholder:text-md placeholder:font-chivo py-5 px-[30px]'}),
        label='')

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter your email address...',
               'class': 'outline-none flex-1 placeholder:text-gray-400 placeholder:text-md placeholder:font-chivo py-5 px-[30px]'}
    ), label='')

    company = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter your company name...(Optional)',
               'class': 'outline-none flex-1 placeholder:text-gray-400 placeholder:text-md placeholder:font-chivo py-5 px-[30px]'}
    ), label='')

    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter your phone...',
               'class': 'outline-none flex-1 placeholder:text-gray-400 placeholder:text-md placeholder:font-chivo py-5 px-[30px]'}
    ), label='')

    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Enter your message here...',
               'class': 'border border-gray-200 resize-none rounded-2xl w-full max-h-[140px] p-[26px] mb-[33px]'}
    ), label='')

    class Meta:
        model = Contact
        fields = '__all__'


class SignupForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your first name...', 'class': 'outline-none flex-1 pr-3 border caret-green-900 w-full placeholder:text-gray-400 placeholder:text-text placeholder:font-chivo border-[#C2C8D0] rounded-[4px] py-[14px] pl-[16px] pr-[12px] focus:border-green-900 focus:border-[2px]'}), min_length=5, max_length=150, label='')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your last name...', 'class': 'outline-none flex-1 pr-3 border caret-green-900 w-full placeholder:text-gray-400 placeholder:text-text placeholder:font-chivo border-[#C2C8D0] rounded-[4px] py-[14px] pl-[16px] pr-[12px] focus:border-green-900 focus:border-[2px]'}), min_length=5, max_length=150, label='')
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your username...', 'class': 'outline-none flex-1 pr-3 border caret-green-900 w-full placeholder:text-gray-400 placeholder:text-text placeholder:font-chivo border-[#C2C8D0] rounded-[4px] py-[14px] pl-[16px] pr-[12px] focus:border-green-900 focus:border-[2px]'}), min_length=5, max_length=150, label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Enter your email...','class': 'outline-none flex-1 pr-3 border caret-green-900 w-full placeholder:text-gray-400 placeholder:text-text placeholder:font-chivo border-[#C2C8D0] rounded-[4px] py-[14px] pl-[16px] pr-[12px] focus:border-green-900 focus:border-[2px]'}), label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password...', 'class': 'outline-none flex-1 pr-3 border caret-green-900 w-full placeholder:text-gray-400 placeholder:text-text placeholder:font-chivo border-[#C2C8D0] rounded-[4px] py-[14px] pl-[16px] pr-[12px] focus:border-green-900 focus:border-[2px]'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Repeat your password...', 'class': 'outline-none flex-1 pr-3 border caret-green-900 w-full placeholder:text-gray-400 placeholder:text-text placeholder:font-chivo border-[#C2C8D0] rounded-[4px] py-[14px] pl-[16px] pr-[12px] focus:border-green-900 focus:border-[2px]'}), label='')
    is_author = forms.BooleanField(label="Are you an Author?", required=False)

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):

        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            is_staff=self.cleaned_data['is_author'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )

        if self.cleaned_data['is_author']:
            return Author.objects.create(user=user)
        else:
            return Profile.objects.create(user=user)

        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'outline-none flex-1 pr-3 border caret-green-900 w-full placeholder:text-gray-400 placeholder:text-text placeholder:font-chivo border-[#C2C8D0] rounded-[4px] py-[14px] pl-[16px] pr-[12px] focus:border-green-900 focus:border-[2px]',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'outline-none flex-1 pr-3 border caret-green-900 w-full placeholder:text-gray-400 placeholder:text-text placeholder:font-chivo border-[#C2C8D0] rounded-[4px] py-[14px] pl-[16px] pr-[12px] focus:border-green-900 focus:border-[2px]',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))
    class Meta:
        model = User
        fields = ['username', 'password']
