from rest_framework import serializers
from django.db.models import Avg
from .models import Place, Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model - used for displaying review details.
    """
    reviewer_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'rating', 'text', 'created_at', 'reviewer_name']
        read_only_fields = ['id', 'created_at', 'reviewer_name']


class CreateReviewSerializer(serializers.Serializer):
    """
    Serializer for creating a new review.
    Handles place creation/lookup and review creation.
    """
    place_name = serializers.CharField(
        max_length=255,
        help_text='Name of the place being reviewed'
    )
    place_address = serializers.CharField(
        help_text='Full address of the place'
    )
    rating = serializers.IntegerField(
        min_value=1,
        max_value=5,
        help_text='Rating from 1 to 5'
    )
    text = serializers.CharField(
        required=False,
        allow_blank=True,
        default='',
        help_text='Optional review text'
    )

    def validate_rating(self, value):
        """
        Validate that rating is between 1 and 5.
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                'Rating must be between 1 and 5.'
            )
        return value

    def create(self, validated_data):
        """
        Create or get place, then create the review.
        """
        user = self.context['request'].user
        place_name = validated_data['place_name'].strip()
        place_address = validated_data['place_address'].strip()

        # Get or create the place
        place, created = Place.objects.get_or_create(
            name=place_name,
            address=place_address
        )

        # Create the review
        review = Review.objects.create(
            user=user,
            place=place,
            rating=validated_data['rating'],
            text=validated_data.get('text', '')
        )

        return review


class PlaceSearchSerializer(serializers.Serializer):
    """
    Serializer for place search results.
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)


class PlaceDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed place information including all reviews.
    """
    average_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ['id', 'name', 'address', 'average_rating', 'review_count', 'reviews']

    def get_reviews(self, obj):
        """
        Return reviews with the current user's review first (if exists),
        followed by other reviews sorted by newest first.
        """
        request = self.context.get('request')
        current_user = request.user if request else None

        all_reviews = obj.reviews.select_related('user').all()
        
        # Separate current user's review from others
        user_reviews = []
        other_reviews = []
        
        for review in all_reviews:
            if current_user and review.user_id == current_user.id:
                user_reviews.append(review)
            else:
                other_reviews.append(review)

        # Sort other reviews by newest first (already ordered by -created_at in model)
        ordered_reviews = user_reviews + other_reviews

        return ReviewSerializer(ordered_reviews, many=True).data


class PlaceListSerializer(serializers.ModelSerializer):
    """
    Serializer for place listing with average rating.
    """
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Place
        fields = ['id', 'name', 'address', 'average_rating']
