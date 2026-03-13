from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Q, Case, When, Value, IntegerField
from django.db.models.functions import Lower
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Place, Review
from .serializers import (
    CreateReviewSerializer,
    ReviewSerializer,
    PlaceDetailSerializer,
    PlaceListSerializer,
)


class AddReviewView(APIView):
    """
    API endpoint to add a new review for a place.
    If the place doesn't exist, it will be created.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
        Add a new review for a place.
        
        If a place with the given name and address exists, the review will be added to it.
        If not, a new place will be created first.
        
        **Required fields:**
        - place_name: Name of the place
        - place_address: Full address of the place
        - rating: Integer from 1 to 5
        
        **Optional fields:**
        - text: Review text/comments
        """,
        request_body=CreateReviewSerializer,
        responses={
            201: openapi.Response(
                description="Review added successfully",
                examples={
                    "application/json": {
                        "message": "Review added successfully.",
                        "review": {
                            "id": 1,
                            "rating": 5,
                            "text": "Great place!",
                            "created_at": "2025-12-28T12:00:00Z",
                            "reviewer_name": "John Doe"
                        },
                        "place": {
                            "id": 1,
                            "name": "Pizza Palace",
                            "address": "123 Main Street"
                        }
                    }
                }
            ),
            400: "Bad Request - Invalid input data",
            401: "Unauthorized - Token required"
        },
        tags=['Reviews']
    )
    def post(self, request):
        serializer = CreateReviewSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            review = serializer.save()
            
            return Response({
                'message': 'Review added successfully.',
                'review': ReviewSerializer(review).data,
                'place': {
                    'id': review.place.id,
                    'name': review.place.name,
                    'address': review.place.address,
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchPlacesView(APIView):
    """
    API endpoint to search for places.
    
    Query Parameters:
    - name: Search by place name (exact matches shown first, then partial)
    - min_rating: Filter by minimum average rating
    
    Behavior:
    - If name is provided: exact matches first, then partial substring matches
    - If min_rating is provided: only places with avg rating >= min_rating
    """
    permission_classes = [IsAuthenticated]

    name_param = openapi.Parameter(
        'name',
        openapi.IN_QUERY,
        description="Search by place name. Exact matches appear first, followed by partial matches.",
        type=openapi.TYPE_STRING,
        required=False
    )
    min_rating_param = openapi.Parameter(
        'min_rating',
        openapi.IN_QUERY,
        description="Filter places with average rating >= this value. Must be between 1 and 5.",
        type=openapi.TYPE_NUMBER,
        required=False
    )

    @swagger_auto_schema(
        operation_description="""
        Search for places by name and/or minimum rating.
        
        **Search Behavior:**
        - If `name` is provided, places with exact name match appear first, then partial matches
        - If `min_rating` is provided, only places with average rating >= min_rating are shown
        - Both parameters can be combined
        
        **Response includes:**
        - count: Total number of matching places
        - results: List of places with id, name, address, and average_rating
        """,
        manual_parameters=[name_param, min_rating_param],
        responses={
            200: openapi.Response(
                description="Search results",
                examples={
                    "application/json": {
                        "count": 2,
                        "results": [
                            {"id": 1, "name": "Pizza Palace", "address": "123 Main St", "average_rating": 4.5},
                            {"id": 2, "name": "Pizza Hut", "address": "456 Oak Ave", "average_rating": 3.8}
                        ]
                    }
                }
            ),
            400: "Bad Request - Invalid min_rating value",
            401: "Unauthorized - Token required"
        },
        tags=['Places']
    )
    def get(self, request):
        name_query = request.query_params.get('name', '').strip()
        min_rating_str = request.query_params.get('min_rating', '')

        # Start with all places
        queryset = Place.objects.all()

        # Annotate with average rating
        queryset = queryset.annotate(
            average_rating=Avg('reviews__rating')
        )

        # Filter by minimum rating if provided
        if min_rating_str:
            try:
                min_rating = float(min_rating_str)
                if min_rating < 1 or min_rating > 5:
                    return Response(
                        {'error': 'min_rating must be between 1 and 5.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # Only include places with reviews and avg rating >= min_rating
                queryset = queryset.filter(average_rating__gte=min_rating)
            except ValueError:
                return Response(
                    {'error': 'min_rating must be a valid number.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Filter and sort by name if provided
        if name_query:
            name_query_lower = name_query.lower()
            
            # Filter places that contain the search term (case-insensitive)
            queryset = queryset.filter(name__icontains=name_query)
            
            # Annotate for sorting: exact matches first (case-insensitive)
            queryset = queryset.annotate(
                is_exact_match=Case(
                    When(name__iexact=name_query, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                )
            ).order_by('is_exact_match', 'name')
        else:
            # Default ordering by name
            queryset = queryset.order_by('name')

        # Serialize the results
        serializer = PlaceListSerializer(queryset, many=True)
        
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)


class PlaceDetailView(APIView):
    """
    API endpoint to get detailed information about a place.
    
    Returns:
    - Place name, address, average rating
    - List of all reviews with the current user's review first,
      then remaining reviews sorted by newest first
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
        Get detailed information about a specific place.
        
        **Response includes:**
        - id, name, address of the place
        - average_rating: Average of all ratings
        - review_count: Total number of reviews
        - reviews: List of all reviews with reviewer names
        
        **Review ordering:**
        - Current user's review appears first (if exists)
        - Other reviews are sorted by newest first
        """,
        responses={
            200: PlaceDetailSerializer,
            404: "Not Found - Place does not exist",
            401: "Unauthorized - Token required"
        },
        tags=['Places']
    )
    def get(self, request, place_id):
        try:
            place = Place.objects.prefetch_related(
                'reviews',
                'reviews__user'
            ).get(id=place_id)
        except Place.DoesNotExist:
            return Response(
                {'error': 'Place not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Calculate average rating and review count
        reviews = place.reviews.all()
        avg_rating = None
        if reviews.exists():
            avg_rating = round(sum(r.rating for r in reviews) / reviews.count(), 2)

        # Prepare response data
        serializer = PlaceDetailSerializer(place, context={'request': request})
        response_data = serializer.data
        response_data['average_rating'] = avg_rating
        response_data['review_count'] = reviews.count()

        return Response(response_data, status=status.HTTP_200_OK)


class UserReviewsView(APIView):
    """
    API endpoint to get all reviews by the current authenticated user.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
        Get all reviews submitted by the current authenticated user.
        
        **Response includes:**
        - count: Total number of reviews by the user
        - reviews: List of reviews with place information
        
        Each review contains:
        - id, rating, text, created_at
        - place: Object with id, name, and address
        """,
        responses={
            200: openapi.Response(
                description="User's reviews",
                examples={
                    "application/json": {
                        "count": 2,
                        "reviews": [
                            {
                                "id": 1,
                                "rating": 5,
                                "text": "Great!",
                                "created_at": "2025-12-28T12:00:00Z",
                                "place": {"id": 1, "name": "Pizza Palace", "address": "123 Main St"}
                            }
                        ]
                    }
                }
            ),
            401: "Unauthorized - Token required"
        },
        tags=['Reviews']
    )
    def get(self, request):
        reviews = Review.objects.filter(user=request.user).select_related('place')
        
        review_data = []
        for review in reviews:
            review_data.append({
                'id': review.id,
                'rating': review.rating,
                'text': review.text,
                'created_at': review.created_at,
                'place': {
                    'id': review.place.id,
                    'name': review.place.name,
                    'address': review.place.address,
                }
            })

        return Response({
            'count': len(review_data),
            'reviews': review_data
        }, status=status.HTTP_200_OK)
