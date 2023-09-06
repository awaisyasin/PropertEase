from django.db import models
from accounts.models import CustomUser
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.validators import MaxValueValidator

fs = FileSystemStorage(location=settings.MEDIA_ROOT)

# Create your models here.

class PropertyCategory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Property Categories"


class Property(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField()
    description = models.TextField()
    property_type = models.ForeignKey(PropertyCategory, on_delete=models.SET_NULL, null=True)
    property_location = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    square_footage = models.PositiveIntegerField()
    amenities = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="properties", editable=False)
    def __str__(self):
        return f"{self.title} (Owner:  {self.owner.username})"
    class Meta:
        verbose_name_plural = "Properties"


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews")
    review_text = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Review for {self.property.title} by {self.user.username}"
    class Meta:
        verbose_name_plural = "Reviews"


class Thread(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField(max_length=1000)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="threads")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title


class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=256)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content


class Message(models.Model):
    content = models.CharField(max_length=256)
    user1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user1_messages", null=True)
    user2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user2_messages", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Message from {self.user1} to {self.user2}"


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    followee = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.follower} following {self.followee}"