from django.contrib import admin
from .models import Movie, Seat, Booking

# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'duration')
    search_fields = ('title', 'description')
    list_filter = ('release_date',)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('seat_number',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'seat', 'booking_date')
    list_filter = ('booking_date', 'movie')
    search_fields = ('user__username', 'movie__title', 'seat__seat_number')
    date_hierarchy = 'booking_date'