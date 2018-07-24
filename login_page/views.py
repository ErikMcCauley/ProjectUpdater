from django.shortcuts import render
from .models import projects


def login_view(request):
    return render(request, 'login_page/login.html')


def display(request):
    if request.method == 'POST':
        project = projects.objects.all()
        tester = request.POST['code']
        if projects.objects.filter(projectCode=tester):
            project = projects.objects.filter(projectCode=tester)
        else:
            project = {'projectCode': "No Such Projects"}
        return render(request, 'login_page/display.html', {'display': project})
    elif request.method == 'GET':
        return render(request, 'login_page/login.html')


