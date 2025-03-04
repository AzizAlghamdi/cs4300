from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Set up DRF router
router = DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'seats', views.SeatViewSet)
router.register(r'bookings', views.BookingViewSet, basename='booking')

# URL patterns
urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Template views
    path('', views.MovieViewSet.movie_list, name='movie_list'),
    path('book-seat/<int:movie_id>/', views.SeatViewSet.seat_booking, name='book_seat'),
    path('process-booking/<int:movie_id>/', views.BookingViewSet.process_booking, name='process_booking'),
    path('booking-history/', views.BookingViewSet.booking_history, name='booking_history'),
]