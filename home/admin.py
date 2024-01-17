from django.contrib import admin

from home.models import Person

# Register your models here.
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'username', 'birth_date', 'gender']
    list_display_links = ['full_name', 'username']
    list_filter = ['gender']
    
    def full_name(self, obj):
        return obj.user.get_full_name()
    
    def username(self, obj):
        return obj.user
    