from django.db import models
from django.contrib.auth.models import User

class Coin(models.Model):
    # Define choices for coin status
    STATUS_CHOICES = (
        ('Select', 'Select'),  # Placeholder option
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('pending', 'Pending'),
    )

    coin_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    coin_image = models.ImageField(upload_to='coin_images/', null=True, blank=True)   # Image field to store coin image
    coin_name = models.CharField(max_length=100)  # Char field for coin name
    coin_desc = models.TextField()  # Text field for coin description
    coin_year = models.IntegerField()  # Integer field for coin year
    coin_country = models.CharField(max_length=50)  # Char field for coin country
    coin_material = models.CharField(max_length=50)  # Char field for coin material
    coin_weight = models.FloatField()  # Float field for coin weight
    starting_bid = models.FloatField()  # Float field for starting bid
    coin_status = models.CharField(max_length=50, choices=STATUS_CHOICES)  # Char field with choices for coin status

    def __str__(self):
        return self.coin_name  # Return the coin name as its string representation

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username  # Return the username as the string representation
