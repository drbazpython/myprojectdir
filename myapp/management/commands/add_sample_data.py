from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Spot, WindCondition, Review
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Adds sample data to the database'

    def handle(self, *args, **kwargs):
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='barrie').exists():
            User.objects.create_superuser('barrie', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: barrie'))

        # Create some regular users
        users = []
        for i in range(1, 4):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@example.com',
                    password='user123'
                )
                users.append(user)
                self.stdout.write(self.style.SUCCESS(f'Created user: {username}'))

        # Sample windsurf spots
        spots_data = [
            {
                'name': 'Maui Ho\'okipa',
                'location': 'Maui, Hawaii',
                'description': 'World-famous windsurfing spot known for its consistent waves and strong winds. '
                             'Best for advanced riders, featuring reef break waves and side-shore winds.',
                'latitude': 20.9334,
                'longitude': -156.3571
            },
            {
                'name': 'Tarifa Beach',
                'location': 'Tarifa, Spain',
                'description': 'Europe\'s windsurfing capital with strong Levante winds. '
                             'Perfect for all skill levels with shallow waters and consistent conditions.',
                'latitude': 36.0143,
                'longitude': -5.6044
            },
            {
                'name': 'Jericoacoara',
                'location': 'Ceará, Brazil',
                'description': 'Beautiful beach destination with steady trade winds and flat water lagoons. '
                             'Ideal for freestyle windsurfing and beginners.',
                'latitude': -2.7956,
                'longitude': -40.5137
            },
            {
                'name': 'Lake Garda',
                'location': 'Trentino, Italy',
                'description': 'Famous European lake spot with thermal winds and stunning mountain scenery. '
                             'Great for beginners in the morning and advanced riders in the afternoon.',
                'latitude': 45.8949,
                'longitude': 10.8766
            },
            {
                'name': 'Red Sea',
                'location': 'Dahab, Egypt',
                'description': 'Crystal clear waters with reliable thermal winds and flat water conditions. '
                             'Perfect for speed runs and freestyle tricks.',
                'latitude': 28.4817,
                'longitude': 34.4961
            }
        ]

        # Create spots
        for spot_data in spots_data:
            spot, created = Spot.objects.get_or_create(
                name=spot_data['name'],
                defaults=spot_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created spot: {spot.name}'))

                # Add wind conditions for the last 5 days
                for days_ago in range(5):
                    date = timezone.now().date() - timedelta(days=days_ago)
                    WindCondition.objects.create(
                        spot=spot,
                        date=date,
                        wind_speed=random.uniform(10.0, 25.0),
                        wind_direction=random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
                        temperature=random.uniform(20.0, 30.0)
                    )

                # Add reviews
                for user in users:
                    Review.objects.create(
                        spot=spot,
                        user=user,
                        rating=random.randint(3, 5),
                        comment=random.choice([
                            'Great spot for windsurfing! Perfect wind conditions.',
                            'Beautiful location with consistent winds.',
                            'One of my favorite places to windsurf.',
                            'Excellent spot with good facilities.',
                            'Amazing waves and wind conditions.'
                        ])
                    )

        self.stdout.write(self.style.SUCCESS('Successfully added sample data'))
