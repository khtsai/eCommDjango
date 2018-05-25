from django.contrib import admin
from .models import Tag

# Register your models here.
class TagAdmin(admin.ModelAdmin):
    list_display = ['__str__','slug']
    class Meta:
        model = Tag

admin.site.register(Tag)