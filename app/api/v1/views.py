from django.db.models import Prefetch, Q
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from app.models import Book, BookAuthors, BookBookshelves, BookLanguages, BookSubjects

from .pagination import CustomPagination
from .serializers import BookSerializer


class BooksListAPIView(ListAPIView):
    serializer_class = BookSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Book.objects.prefetch_related(
            Prefetch(
                "bookauthors_set", queryset=BookAuthors.objects.select_related("author")
            ),
            Prefetch(
                "bookbookshelves_set",
                queryset=BookBookshelves.objects.select_related("bookshelf"),
            ),
            Prefetch(
                "booklanguages_set",
                queryset=BookLanguages.objects.select_related("language"),
            ),
            Prefetch(
                "booksubjects_set",
                queryset=BookSubjects.objects.select_related("subject"),
            ),
            "booksformat_set",
        ).order_by("-download_count")

        params = self.request.query_params

        # Filter by Gutenberg ID
        gutenberg_ids = params.getlist("gutenberg_id")
        if gutenberg_ids:
            queryset = queryset.filter(gutenberg_id__in=gutenberg_ids)

        # Filter by language
        languages = params.getlist("language")
        if languages:
            queryset = queryset.filter(booklanguages_set__language__code__in=languages)

        # Filter by mime-type
        mime_types = params.getlist("mime_type")
        if mime_types:
            queryset = queryset.filter(booksformat_set__mime_type__in=mime_types)

        # Filter by topic
        topics = params.getlist("topic")
        if topics:
            topic_queries = Q()
            for topic in topics:
                topic_queries |= Q(booksubjects_set__subject__name__icontains=topic)
                topic_queries |= Q(
                    bookbookshelves_set__bookshelf__name__icontains=topic
                )
            queryset = queryset.filter(topic_queries).distinct()

        # Filter by author
        authors = params.getlist("author")
        if authors:
            author_queries = Q()
            for author in authors:
                author_queries |= Q(bookauthors_set__author__name__icontains=author)
            queryset = queryset.filter(author_queries).distinct()

        # Filter by title
        titles = params.getlist("title")
        if titles:
            title_queries = Q()
            for title in titles:
                title_queries |= Q(title__icontains=title)
            queryset = queryset.filter(title_queries).distinct()

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "count": len(serializer.data),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
