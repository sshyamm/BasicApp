from rest_framework import serializers  # Import serializers from Django REST Framework
from .models import Coin  # Import the Coin model

class CoinSerializer(serializers.ModelSerializer):  # Define a serializer for the Coin model
    # Define a HyperlinkedIdentityField for generating hyperlinks to individual coin details
    view_details = serializers.HyperlinkedIdentityField(view_name='coin-detail', lookup_field='pk')

    class Meta:
        model = Coin  # Specify the Coin model to serialize
        fields = ['coin_id', 'coin_image', 'coin_name', 'coin_desc', 'coin_year', 'coin_country', 'coin_material', 'coin_weight', 'starting_bid', 'coin_status', 'view_details']  # Define the fields to include in the serialized representation

    # Validate uniqueness of coin_name field
    def validate_coin_name(self, value):
        existing_coins = Coin.objects.filter(coin_name=value)
        if self.instance:  # Exclude current instance for update operation
            existing_coins = existing_coins.exclude(pk=self.instance.pk)
        if existing_coins.exists():
            raise serializers.ValidationError("Coin name must be unique.")
        return value

    # Validate uniqueness of coin_country field
    def validate_coin_country(self, value):
        existing_coins = Coin.objects.filter(coin_country=value)
        if self.instance:
            existing_coins = existing_coins.exclude(pk=self.instance.pk)
        if existing_coins.exists():
            raise serializers.ValidationError("Coin country must be unique.")
        return value

    # Validate uniqueness of coin_year field
    def validate_coin_year(self, value):
        existing_coins = Coin.objects.filter(coin_year=value)
        if self.instance:
            existing_coins = existing_coins.exclude(pk=self.instance.pk)
        if existing_coins.exists():
            raise serializers.ValidationError("Coin year must be unique.")
        return value

    # Validate uniqueness of coin_material field
    def validate_coin_material(self, value):
        existing_coins = Coin.objects.filter(coin_material=value)
        if self.instance:
            existing_coins = existing_coins.exclude(pk=self.instance.pk)
        if existing_coins.exists():
            raise serializers.ValidationError("Coin material must be unique.")
        return value

    # Validate uniqueness of coin_weight field
    def validate_coin_weight(self, value):
        existing_coins = Coin.objects.filter(coin_weight=value)
        if self.instance:
            existing_coins = existing_coins.exclude(pk=self.instance.pk)
        if existing_coins.exists():
            raise serializers.ValidationError("Coin weight must be unique.")
        return value
        
        # Validate coin_status field
    def validate_coin_status(self, value):
        if value == 'Select':
            raise serializers.ValidationError("Please select a valid coin status.")
        return value

