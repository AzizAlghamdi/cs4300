from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Movie, Seat, Booking
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer

# Create your views here.

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    # Regular Django view for template
    def movie_list(request):
        movies = Movie.objects.all()
        return render(request, 'bookings/movie_list.html', {'movies': movies})

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        movie_id = request.query_params.get('movie_id')
        if not movie_id:
            return Response({"error": "movie_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Find seats that are not booked for this movie
        booked_seats = Booking.objects.filter(movie_id=movie_id).values_list('seat_id', flat=True)
        available_seats = Seat.objects.exclude(id__in=booked_seats)
        serializer = self.get_serializer(available_seats, many=True)
        return Response(serializer.data)
    
    # Regular Django view for template
    def seat_booking(request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        booked_seats = Booking.objects.filter(movie=movie).values_list('seat_id', flat=True)
        available_seats = Seat.objects.exclude(id__in=booked_seats)
        return render(request, 'bookings/seat_booking.html', {
            'movie': movie,
            'available_seats': available_seats
        })

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        # Return only the current user's bookings
        user = self.request.user
        return Booking.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        movie_id = request.data.get('movie_id')
        seat_id = request.data.get('seat_id')
        
        # Check if movie and seat exist
        movie = get_object_or_404(Movie, id=movie_id)
        seat = get_object_or_404(Seat, id=seat_id)
        
        # Check if seat is already booked for this movie
        if Booking.objects.filter(movie=movie, seat=seat).exists():
            return Response({"error": "This seat is already booked for this movie"}, 
                           status=status.HTTP_400_BAD_REQUEST)
        
        # Create booking
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # Regular Django view for template
    def booking_history(request):
        bookings = Booking.objects.filter(user=request.user)
        return render(request, 'bookings/booking_history.html', {'bookings': bookings})
    
    def process_booking(request, movie_id):
        if request.method == 'POST':
            movie = get_object_or_404(Movie, id=movie_id)
            seat_id = request.POST.get('seat_id')
            seat = get_object_or_404(Seat, id=seat_id)
            
            # Check if seat is already booked
            if Booking.objects.filter(movie=movie, seat=seat).exists():
                return render(request, 'bookings/booking_error.html', {
                    'error': 'This seat is already booked'
                })
            
            # Create new booking
            booking = Booking.objects.create(
                user=request.user,
                movie=movie,
                seat=seat
            )
            
            return render(request, 'bookings/booking_confirmation.html', {
                'booking': booking
            })