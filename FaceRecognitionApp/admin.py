from django.contrib import admin
from .models import people, detection

# Register your models here.
class people_admin(admin.ModelAdmin):
  list_display = ("name","encoding")
admin.site.register(people,people_admin)

class detection_admin(admin.ModelAdmin):
  list_display = ("name","date","time")
admin.site.register(detection,detection_admin)