"""
Management command to populate the database with random test data.
Creates random users, places, and reviews for testing purposes.
"""

import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from reviews.models import Place, Review


User = get_user_model()


# Sample data for generating random entries
FIRST_NAMES = [
    'Aarav', 'Vivaan', 'Aditya', 'Vihaan', 'Arjun', 'Sai', 'Reyansh', 'Ayaan',
    'Krishna', 'Ishaan', 'Shaurya', 'Atharva', 'Advik', 'Pranav', 'Advaith',
    'Aarush', 'Dhruv', 'Kabir', 'Ritvik', 'Aaryan', 'Karthik', 'Darsh', 'Veer',
    'Saanvi', 'Aanya', 'Aadhya', 'Aaradhya', 'Ananya', 'Pari', 'Anika', 'Navya',
    'Diya', 'Myra', 'Sara', 'Ira', 'Ahana', 'Kiara', 'Anvi', 'Tara', 'Prisha',
    'Riya', 'Isha', 'Neha', 'Pooja', 'Kavya', 'Shreya', 'Divya', 'Sneha', 'Nisha',
]

LAST_NAMES = [
    'Sharma', 'Verma', 'Gupta', 'Singh', 'Kumar', 'Patel', 'Shah', 'Joshi',
    'Agarwal', 'Mehta', 'Reddy', 'Rao', 'Nair', 'Menon', 'Iyer', 'Iyengar',
    'Pillai', 'Choudhury', 'Banerjee', 'Chatterjee', 'Mukherjee', 'Das', 'Roy',
    'Bose', 'Sen', 'Ghosh', 'Dutta', 'Malhotra', 'Kapoor', 'Khanna', 'Saxena',
]

PLACE_TYPES = [
    'Restaurant', 'Cafe', 'Clinic', 'Hospital', 'Shop', 'Store', 'Bakery',
    'Pharmacy', 'Salon', 'Gym', 'Hotel', 'Bar', 'Lounge', 'Spa', 'Studio',
]

PLACE_PREFIXES = [
    'The Royal', 'Green', 'Blue', 'Golden', 'Silver', 'Royal', 'Grand',
    'The', 'New', 'Old', 'City', 'Urban', 'Prime', 'Elite', 'Classic',
    'Modern', 'Vintage', 'Cozy', 'Sunny', 'Happy', 'Fresh', 'Quick', 'Super',
]

PLACE_SUFFIXES = [
    'Palace', 'Corner', 'Hub', 'Point', 'Spot', 'Zone', 'Place', 'House',
    'Express', 'Central', 'Plaza', 'Center', 'Den', 'Junction', 'Avenue',
]

STREETS = [
    'MG Road', 'Park Street', 'Commercial Street', 'Brigade Road', 'FC Road',
    'Linking Road', 'Hill Road', 'Church Street', 'Anna Salai', 'Mount Road',
    'Residency Road', 'Cunningham Road', 'Infantry Road', 'St Marks Road',
    'Lavelle Road', 'Richmond Road', 'Palace Road', 'Race Course Road',
]

CITIES = [
    'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune',
    'Ahmedabad', 'Jaipur', 'Lucknow', 'Chandigarh', 'Kochi', 'Indore', 'Bhopal',
]

STATES = {
    'Mumbai': 'Maharashtra',
    'Delhi': 'Delhi',
    'Bangalore': 'Karnataka',
    'Hyderabad': 'Telangana',
    'Chennai': 'Tamil Nadu',
    'Kolkata': 'West Bengal',
    'Pune': 'Maharashtra',
    'Ahmedabad': 'Gujarat',
    'Jaipur': 'Rajasthan',
    'Lucknow': 'Uttar Pradesh',
    'Chandigarh': 'Chandigarh',
    'Kochi': 'Kerala',
    'Indore': 'Madhya Pradesh',
    'Bhopal': 'Madhya Pradesh',
}

POSITIVE_REVIEWS = [
    "Excellent service and quality! Highly recommended.",
    "Amazing experience. Will definitely come back.",
    "Best in the city! Worth every penny.",
    "Great atmosphere and friendly staff.",
    "Exceeded my expectations. Very satisfied.",
    "Top-notch quality. Five stars!",
    "Wonderful experience from start to finish.",
    "Absolutely loved it! Perfect in every way.",
    "Outstanding service. Very professional.",
    "Fantastic! Couldn't ask for more.",
]

NEUTRAL_REVIEWS = [
    "Decent experience. Nothing exceptional but not bad either.",
    "Average quality. Could be better.",
    "Okay service. Met basic expectations.",
    "Fair enough for the price.",
    "Nothing special but gets the job done.",
    "Moderately satisfied. Room for improvement.",
    "Standard quality. As expected.",
    "Acceptable service. No complaints.",
]

NEGATIVE_REVIEWS = [
    "Disappointing experience. Expected better.",
    "Not up to the mark. Needs improvement.",
    "Below average service. Would not recommend.",
    "Poor quality. Very unsatisfied.",
    "Not worth the price. Regret visiting.",
    "Bad experience. Staff was unhelpful.",
    "Very disappointed. Will not return.",
    "Substandard quality. Avoid if possible.",
]


