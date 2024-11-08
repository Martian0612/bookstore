from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

# Create your models here.

class Author(models.Model):
    
    name = models.CharField(max_length = 100)
    about = models.TextField()
    profile_photo = models.ImageField(upload_to = "static/author/img/", null= True, blank= True)

    def __str__(self):
        return self.name
    
class Publisher(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    contact = models.CharField(max_length= 50)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length= 200, unique= True)
    author = models.ForeignKey(Author, on_delete= models.SET_NULL , null= True,related_name = "book_author")
    # author = models.ForeignKey(Author, on_delete= models.SET_DEFAULT ,  default = None,related_name = "book_author")
    publisher = models.ForeignKey(Publisher, on_delete= models.SET_NULL , null= True, related_name = "book_publisher")
    # publisher = models.ForeignKey(Publisher, on_delete= models.SET_DEFAULT,  default = None, related_name = "book_publisher")
    published_date = models.DateField(auto_now_add= True)
    cover_image = models.ImageField(upload_to = "static/book/img/")
    genre = models.CharField(max_length = 100)
    description = models.TextField()
    language = models.CharField(max_length= 100)
    number_of_pages = models.IntegerField()

    # There will be a validator in serializer for checking the format of isbn_number
    isbn_number = models.CharField(unique= True, max_length=13 )


    # This fields will get calculated using their respective models, dynamically for read only purpose.

    @property
    def likes_count(self):
        return self.book_like.count()

    @property
    def rating_average(self):
        return self.book_rating.aggregate(Avg('rating'))['rating__avg'] or 0

    @property
    def rating_count(self):
        return self.book_rating.count()

    @property
    def comment_count(self):
        return self.book_comment.count()

class Like(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    book = models.ForeignKey(Book, on_delete= models.CASCADE,related_name= "book_like")
    timestamp = models.DateTimeField(auto_now = True)

class Rating(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    book = models.ForeignKey(Book, on_delete= models.CASCADE, related_name= "book_rating")
    
    rating_choices = ((1,1), (2,2),(3,3),(4,4),(5,5))
    rating = models.IntegerField( choices= rating_choices)
    timestamp = models.DateTimeField(auto_now = True)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete= models.CASCADE)
    book = models.ForeignKey(Book, on_delete= models.CASCADE, related_name= "book_comment")
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now = True)