from django.shortcuts import render


def home(request):
    return render(request, 'product/home.html', {'user': request.user})


def profile(request):
    return render(request, 'product/profile.html')