class Command(BaseCommand):
    help = 'Populates the database with random users, places, and reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=50,
            help='Number of users to create (default: 50)'
        )
        parser.add_argument(
            '--places',
            type=int,
            default=100,
            help='Number of places to create (default: 100)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=500,
            help='Number of reviews to create (default: 500)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating'
        )

    def handle(self, *args, **options):
        num_users = options['users']
        num_places = options['places']
        num_reviews = options['reviews']
        clear_data = options['clear']

        if clear_data:
            self.stdout.write('Clearing existing data...')
            Review.objects.all().delete()
            Place.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        # Create users
        self.stdout.write(f'Creating {num_users} users...')
        users = self._create_users(num_users)
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users.'))

        # Create places
        self.stdout.write(f'Creating {num_places} places...')
        places = self._create_places(num_places)
        self.stdout.write(self.style.SUCCESS(f'Created {len(places)} places.'))

        # Create reviews
        self.stdout.write(f'Creating {num_reviews} reviews...')
        reviews = self._create_reviews(num_reviews, users, places)
        self.stdout.write(self.style.SUCCESS(f'Created {len(reviews)} reviews.'))

        self.stdout.write(self.style.SUCCESS(
            f'\nData population complete!\n'
            f'  - Users: {len(users)}\n'
            f'  - Places: {len(places)}\n'
            f'  - Reviews: {len(reviews)}'
        ))

    def _generate_phone_number(self):
        """Generate a random Indian phone number."""
        return f'+91{random.randint(7000000000, 9999999999)}'

    def _generate_name(self):
        """Generate a random full name."""
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        return f'{first_name} {last_name}'

    def _generate_place_name(self):
        """Generate a random place name."""
        place_type = random.choice(PLACE_TYPES)
        
        # Different naming patterns
        pattern = random.choice(['prefix', 'suffix', 'both', 'simple'])
        
        if pattern == 'prefix':
            prefix = random.choice(PLACE_PREFIXES)
            return f'{prefix} {place_type}'
        elif pattern == 'suffix':
            suffix = random.choice(PLACE_SUFFIXES)
            return f'{place_type} {suffix}'
        elif pattern == 'both':
            prefix = random.choice(PLACE_PREFIXES)
            suffix = random.choice(PLACE_SUFFIXES)
            return f'{prefix} {suffix}'
        else:
            last_name = random.choice(LAST_NAMES)
            return f"{last_name}'s {place_type}"

    def _generate_address(self):
        """Generate a random address."""
        building_no = random.randint(1, 500)
        street = random.choice(STREETS)
        city = random.choice(CITIES)
        state = STATES[city]
        pincode = random.randint(100000, 999999)
        
        return f'{building_no}, {street}, {city}, {state} - {pincode}'

    def _generate_review_text(self, rating):
        """Generate review text based on rating."""
        # 20% chance of no review text
        if random.random() < 0.2:
            return ''
        
        if rating >= 4:
            return random.choice(POSITIVE_REVIEWS)
        elif rating == 3:
            return random.choice(NEUTRAL_REVIEWS)
        else:
            return random.choice(NEGATIVE_REVIEWS)

    def _create_users(self, count):
        """Create random users."""
        users = []
        existing_phones = set(User.objects.values_list('phone_number', flat=True))
        
        attempts = 0
        max_attempts = count * 3
        
        while len(users) < count and attempts < max_attempts:
            attempts += 1
            phone = self._generate_phone_number()
            
            if phone in existing_phones:
                continue
            
            existing_phones.add(phone)
            
            user = User.objects.create_user(
                phone_number=phone,
                name=self._generate_name(),
                password='testpass123'  # Simple password for testing
            )
            users.append(user)
        
        return users

    def _create_places(self, count):
        """Create random places."""
        places = []
        existing_places = set(
            Place.objects.values_list('name', 'address')
        )
        
        attempts = 0
        max_attempts = count * 3
        
        while len(places) < count and attempts < max_attempts:
            attempts += 1
            name = self._generate_place_name()
            address = self._generate_address()
            
            if (name, address) in existing_places:
                continue
            
            existing_places.add((name, address))
            
            place = Place.objects.create(
                name=name,
                address=address
            )
            places.append(place)
        
        return places

    def _create_reviews(self, count, users, places):
        """Create random reviews."""
        if not users or not places:
            self.stdout.write(self.style.WARNING(
                'No users or places available. Skipping review creation.'
            ))
            return []
        
        reviews = []
        
        for _ in range(count):
            user = random.choice(users)
            place = random.choice(places)
            
            # Generate rating with weighted distribution (more positive reviews)
            rating = random.choices(
                [1, 2, 3, 4, 5],
                weights=[5, 10, 20, 30, 35],
                k=1
            )[0]
            
            review = Review.objects.create(
                user=user,
                place=place,
                rating=rating,
                text=self._generate_review_text(rating)
            )
            reviews.append(review)
        
        return reviews
