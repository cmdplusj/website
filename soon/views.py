from django.shortcuts import render

# Create your views here.

def soon_home(request):
    return render(request, 'soon/soon_home.html')
