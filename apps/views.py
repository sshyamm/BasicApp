from django.shortcuts import render, redirect, get_object_or_404  # Import render function from Django
from django.urls import reverse
from rest_framework import status  # Import status codes from Django REST Framework
from rest_framework.response import Response  # Import Response class from Django REST Framework
from rest_framework import viewsets  # Import viewsets from Django REST Framework
from .models import Coin, Profile, SearchHistory, CartItem  # Import the Coin model
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

@login_required
def save_changes(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                item_id = int(key.split('_')[1])
                quantity = int(value)
                cart_item = CartItem.objects.get(pk=item_id)
                cart_item.quantity = quantity
                cart_item.price = cart_item.coin.rate * quantity
                cart_item.save()
        messages.success(request, 'Changes saved successfully!')
        return redirect('cart')  # Assuming 'cart' is the name of the URL pattern for the cart page
    else:
        # Handle GET request (if needed)
        pass

@login_required
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    messages.success(request, 'Item removed successfully!')
    return redirect('cart')

@login_required
def cart(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    # Calculate total price
    total_price = sum(item.quantity * item.coin.rate for item in cart_items)

    for item in cart_items:
        item.price = item.quantity * item.coin.rate
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, coin_id):
    if request.method == 'POST':
        # Get the selected coin
        coin = Coin.objects.get(pk=coin_id)
        # Get the current user
        user = request.user
        # Create a CartItem object
        cart_item = CartItem.objects.create(user=user, coin=coin)
        # Redirect to the cart page
        messages.success(request, 'Your item added to the cart!')
        return redirect('cart')
    else:
        # Handle GET request (if needed)
        pass


@login_required
def edit_coin(request, coin_id):
    coin = get_object_or_404(Coin, pk=coin_id)

    if request.user.id != coin.created_by_id:
        return redirect('apps:home')

    if request.method == 'POST':
        form = CoinForm(request.POST, request.FILES, instance=coin)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coin updated successfully!')
            return redirect(reverse('coin-details', kwargs={'coin_id': coin_id}))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CoinForm(instance=coin)
    
    return render(request, 'edit_coin.html', {'form': form, 'coin': coin})

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

from django.db import models

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
                        # Get the field object from the Coin model
                        field_object = Coin._meta.get_field(key)
                        # Check if the field is an integer or number field
                        if isinstance(field_object, (models.IntegerField, models.DecimalField, models.FloatField)):
                            try:
                                # Convert the value to the appropriate type
                                value = field_object.to_python(value)
                                # For integer and number fields, perform exact match
                                search_params[key] = value
                            except ValueError:
                                # Handle the case where the value cannot be converted to the appropriate type
                                messages.error(request, f'Invalid value for {key}. Please enter a valid number.')
                                return redirect('apps:home')
                        else:
                            # Use __icontains for partial matching for non-integer fields
                            search_params[key + '__icontains'] = value
                        
                        # Save search history to the database
                        SearchHistory.objects.create(user=request.user, search_text=f'{key.capitalize()}: {value}')

            # Filter coins based on search parameters
            coins_list = coins_list.filter(**search_params)

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
            return redirect(reverse('coin-details', kwargs={'coin_id': coin.pk}))
    else:
        form = CoinForm()
    return render(request, 'create_coin.html', {'form': form})

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!. Please login with your credentials.')
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



