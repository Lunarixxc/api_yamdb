import django_filters
from django.shortcuts import get_object_or_404
from reviews.models import Review, Comment, Title, Category, Genre
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsOwnerOrModeratorOrAdmin, IsAdminOrReadOnly

from .serializers import (
    CommentSerializer, GenreSerializer,
    ReviewSerializer, CategorySerializer,
    TitleSerializer,
)
from .mixins import CustomViewSet


class CategoryViewSet(CustomViewSet):
    permission_classes = [IsAdminOrReadOnly, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name', )


class GenreViewSet(CustomViewSet):
    permission_classes = [IsAdminOrReadOnly, ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ('=name', )


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='contains'
    )
    category = django_filters.CharFilter(
        field_name='category__slug',
        lookup_expr='exact'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug',
        lookup_expr='exact'
    )

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrModeratorOrAdmin]

    def get_queryset(self):
        title_id = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get("title_id"))
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrModeratorOrAdmin]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        title_id = self.kwargs.get("title_id")
        review = get_object_or_404(Review, id=review_id, title=title_id)
        new_queryset = Comment.objects.filter(review=review)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=get_object_or_404(Review, id=self.kwargs.get("review_id"))
        )
