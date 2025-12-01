from django.shortcuts import render, redirect
from django.templatetags.static import static
from django.contrib.auth import authenticate, login

from administration.forms.create_user_form import CreateUserForm
import re

def index(request):
    links = [
        {
            'to': "/#features",
            'label': "Features",
        },
        {
            'to': "/#solution",
            'label': "Solution",
        },
        {
            'to': "/#reviews",
            'label': "Reviews",
        },
    ]
    context = {
        "microsoft": static("img/clients/microsoft.svg"),
        "airbnb": static("img/clients/airbnb.svg"),
        "google": static("img/clients/google.svg"),
        "ge": static("img/clients/ge.svg"),
        "netflix": static("img/clients/netflix.svg"),
        "google_cloud":static("img/clients/google-cloud.svg"),
        "pie": static("img/pie.svg"),
        "avatars": {
            "avatar_1": static("img/avatars/avatar-1.webp"),
            "avatar_2": static("img/avatars/avatar-2.webp"),
            "avatar_3": static("img/avatars/avatar-3.webp"),
            "avatar_4": static("img/avatars/avatar-4.webp"),
            "avatar": static("img/avatars/avatar.webp"),
        },
        "links": links,
        "style_css": static("css/globals.css"),
    }
    return render(request, 'home/index.html', context)

def auth_register(request):
    context = {
        "style_css": static("css/globals.css"),
        "shinobu": static("img/Shinobu.jpg"),
    }

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            context['success_message'] = "User registered successfully."
        else:
            context['error_message'] = "There were errors in the form."
            context['form_errors'] = form.errors
    else:
        form = CreateUserForm()
    context['form'] = form
    return render(request, 'auth/register.html', context)


def auth_login(request):
    context = {
        "style_css": static("css/globals.css"),
        "shinobu": static("img/Shinobu.jpg"),
    }
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # if username is email, get the username associated with that email
        # verifi using regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, username):
            from administration.models import User
            try:
                user_obj = User.objects.get(email=username)
                username = user_obj.username
            except User.DoesNotExist:
                context['error_message'] = "Invalid email or password. Please try again."
                return render(request, 'auth/login.html', context)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('administration:dashboard')
        else:
            context['error_message'] = "Invalid username or password. Please try again."

    return render(request, 'auth/login.html', context)