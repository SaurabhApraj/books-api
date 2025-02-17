from rest_framework import serializers

from app.models import Book


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.SerializerMethodField()
    bookshelves = serializers.SerializerMethodField()
    subjects = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()
    formats = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            "title",
            "authors",
            "bookshelves",
            "subjects",
            "languages",
            "formats",
        ]

    def get_authors(self, obj):
        return [{"name": author.author.name} for author in obj.bookauthors_set.all()]

    def get_bookshelves(self, obj):
        return [
            {"name": bookshelf.bookshelf.name}
            for bookshelf in obj.bookbookshelves_set.all()
        ]

    def get_subjects(self, obj):
        return [
            {"name": subject.subject.name} for subject in obj.booksubjects_set.all()
        ]

    def get_languages(self, obj):
        return [
            {"code": language.language.code} for language in obj.booklanguages_set.all()
        ]

    def get_formats(self, obj):
        return [
            {"mime_type": format.mime_type, "url": format.url}
            for format in obj.booksformat_set.all()
        ]
