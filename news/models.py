from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models import Max, Sum
from django.urls import reverse

# Create your models here.
# variables for categories

ctg_sport = 'SPRT'
ctg_world = 'WRLD'
ctg_science = 'SCNC'
ctg_auto = 'AUTO'
ctg_finance = 'FNNC'
ctg_technology = 'TECH'
ctg_culture = 'CLTR'
ctg_humor = 'HUMR'

# categories dictionary
CATEGORIES = [    
    (ctg_sport, 'Sport'),
    (ctg_world, 'World'),
    (ctg_science, 'Science'),
    (ctg_technology, 'Technology & IT'),
    (ctg_auto, 'Auto'),
    (ctg_finance, 'Finance'),
    (ctg_culture, 'Culture & Art'),
    (ctg_humor, 'Humor'),
]

article = 'A'
news = 'N'

POST_TYPE = [
    (news, 'News'),
    (article, 'Article'),
]

# model for categories 
class Category(models.Model):
    category = models.CharField(max_length=4,
                                choices=CATEGORIES,
                                unique=True)
    subscriber = models.ManyToManyField(User, through='CategoryUser')
    
    def __str__(self):
        category_abbreviation = self.category
        for abbreviation, full_name in CATEGORIES:
            if abbreviation == category_abbreviation:
                # print(full_name)
                return full_name
        return self.category


class CategoryUser(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                                 null=False)


# model for Authors as extension of User model
class Author(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                null=False)
    rating = models.IntegerField(default=0)
  
    # getting id from User model releted to the Author
    @property
    def user_id(self):
        return self.user.id
    
    def __str__(self):
        return self.user.username
    
    def get_articles(self):
        try:
            articles = Post.objects.filter(author=self)
            return articles
        except:
            return None

    def get_auth_comments(self):
        try:
            comments = Comment.objects.filter(user=self.user)
            return comments
        except:
            return None
    
    def get_auth_article_comments(self, article):
        try:
            comments = Comment.objects.filter(post=article)
            return comments
        except:
            return None

    
    def update_rating(self):
        articles = self.get_articles()
        auth_comments = self.get_auth_comments()
        
        rating_by_articles = 0
        rating_by_auth_comments = 0
        rating_by_articles_comments = 0
        try:
            if articles.exists():
                rating_by_articles = articles.aggregate(Sum('rating')).get('rating__sum') * 3
                

            if auth_comments.exists():
                rating_by_auth_comments = auth_comments.aggregate(Sum('rating')).get('rating__sum')
                
            
            if articles.exists():
                for article in articles:
                    article_comments = Comment.objects.filter(post=article)
                    if article_comments.exists():
                        rating_by_articles_comments += article_comments.aggregate(Sum('rating')).get('rating__sum')
                    
        except:
            print(f'ERROR: Unable get ratings')
            return False
        else:
            common_rating = sum([rating_by_articles, rating_by_auth_comments, rating_by_articles_comments])
            if common_rating > 0:
                print(f'INFO: Rating: {self.rating} >> {common_rating}')
                self.rating = common_rating
                self.save()
                return True
     


# model for Posts
class Post(models.Model):
    author = models.ForeignKey(Author,
                               on_delete=models.CASCADE,
                               null=False)
    type = models.CharField(max_length=1, 
                            choices=POST_TYPE,
                              default=news)
    publication_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, 
                                      through='PostCategory')
    title = models.CharField(max_length=100,
                             default='')
    content = models.TextField(default='Text here...')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save() 

    def dislike(self):
        if self.rating > 0:
            self.rating -= 1
            self.save()

    def preview(self):
        str = self.content[:100] + '...'
        return str
    
    def author_name(self):
        return str(self.user.username)
    
    def get_absolute_url(self):
        if self.type == "N":
            return reverse("news_detail", kwargs={"pk": self.pk}) # redirect to news/<int:pk>
        
        if self.type == "A":
            return reverse("article_detail", kwargs={"pk": self.pk}) # redirect to articles/<int:pk>
    

# model for releasing ManyToMany relation between
# Post and Category models/tables
class PostCategory(models.Model):
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 null=False)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             null=False)
    
class Comment (models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    comment = models.TextField(default=f'Comment here...')
    publication_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        if self.rating > 0:
            self.rating -= 1
            self.save()
    

