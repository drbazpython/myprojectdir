from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from .models import Spot, WindCondition, Review

class SpotModelTests(TestCase):
    def setUp(self):
        self.spot = Spot.objects.create(
            name='Test Spot',
            location='Test Location',
            description='Test Description',
            latitude=Decimal('20.7984'),
            longitude=Decimal('-156.3319')
        )

    def test_spot_creation(self):
        self.assertEqual(self.spot.name, 'Test Spot')
        self.assertEqual(self.spot.location, 'Test Location')
        self.assertTrue(isinstance(self.spot, Spot))
        self.assertEqual(str(self.spot), 'Test Spot')

    def test_spot_coordinates(self):
        self.assertEqual(self.spot.latitude, Decimal('20.7984'))
        self.assertEqual(self.spot.longitude, Decimal('-156.3319'))

class WindConditionModelTests(TestCase):
    def setUp(self):
        self.spot = Spot.objects.create(
            name='Test Spot',
            location='Test Location',
            description='Test Description',
            latitude=Decimal('20.7984'),
            longitude=Decimal('-156.3319')
        )
        self.condition = WindCondition.objects.create(
            spot=self.spot,
            date='2024-03-20',
            wind_speed=Decimal('15.5'),
            wind_direction='N',
            temperature=Decimal('25.0')
        )

    def test_wind_condition_creation(self):
        self.assertEqual(self.condition.wind_speed, Decimal('15.5'))
        self.assertEqual(self.condition.wind_direction, 'N')
        self.assertEqual(self.condition.temperature, Decimal('25.0'))
        self.assertTrue(isinstance(self.condition, WindCondition))

    def test_wind_condition_string_representation(self):
        expected_string = f"{self.spot.name} - 2024-03-20 - 15.5kts"
        self.assertEqual(str(self.condition), expected_string)

class ReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.spot = Spot.objects.create(
            name='Test Spot',
            location='Test Location',
            description='Test Description',
            latitude=Decimal('20.7984'),
            longitude=Decimal('-156.3319')
        )
        self.review = Review.objects.create(
            spot=self.spot,
            user=self.user,
            rating=5,
            comment='Great spot!'
        )

    def test_review_creation(self):
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, 'Great spot!')
        self.assertTrue(isinstance(self.review, Review))

    def test_review_string_representation(self):
        expected_string = f"{self.spot.name} - {self.user.username} - 5★"
        self.assertEqual(str(self.review), expected_string)

class SpotViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.spot = Spot.objects.create(
            name='Test Spot',
            location='Test Location',
            description='Test Description',
            latitude=Decimal('20.7984'),
            longitude=Decimal('-156.3319')
        )
        self.spot_url = reverse('myapp:spot_detail', args=[self.spot.pk])
        self.spot_list_url = reverse('myapp:spot_list')

    def test_spot_list_view(self):
        response = self.client.get(self.spot_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/spot_list.html')
        self.assertContains(response, 'Test Spot')

    def test_spot_detail_view(self):
        response = self.client.get(self.spot_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/spot_detail.html')
        self.assertContains(response, 'Test Spot')
        self.assertContains(response, 'Test Location')

    def test_add_review_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        review_url = reverse('myapp:add_review', args=[self.spot.pk])
        response = self.client.post(review_url, {
            'rating': 5,
            'comment': 'Great spot!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful post
        self.assertTrue(Review.objects.filter(spot=self.spot, user=self.user).exists())

    def test_add_review_unauthenticated(self):
        review_url = reverse('myapp:add_review', args=[self.spot.pk])
        response = self.client.get(review_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login page

class WindConditionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.spot = Spot.objects.create(
            name='Test Spot',
            location='Test Location',
            description='Test Description',
            latitude=Decimal('20.7984'),
            longitude=Decimal('-156.3319')
        )

    def test_add_condition_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        condition_url = reverse('myapp:add_condition', args=[self.spot.pk])
        response = self.client.post(condition_url, {
            'wind_speed': '15.5',
            'wind_direction': 'N',
            'temperature': '25.0'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful post
        self.assertTrue(WindCondition.objects.filter(spot=self.spot).exists())

    def test_add_condition_unauthenticated(self):
        condition_url = reverse('myapp:add_condition', args=[self.spot.pk])
        response = self.client.get(condition_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login page

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.login_url = reverse('login')
        self.spot_list_url = reverse('myapp:spot_list')

    def test_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_successful(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertRedirects(response, self.spot_list_url)
        
        # Check if user is logged in
        response = self.client.get(self.spot_list_url)
        self.assertEqual(str(response.context['user']), 'testuser')

    def test_login_failed(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_logout(self):
        # First login
        self.client.login(username='testuser', password='testpass123')
        
        # Check if user is logged in
        response = self.client.get(self.spot_list_url)
        self.assertEqual(str(response.context['user']), 'testuser')
        
        # Logout using POST
        response = self.client.post(reverse('myapp:logout'))
        self.assertEqual(response.status_code, 200)  # Shows logged_out.html
        self.assertTemplateUsed(response, 'registration/logged_out.html')
        
        # Check if user is logged out
        response = self.client.get(self.spot_list_url)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logged_out_page_content(self):
        response = self.client.get(reverse('myapp:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/logged_out.html')
        self.assertContains(response, 'You have been successfully logged out')
        self.assertContains(response, 'Log In Again')
        self.assertContains(response, 'Return to Spots')

    def test_logout_get_shows_template(self):
        # First login
        self.client.login(username='testuser', password='testpass123')
        
        # Try logout with GET
        response = self.client.get(reverse('myapp:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/logged_out.html')
