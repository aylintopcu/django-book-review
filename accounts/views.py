from bookcatalog.models import Reader, ReadingList, FriendsList
from django import forms
from django.shortcuts import redirect, render
from django.views import View
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
# Create your views here.


class SignUpView(View):
    def get(self, request):
        form = SignUpForm()
        context = {'sign_up_form': form}
        return render(request, 'accounts/signup.html', context)

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            reader = Reader(user=user)
            reader.save()
            want_to_read = ReadingList(list_name='Want to Read', created_by=reader)
            want_to_read.save()
            currently_reading = ReadingList(list_name='Currently Reading', created_by=reader)
            currently_reading.save()
            read = ReadingList(list_name='Read', created_by=reader)
            read.save()
            friends_list = FriendsList(reader=reader)
            friends_list.save()
            login(request, user)
            return redirect('bookcatalog:index')

        else:
            context = {'sign_up_form': form}
            return render(request, 'accounts/signup.html', context)


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        context = {'login_form': form}
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')

        else:
            context = {'login_form': form}
            return render(request, 'accounts/login.html', context)
