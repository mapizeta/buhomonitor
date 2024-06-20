from django.shortcuts import render

def view_logs(request):
    return render(request, 'view_logs.html')
