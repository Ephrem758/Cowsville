from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def tables(request):
    return render(request, 'tables.html')

def billing(request):
    return render(request, 'billing.html')

def virtual_reality(request):
    return render(request, 'virtual-reality.html')

def rtl(request):
    return render(request, 'rtl.html')

def notifications(request):
    return render(request, 'notifications.html')

def profile(request):
    return render(request, 'profile.html')

def sign_in(request):
    return render(request, 'sign-in.html')

def sign_up(request):
    return render(request, 'sign-up.html')


# def search_view(request):
#     query = request.GET.get('q')  # Get the search input
#     # For now, we're not filtering anything, but you can store the query for later use
#     context = {
#         'query': query,
#         'total_sales': 10000,  # Example existing data
#         'growth_rate': 12,     # Example existing data
#         # Add all other existing context data here
#     }

    return render(request, 'your_template.html', context)