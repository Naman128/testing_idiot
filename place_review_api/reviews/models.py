from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Place(models.Model):
    """
    Model representing a place that can be reviewed.
    Places can be shops, restaurants, doctors, etc.
    """
    name = models.CharField(
        max_length=255,
        help_text='Name of the place (e.g., restaurant name, shop name)'
    )
    address = models.TextField(
        help_text='Full address of the place'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'places'
        verbose_name = 'place'
        verbose_name_plural = 'places'
        ordering = ['name']
        # Unique constraint: combination of name + address must be unique
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'address'],
                name='unique_place_name_address'
            )
        ]
        indexes = [
            models.Index(fields=['name'], name='place_name_idx'),
        ]

    def __str__(self):
        return f"{self.name} - {self.address[:50]}"

    def get_average_rating(self):
        """
        Calculate and return the average rating for this place.
        Returns None if no reviews exist.
        """
        reviews = self.reviews.all()
        if not reviews.exists():
            return None
        
        total_rating = sum(review.rating for review in reviews)
        return round(total_rating / reviews.count(), 2)

    def get_review_count(self):
        """
        Return the total number of reviews for this place.
        """
        return self.reviews.count()


class Review(models.Model):
    """
    Model representing a user's review of a place.
    """
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='User who wrote this review'
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Place being reviewed'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Rating must be at least 1'),
            MaxValueValidator(5, message='Rating cannot exceed 5')
        ],
        help_text='Rating from 1 (worst) to 5 (best)'
    )
    text = models.TextField(
        blank=True,
        default='',
        help_text='Optional review text/comments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'place'], name='review_user_place_idx'),
            models.Index(fields=['-created_at'], name='review_created_at_idx'),
        ]

    def __str__(self):
        return f"Review by {self.user.name} for {self.place.name} - {self.rating}/5"
