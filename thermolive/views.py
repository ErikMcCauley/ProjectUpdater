from django.shortcuts import render, redirect

def home_page(request):
    if request.method == "GET":
        return redirect('login_page:login')
    return redirect('login_page:login')
