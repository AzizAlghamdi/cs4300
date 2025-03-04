from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date
from .models import Movie, Seat, Booking

# Create your tests here.

class ModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create a test movie
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='This is a test movie description',
            release_date=date(2023, 1, 1),
            duration=120
        )
        
        # Create a test seat
        self.seat = Seat.objects.create(
            seat_number='A1',
            is_available=True
        )
    
    def test_movie_creation(self):
        """Test that a movie is created correctly"""
        self.assertEqual(self.movie.title, 'Test Movie')
        self.assertEqual(self.movie.duration, 120)
    
    def test_seat_creation(self):
        """Test that a seat is created correctly"""
        self.assertEqual(self.seat.seat_number, 'A1')
        self.assertTrue(self.seat.is_available)
    
    def test_booking_creation(self):
        """Test that a booking is created correctly"""
        booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )
        self.assertEqual(booking.movie, self.movie)
        self.assertEqual(booking.seat, self.seat)
        self.assertEqual(booking.user, self.user)


class APITests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create a test movie
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='This is a test movie description',
            release_date=date(2023, 1, 1),
            duration=120
        )
        
        # Create test seats
        self.seat1 = Seat.objects.create(seat_number='A1', is_available=True)
        self.seat2 = Seat.objects.create(seat_number='A2', is_available=True)
        
        # Set up the API client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_get_movies(self):
        """Test retrieving movies list via API"""
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Movie')
    
    def test_get_seats(self):
        """Test retrieving seats list via API"""
        response = self.client.get(reverse('seat-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_create_booking(self):
        """Test creating a booking via API"""
        data = {
            'movie_id': self.movie.id,
            'seat_id': self.seat1.id
        }
        response = self.client.post(reverse('booking-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that the booking was created in the database
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.movie, self.movie)
        self.assertEqual(booking.seat, self.seat1)
        self.assertEqual(booking.user, self.user)
    
    def test_double_booking_error(self):
        """Test that booking the same seat twice produces an error"""
        # Create the first booking
        Booking.objects.create(
            movie=self.movie,
            seat=self.seat1,
            user=self.user
        )
        
        # Try to create a second booking for the same seat
        data = {
            'movie_id': self.movie.id,
            'seat_id': self.seat1.id
        }
        response = self.client.post(reverse('booking-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Check that only one booking exists
        self.assertEqual(Booking.objects.count(), 1)


class ViewTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.force_login(self.user)
        
        # Create test movies
        self.movie1 = Movie.objects.create(
            title='Test Movie 1',
            description='Description 1',
            release_date=date(2023, 1, 1),
            duration=120
        )
        self.movie2 = Movie.objects.create(
            title='Test Movie 2',
            description='Description 2',
            release_date=date(2023, 2, 1),
            duration=90
        )
        
        # Create test seats
        self.seat1 = Seat.objects.create(seat_number='A1', is_available=True)
        self.seat2 = Seat.objects.create(seat_number='A2', is_available=True)
    
    def test_movie_list_view(self):
        """Test the movie list view"""
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/movie_list.html')
        self.assertContains(response, 'Test Movie 1')
        self.assertContains(response, 'Test Movie 2')
    
    def test_seat_booking_view(self):
        """Test the seat booking view"""
        response = self.client.get(reverse('book_seat', args=[self.movie1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/seat_booking.html')
        self.assertContains(response, 'Test Movie 1')
        self.assertContains(response, 'A1')
        self.assertContains(response, 'A2')
    
    def test_booking_process(self):
        """Test the booking process"""
        data = {
            'seat_id': self.seat1.id
        }
        response = self.client.post(reverse('process_booking', args=[self.movie1.id]), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_confirmation.html')
        
        # Check booking was created
        booking = Booking.objects.first()
        self.assertEqual(booking.movie, self.movie1)
        self.assertEqual(booking.seat, self.seat1)
        self.assertEqual(booking.user, self.user)
    
    def test_booking_history_view(self):
        """Test the booking history view"""
        # Create a booking
        booking = Booking.objects.create(
            movie=self.movie1,
            seat=self.seat1,
            user=self.user
        )
        
        response = self.client.get(reverse('booking_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_history.html')
        self.assertContains(response, 'Test Movie 1')
        self.assertContains(response, 'A1')