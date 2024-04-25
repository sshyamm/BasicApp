"""
URL configuration for BasicProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from apps.views import CoinViewSet, CoinSearchView, coins_table, coin_details, edit_coin

# Create a router for registering viewsets
router = routers.DefaultRouter()

# Register CoinViewSet with the router
router.register(r'coins', CoinViewSet)

# Define URL patterns
urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),
    # API endpoints for coins using the router
    path('api/', include(router.urls)),
    path('coins/search/<path:path_params>/', CoinSearchView.as_view(), name='coin-search'),
    path('coins/', coins_table, name='coins-table'),  # URL for the coins table HTML page
    path('coin/<int:coin_id>/', coin_details, name='coin-details'),  # URL for the coin details page
    path('edit-coin/<int:coin_id>/', edit_coin, name='edit_coin'),
    path("", include(("apps.urls", "apps"), "apps")),
] 
# Serve media files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


