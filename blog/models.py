from django.db import models
from django.contrib.auth import get_user_model

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        abstract = True

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
    
    def __str__(self):
        return self.name

class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)
   
    def with_author_and_tags(self):
        return self.select_related('author').prefetch_related('tags')
   
    def recent_first(self):
        return self.order_by('-created_at')

User = get_user_model()

class Article(TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    tags = models.ManyToManyField(Tag, through='ArticleTag', related_name='articles')
    published_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    objects = ArticleQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['article', 'tag']

