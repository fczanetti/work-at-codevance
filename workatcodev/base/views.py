from django.shortcuts import render


def denied_access(request):
    return render(request, 'base/denied_access.html')
