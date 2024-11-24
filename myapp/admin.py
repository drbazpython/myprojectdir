from django.contrib import admin
from .models import Spot, WindCondition, Review

# Register your models here.
@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at', 'updated_at')
    search_fields = ('name', 'location', 'description')
    list_filter = ('created_at', 'updated_at')

@admin.register(WindCondition)
class WindConditionAdmin(admin.ModelAdmin):
    list_display = ('spot', 'date', 'wind_speed', 'wind_direction', 'temperature')
    list_filter = ('date', 'wind_direction', 'spot')
    search_fields = ('spot__name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('spot', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'spot')
    search_fields = ('spot__name', 'user__username', 'comment')
