from django.contrib import admin
from .models import Place, Review


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """
    Admin configuration for Place model.
    """
    list_display = ('name', 'address', 'get_average_rating', 'get_review_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'address')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for Review model.
    """
    list_display = ('user', 'place', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__name', 'user__phone_number', 'place__name', 'text')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user', 'place')
