# # # # from django.shortcuts import render
# # # #
# # # # from blog.models import Article
# # # #
# # # #
# # # # def home(request):
# # # #     articles = Article.objects.all()
# # # #     return  render(request, 'blog/home.html')
# # # #
# # # # for article in Article.objects.all():
# # # #     print(article.title)
# # # #
# # # # first_article = Article.objects.all()[0]
# # # # first_article_1 = Article.objects.all().first()
# # # # last_article = Article.objects.all().last()
# # # #
# # # # first_five = Article.objects.all()[:5]
# # # # articles_5_to_10 = Article.objects.all()[5:10]
# # # # total_articles = Article.objects.all().count()
# # # #
# # # # has_articles = Article.objects.all().exists()
# # # # published_articles = Article.objects.filter(is_published=True).order_by('-published_date')[:10]
# # # # int()
# # # #
# # # # article = Article(
# # # #     title="Введение в Django ORM",
# # # #     content="Ура, я знакомлюсь с ORM Django. И узнал что это мощный инструмент",
# # # #     author=some_user,
# # # #     is_published=True,
# # # # )
# # # # article.save()
# # # #
# # # # article_1 = Article.objects.create(
# # # # title="Введение в Django ORM",
# # # #     content="Ура, я знакомлюсь с ORM Django. И узнал что это мощный инструмент",
# # # #     author=some_user,
# # # #     is_published=True,
# # # # )
# # # #
# # # # articles = [
# # # #     Article(title=f'Статья {i}', content=f'Содержание статьи {i}', author=some_user)
# # # #     for i in range(100)
# # # # ]
# # # # Article.objects.bulk_create(articles)
# # # #
# # # # article = Article.objects.get(id=1)
# # # # article.title = 'Обновленный заголовок'
# # # # article.content = 'Новое содержание статьи'
# # # # article.save()
# # # #
# # # # article.title = 'Обновленный заголовок'
# # # # article.save(update_fields=['title'])
# # # # Article.objects.filter(author=some_user).update(is_published=True)
# # # #
# # # # article = Article.objects.get(id=1)
# # # # article.delete()
# # # #
# # # # def home(request):
# # # #     articles = Article.objects.filter(is_published=True).select_related('author')
# # # #     return render(request, 'blog/home.html', {'articles': articles})
# # # #
# # # # articles = Article.objects.select_related('author', 'author__profile')
# # # #
# # # # def home(request):
# # # #     articles = Article.objects.filter(is_published=True).select_related('author').prefetch_related('tags')
# # # #     return render(request, 'blog/home.html', {'articles': articles})
# # # #
# # # # from django.db.models import Prefetch
# # # #
# # # # # Загружаем статьи, их авторов и только опубликованные статьи авторов
# # # # articles = Article.objects.select_related('author').prefetch_related(
# # # #     Prefetch('author__articles', queryset=Article.objects.filter(is_published=True))
# # # # )
# # # #
# # # # Article.objects.filter(is_published=True, author__username='john')
# # # #
# # # #
# # # # from django.db.models import Q
# # # #
# # # # article = Article.objects.filter(
# # # #     Q(is_published=True) | Q(author__username='john')
# # # # )
# # # #
# # # # articles = Article.objects.filter(
# # # #     Q(is_published=True) & (Q(author__username='john') | Q(author__username='alice'))
# # # # )
# # # #
# # # # articles = Article.objects.filter(~Q(is_published=True))
# # # # articles = Article.objects.exclude(is_published=True)
# # # from django.db.models import Q
# # #
# # # def search_articles(title=None, author=None, tag=None):
# # #     query = Q()
# # #
# # #     if title:
# # #         query &= Q(title__icontains=title)
# # #     if author:
# # #         query &= Q(author__username=author)
# # #     if tag:
# # #         query &= Q(tags__name=tag)
# # #
# # #     return Article.objects.filter(query)
# # #
# # # from django.db.models import F
# # #
# # # popular_articles = Article.objects.filter(likes_count__gt=F('views_count') / 2)
# # #
# # # # ПЛОХО: гонка данных при конкурентных запросах
# # # article = Article.objects.get(id=1)
# # # article.views_count = article.views_count + 1
# # # article.save()
# # #
# # #
# # # # ХОРОШО: атомарное обновление
# # # article = Article.objects.get(id=1)
# # # article.views_count = F('views_count') + 1
# # # article.save()
# # #
# # # def home(request):
# # # articles = (
# # #     Article.objects
# # #     .filter(is_published=True)
# # #     .annotate(
# # #         rating=F('likes') - F('dislikes'),
# # #
# # #         full_title=Concat(
# # #             F('title'),
# # #             Value(' — '),
# # #             F('subtitle')
# # #         )
# # #     )
# # #     .select_related('author')
# # #     .prefetch_related('tags')
# # # )
# # #
# # # return render(request, 'blog/home.html', {'articles': articles})
# #
# #
# # # ОТ 25/10
# #
# # from django.db.models import Count
# #
# # total_published = Article.objects.filter(is_published=True).count()
# #
# # from django.db.models import Count, Avg, Max, Min, Sum
# #
# # # Получаем статистику по всем статьям
# # stats = Article.objects.aggregate(
# #     total_articles=Count('id'),
# #     avg_tags=Avg('tags__id'),  # Среднее количество тегов на статью (приблизительно)
# # )
# # # Результат: {'total_articles': 150, 'avg_tags': 3.5}
# #
# #
# # from django.db.models import Count
# #
# # articles = Article.objects.annotate(tags_count=Count('tags'))
# #
# # for article in articles:
# #     print(f"{article.title} имеет {article.tags_count} тегов")
# #
# # # Найдем статьи с более чем тремя тегами и отсортируем по количеству тегов
# # popular_articles = Article.objects.annotate(
# #     tags_count=Count('tags')
# # ).filter(tags_count__gt=3).order_by('-tags_count')
# #
# #
# # from django.contrib.auth.models import User
# # from django.db.models import Count, Q
# #
# # authors = User.objects.annotate(
# #     publosher_article_count = Count('articles', filter=Q(is_published=True)
# #                                     ).filter(popular_articles_count__gt=0).order_by('-publosher_article_count')
# # )
# #
# # django.db.models.functions
# #
# # from django.db.models import Count, F, FloatField
# # from django.db.models.functions import Cast
# #
# # articles = Article.objects.annotate(
# #     tags_count=Count('tags'),
# #     # Вычисляем плотность тегов (тегов на символ содержания)
# #     content_length=Cast(models.functions.Length('content'), FloatField()),
# #     tag_density=F('tags_count') / F('content_length')
# # ).filter(tag_density__gt=0.001)
# #
# #
# # articles = Article.objects.raw('SELECT * FROM blog_article WHERE is_published = %s', [True])
# #
# # for article in articles:
# #     print(article.title)  # Это полноценный объект Article
# #
# # articles = Article.objects.raw(
# #     "SELECT * FROM blog_article WHERE to_tsvector('russian', title || ' ' || content) @@ to_tsquery('russian', %s)",
# #     ['Django & ORM']
# # )
# #
# # from django.db import connection
# #
# # def get_article_statistics():
# #     with connection.cursor() as cursor:
# #         cursor.execute("""
# #             SELECT
# #                 u.username,
# #                 COUNT(a.id) as article_count,
# #                 AVG(LENGTH(a.content)) as avg_content_length
# #             FROM auth_user u
# #             LEFT JOIN blog_article a ON u.id = a.author_id
# #             WHERE a.is_published = TRUE
# #             GROUP BY u.id, u.username
# #             HAVING COUNT(a.id) > 0
# #             ORDER BY article_count DESC
# #         """)
# #         columns = [col[0] for col in cursor.description]
# #         return [dict(zip(columns, row)) for row in cursor.fetchall()]
# #
# #
# # articles = Article.objects.extra(
# #     select={'content_length': 'LENGTH(content)'},
# #     where=['LENGTH(content) > %s'],
# #     params=[1000],
# #     order_by=['-content_length']
# # )
# #
# # from django.db.models.functions import Length
# #
# # articles = Article.objects.annotate(
# #     content_length=Length('content')
# # ).filter(content_length__gt=1000).order_by('-content_length')
#
#
# from  django.db import models
#
# class TimeStampedModel(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     class Meta:
#         abstract = True
#
#
# class Article(TimeStampedModel):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
#     tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
#     published_date = models.DateTimeField(auto_now_add=True)
#     is_published = models.BooleanField(default=False)
#
#     class Meta:
#         ordering = ['-published_date']
#         verbose_name = 'статья'
#         verbose_name_plural = 'статьи'
#
# class Tag(TimeStampedModel):
#     name = models.CharField(max_length=50, unique=True)
#     slug = models.SlugField(unique=True)
#
#     class Meta:
#         verbose_name = 'тег'
#         verbose_name_plural = 'теги'
#
# class PublishableModel(models.Model):
#     is_published = models.BooleanField(default=False)
#     published_date = models.DateTimeField(null=True, blank=True)
#
#     class Meta:
#         abstract = True
#
#     def publish(self):
#         """Публикует объект, устанавливая текущую дату"""
#         from django.utils import timezone
#         self.is_published = True
#         self.published_date = timezone.now()
#         self.save(update_fields=['is_published', 'published_date'])
#
#     def unpublish(self):
#         """Снимает объект с публикации"""
#         self.is_published = False
#         self.save(update_fields=['is_published'])
#
# class BaseModel(TimeStampedModel):
#     class Meta:
#         abstract = True
#
#     def get_absolute_url(self):
#         raise NotImplementedError
#
# class PublishableModel(BaseModel):
#     is_published = models.BooleanField(default=False)
#     published_date = models.DateTimeField(null=True, blank=True)
#     class Meta:
#         abstract = True
#
#
# class PublishedArticle(Article):
#     class Meta:
#         proxy = True
#         ordering = ['-published_date']
#         verbose_name = 'опубликованная статья'
#         verbose_name_plural = 'опубликованные статьи'
#
#     def get_related_articles(self):
#         """Возвращает похожие опубликованные статьи по тегам"""
#         return Article.objects.filter(
#             tags__in=self.tags.all(),
#             is_published=True
#         ).exclude(id=self.id).distinct()[:5]
#
# class PublishedArticleManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(is_published=True)
#
# class PublishedArticle(Article):
#     objects = PublishedArticleManager()
#
#     class Meta:
#         proxy = True
#
# # Вместо Article.objects.filter(is_published=True)
# # Можно просто
# def home(request):
#     articles = PublishedArticle.objects.select_related('author').prefetch_related('tags')
#     return render(request, 'blog/home.html', {'articles': articles})
#
#
# class PublishedArticleManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(is_published=True).select_related('author')
#
# class Article(TimeStampedModel):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
#     tags = models.ManyToManyField(Tag, related_name='articles', blank=True)
#     published_date = models.DateTimeField(auto_now_add=True)
#     is_published = models.BooleanField(default=False)
#
#     objects = models.Manager()  # Стандартный менеджер
#     published = PublishedArticleManager()  # Кастомный менеджер
#
#     class Meta:
#         ordering = ['-published_date']
#
#
# class ArticleManager(models.Manager):
#     def published(self):
#         """Возвращает опубликованные статьи"""
#         return self.filter(is_published=True)
#
#     def by_author(self, username):
#         """Возвращает статьи конкретного автора"""
#         return self.filter(author__username=username)
#
#     def recent(self, days=7):
#         """Возвращает статьи за последние N дней"""
#         from django.utils import timezone
#         from datetime import timedelta
#         threshold = timezone.now() - timedelta(days=days)
#         return self.filter(published_date__gte=threshold)
#
#     def with_tags(self, tag_names):
#         """Возвращает статьи с указанными тегами"""
#         return self.filter(tags__name__in=tag_names).distinct()
#
#     def popular(self, min_tags=3):
#         """Возвращает популярные статьи (с большим количеством тегов)"""
#         from django.db.models import Count
#         return self.annotate(tags_count=Count('tags')).filter(tags_count__gte=min_tags)
#
# class Article(TimeStampedModel):
#     # ... поля модели ...
#     objects = ArticleManager()
#
# # Опубликованные статьи конкретного автора за последнюю неделю
# recent_articles = Article.objects.published().by_author('john').recent(7)
#
# # Популярные статьи с определенными тегами
# popular = Article.objects.popular(min_tags=5).with_tags(['Django', 'Python'])
#
#
# class ArticleManager(models.Manager):
#     def create_article(self, title, content, author, tags=None):
#         """Создает статью с автоматической генерацией slug"""
#         from django.utils.text import slugify
#
#         article = self.create(
#             title=title,
#             content=content,
#             author=author
#         )
#
#         if tags:
#             article.tags.set(tags)
#
#         return article
#
# # Использование
# article = Article.objects.create_article(
#     title='Новая статья',
#     content='Содержание статьи',
#     author=request.user,
#     tags=[tag1, tag2]
# )
#
# class ArticleQuerySet(models.QuerySet):
#     def published(self):
#         return self.filter(is_published=True)
#
#     def by_author(self, username):
#         return self.filter(author__username=username)
#
#     def recent(self, days=7):
#         from django.utils import timezone
#         from datetime import timedelta
#         threshold = timezone.now() - timedelta(days=days)
#         return self.filter(published_date__gte=threshold)
#
# class ArticleManager(models.Manager):
#     def get_queryset(self):
#         return ArticleQuerySet(self.model, using=self._db)
#
#     def published(self):
#         return self.get_queryset().published()
#
#     def by_author(self, username):
#         return self.get_queryset().by_author(username)
#
#     def recent(self, days=7):
#         return self.get_queryset().recent(days)
#
# class ArticleQuerySet(models.QuerySet):
#     def published(self):
#         return self.filter(is_published=True)
#
#     def by_author(self, username):
#         return self.filter(author__username=username)
#
# class Article(models.Model):
#     # ... поля ...
#     objects = ArticleQuerySet.as_manager()