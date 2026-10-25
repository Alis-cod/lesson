from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q, Avg
from django.db.models.functions import Length
from django.contrib.auth import get_user_model
from .models import Article, Tag

User = get_user_model()
def home(request):
    articles = Article.objects.published().with_author_and_tags().recent_first()[:20]
    return render(request, 'blog/home.html', {'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(
        Article.objects.published().with_author_and_tags(),
        id=article_id
    )
    
    related_articles = Article.objects.published().filter(
        tags__in=article.tags.all()
    ).exclude(
        id=article.id
    ).annotate(
        same_tags=Count('id')
    ).order_by('-same_tags', '-published_date').with_author_and_tags()[:5]
    
    return render(request, 'blog/article_detail.html', {
        'article': article,
        'related_articles': related_articles
    })

def authors_stats(request):
    authors = User.objects.annotate(
        total_articles=Count('articles', filter=Q(articles__is_published=True)),
        avg_content_length=Avg(Length('articles__content'), filter=Q(articles__is_published=True)),
        total_tags=Count('articles__tags', distinct=True, filter=Q(articles__is_published=True))
    ).filter(
        total_articles__gt=0
    ).order_by('-total_articles')
    
    return render(request, 'blog/authors_stats.html', {
        'authors': authors
    })

def search(request):
    query = request.GET.get('q', '')
    
    if query:
        articles = Article.objects.published().filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
        ).distinct().with_author_and_tags().recent_first()[:50]
    else:
        articles = Article.objects.none()
    
    return render(request, 'blog/search.html', {
        'articles': articles,
        'query': query
    })

def tag_articles(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    articles = Article.objects.published().filter(
        tags=tag
    ).with_author_and_tags().recent_first()
    
    return render(request, 'blog/tag_articles.html', {
        'tag': tag,
        'articles': articles
    })