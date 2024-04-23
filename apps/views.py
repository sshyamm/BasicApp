from django.shortcuts import render, redirect, get_object_or_404  # Import render function from Django
from django.urls import reverse
from rest_framework import status  # Import status codes from Django REST Framework
from rest_framework.response import Response  # Import Response class from Django REST Framework
from rest_framework import viewsets  # Import viewsets from Django REST Framework
from .models import Coin, Profile, SearchHistory  # Import the Coin model
from .serializers import CoinSerializer  # Import the CoinSerializer
from rest_framework.views import APIView
import re
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from .forms import ProfileForm, CoinForm
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CoinViewSet(viewsets.ModelViewSet):  # Define a viewset for the Coin model
    queryset = Coin.objects.all()  # Define the queryset to fetch all coin objects
    serializer_class = CoinSerializer  # Specify the serializer class to use for the Coin model


class CoinSearchView(APIView):
    def get(self, request, *args, **kwargs):
        # Extract search parameters from the URL path
        path_params = kwargs.get('path_params')
        
        # Parse the path_params string into field-value pairs
        search_params = {}
        if path_params:
            # Split the path_params string by '/'
            path_params_list = path_params.split('/')
            
            # Ensure there are an even number of elements (field-value pairs)
            if len(path_params_list) % 2 == 0:
                for i in range(0, len(path_params_list), 2):
                    search_params[path_params_list[i]] = path_params_list[i+1]

        # Filter Coin objects based on the provided search parameters
        coins = Coin.objects.all()
        for field, value in search_params.items():
            coins = coins.filter(**{field: value})

        if not coins:
            return Response({"message": "No coins found for the provided search parameters"}, status=404)

        # Serialize the filtered queryset
        serializer = CoinSerializer(coins, many=True, context={'request': request})
        return Response(serializer.data)

@login_required
def coins_table(request):
    # Retrieve data from the Coin model
    coins = Coin.objects.all()

    # Render the HTML template and pass the data to it
    return render(request, 'coins_table.html', {'coins': coins})

@login_required
def coin_details(request, coin_id):
    # Retrieve the coin object with the specified ID
    coin = get_object_or_404(Coin, pk=coin_id)

    # Render the HTML template for coin details and pass the coin object to it
    return render(request, 'coin_details.html', {'coin': coin})

def home(request):
    if request.user.is_authenticated:
        search_params = {}
        coins_list = Coin.objects.all().order_by('-coin_id')

        if request.method == 'POST':
            # Handle search functionality and store search history
            for key in request.POST:
                if key != 'csrfmiddlewaretoken':
                    value = request.POST[key]
                    if value:
                        search_params[key] = value
                        # Save search history to the database
                        SearchHistory.objects.create(user=request.user, search_text=f'{key.capitalize()}: {value}')

            # Filter coins based on search parameters
            for key, value in search_params.items():
                coins_list = coins_list.filter(**{key: value})

        paginator = Paginator(coins_list, 10)  # Change 10 to the desired number of items per page

        page = request.GET.get('page')
        try:
            coins = paginator.page(page)
        except PageNotAnInteger:
            coins = paginator.page(1)
        except EmptyPage:
            coins = paginator.page(paginator.num_pages)

        # Retrieve search history for the current user
        search_history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')

        return render(request, 'home.html', {'coins': coins, 'search_history': search_history})
    else:
        return render(request, 'home.html', {})



@login_required
def clear_search_history(request, search_history_id):
    # Retrieve the search history item to delete
    search_history_item = get_object_or_404(SearchHistory, pk=search_history_id)

    # Check if the search history item belongs to the current user
    if search_history_item.user == request.user:
        # Delete the search history item
        search_history_item.delete()
        messages.success(request, 'Search history item deleted successfully!')
    else:
        messages.error(request, 'You do not have permission to delete this search history item.')

    # Redirect back to the home page or any other desired page
    return redirect('apps:home')

@login_required
def create_coin(request):
    if request.method == 'POST':
        form = CoinForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the logged-in user
            logged_in_user = request.user

            # Assign the logged-in user's ID to the created_by_id field of the coin
            coin = form.save(commit=False)
            coin.created_by_id = logged_in_user.id
            coin.save()

            messages.success(request, 'Coin created successfully!')
            return redirect(reverse("apps:home"))
    else:
        form = CoinForm()
    return render(request, 'create_coin.html', {'form': form})

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect(reverse("apps:login")) 
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
    
@login_required
def view_profile(request):
    profile = Profile.objects.get_or_create(user=request.user)[0]
    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = Profile.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect(reverse('apps:view_profile'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def custom_password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect(reverse('apps:password_change_done'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change-password.html', {'form': form})

@login_required
def custom_password_change_done(request):
    return render(request, 'registration/password-done.html')



