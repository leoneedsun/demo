from django.shortcuts import render
from .models import News, NewsCategory
from django.conf import settings
from .serializers import NewsSerializer, CommentSerializer
from utils import restful
from django.http import Http404
from .forms import PublicCommentForm
from .models import Comment


def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT

    # select_related 可以提前查询外键字段，提高查询效率，降低运算量
    newses = News.objects.select_related('category', 'author').all()[0:count]
    categories = NewsCategory.objects.all()
    context = {
        'newses': newses,
        'categories': categories
    }
    return render(request, 'news/index.html', context=context)


def news_list(request):
    # 通过p参数来指定获取第几页的数据
    # 并且这个p参数是通过查询字符串的方式传过来的：/news/list/?p=2
    # 如果没有给p传递参数，那么给一个默认值'1'
    page = int(request.GET.get('p', 1))

    # 分类为0，代表不进行任何分类，直接按照时间倒序排序
    category_id = int(request.GET.get('category_id', 0))

    # e.g page=1 -> start=0*2=0; page=2 -> start=1*2=2; page=3 -> start=2*2=4
    start = (page - 1) * settings.ONE_PAGE_NEWS_COUNT
    end = start + settings.ONE_PAGE_NEWS_COUNT

    if category_id == 0:
        # QureySet
        # {'id':1, 'title':'abc', category:{'id':1, 'name':'热点'}}
        # 所以需要进行序列化
        newses = News.objects.select_related('category', 'author').all()[start:end]
    else:
        newses = News.objects.filter(category_id=category_id)[start:end]
    serializer = NewsSerializer(newses, many=True)
    data = serializer.data
    return restful.result(data=data)


def news_detail(request, news_id):
    try:
        news = News.objects.select_related('category', 'author').prefetch_related('comments__author').get(pk=news_id)
        context = {
            'news': news
        }
        return render(request, 'news/news_detail.html', context=context)
    except News.DoesNotExist:
        raise Http404


def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        try:
            news_id = form.cleaned_data.get('news_id')
            content = form.cleaned_data.get('content')
            news = News.objects.get(pk=news_id)
            comment = Comment.objects.create(content=content, news=news, author=request.user)
            serialize = CommentSerializer(comment)
            return restful.result(data=serialize.data)
        except:
            raise Http404
    else:
        return restful.params_error(message=form.get_errors())


def search(request):
    return render(request, 'search/search.html')


def find404(request):
    return render(request, '404.html')
