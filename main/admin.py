from django.contrib import admin
from main.models import Store, StoreStatus, StoreHours

admin.site.register([Store, StoreStatus, StoreHours])

# Register your models here.
