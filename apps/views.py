from django.shortcuts import render, get_object_or_404  # Import render function from Django
from rest_framework import status  # Import status codes from Django REST Framework
from rest_framework.response import Response  # Import Response class from Django REST Framework
from rest_framework import viewsets  # Import viewsets from Django REST Framework
from .models import Coin  # Import the Coin model
from .serializers import CoinSerializer  # Import the CoinSerializer
from rest_framework.views import APIView
import re

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

def coins_table(request):
    # Retrieve data from the Coin model
    coins = Coin.objects.all()

    # Render the HTML template and pass the data to it
    return render(request, 'coins_table.html', {'coins': coins})
def coin_details(request, coin_id):
    # Retrieve the coin object with the specified ID
    coin = get_object_or_404(Coin, pk=coin_id)

    # Render the HTML template for coin details and pass the coin object to it
    return render(request, 'coin_details.html', {'coin': coin})