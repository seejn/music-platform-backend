from django.shortcuts import render

def custom_404(request, exception):
    return render(request, 'error.html', status=404)


