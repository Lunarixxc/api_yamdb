from django.shortcuts import get_object_or_404
from reviews.models import Review, Comment, Title
from rest_framework import viewsets, filters, mixins
from rest_framework.pagination import LimitOffsetPagination

from .permissions import CustomPermissions
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [CustomPermissions]

    def get_queryset(self):
        new_queryset = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, id=self.kwargs.get("title_id"))
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset
