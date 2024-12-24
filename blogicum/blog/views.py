from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category
from django.utils.timezone import now


class BaseMixin:
    model = Post


class BlogListView(BaseMixin, ListView):
    paginate_by = 5
    template_name = "blog/index.html"

    def get_queryset(self):
        return Post.get_published_posts().select_related('author', 'category',
                                                         'location')


class CategoryPostsView(BaseMixin, ListView):
    template_name = "blog/category.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category,
                                          slug=self.kwargs["category_slug"])
        if not self.category.is_published:
            raise Http404
        return Post.objects.filter(
            category=self.category, is_published=True, pub_date__lte=now()
        ).order_by("-pub_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class PostDetailView(BaseMixin, DetailView):
    template_name = "blog/detail.html"

    def get_object(self):
        qs = get_object_or_404(Post, pk=self.kwargs["pk"])
        if (qs.pub_date > now() or not qs.is_published
                or not qs.category.is_published):
            raise Http404
        return qs
