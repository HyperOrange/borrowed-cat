from django.shortcuts import render

def role_distribution_view(request):
    return render(request, 'role_distribution/index.html')