from django.contrib import admin
from django.utils.html import format_html
from .models import Coin, Order, OrderItem, ShippingAddress, CartItem, SearchHistory, Profile  # Import the Coin model
from django.conf import settings  # Import Django settings module

@admin.register(Coin)  # Register the Coin model with the admin site
class CoinAdmin(admin.ModelAdmin):  # Define the admin class for Coin model
    # Specify the fields to display in the list view of the admin site
    list_display = ('coin_name', 'display_coin_image', 'coin_desc', 'coin_year', 'coin_country', 'coin_material', 'coin_weight', 'rate', 'starting_bid', 'coin_status', 'created_by_id')

    # Define a method to display the coin image in the list view
    def display_coin_image(self, obj):
        if obj.coin_image:  # Check if coin_image is not null or empty
            # Generate HTML code to display the coin image with specified width and height
            return format_html('<img src="{}" style="max-width:100px; max-height:100px;">'.format(obj.coin_image.url))
        else:
            return "Null"  # Display "Null" if coin_image is null or empty

@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'website')

@admin.register(SearchHistory)
class SearchHistory(admin.ModelAdmin):
    list_display = ('user', 'search_text', 'timestamp')

@admin.register(CartItem)
class CartItem(admin.ModelAdmin):
    list_display = ('user', 'coin', 'quantity', 'price', 'created_at')

@admin.register(Order)
class CoinOrder(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'total_amount', 'status')

@admin.register(OrderItem)
class CoinOrderItem(admin.ModelAdmin):
    list_display = ('order', 'coin', 'quantity', 'rate', 'price')

@admin.register(ShippingAddress)
class ShippingAddress(admin.ModelAdmin):
    list_display = ('user', 'order', 'address', 'city', 'state', 'postal_code')
