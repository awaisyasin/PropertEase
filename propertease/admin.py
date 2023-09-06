from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Property)
admin.site.register(PropertyCategory)
# admin.site.register(PropertyLocation)
# admin.site.register(PropertyAgent)
# admin.site.register(Image)
admin.site.register(Review)
admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Follow)