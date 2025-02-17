from django.db import models


class Author(models.Model):
    birth_year = models.IntegerField(blank=True, null=True)
    death_year = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)

    class Meta:
        db_table = "books_author"


class Book(models.Model):
    download_count = models.IntegerField(blank=True, null=True)
    gutenberg_id = models.IntegerField(unique=True)
    media_type = models.CharField(max_length=16)
    title = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        db_table = "books_book"


class BookAuthors(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        db_table = "books_book_authors"
        unique_together = (("book", "author"),)


class BookBookshelves(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    bookshelf = models.ForeignKey("Bookshelf", on_delete=models.CASCADE)  # Fixed

    class Meta:
        db_table = "books_book_bookshelves"
        unique_together = (("book", "bookshelf"),)


class BookLanguages(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    language = models.ForeignKey("Language", on_delete=models.CASCADE)  # Fixed

    class Meta:
        db_table = "books_book_languages"
        unique_together = (("book", "language"),)


class BookSubjects(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)  # Fixed

    class Meta:
        db_table = "books_book_subjects"
        unique_together = (("book", "subject"),)


class Bookshelf(models.Model):
    name = models.CharField(unique=True, max_length=64)

    class Meta:
        db_table = "books_bookshelf"


class BooksFormat(models.Model):
    mime_type = models.CharField(max_length=32)
    url = models.CharField(max_length=256)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        db_table = "books_format"


class Language(models.Model):
    code = models.CharField(unique=True, max_length=4)

    class Meta:
        db_table = "books_language"


class Subject(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        db_table = "books_subject"
