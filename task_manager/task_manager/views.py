from django.shortcuts import render
from django.templatetags.static import static

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
    return render(request, 'auth/register.html', context)