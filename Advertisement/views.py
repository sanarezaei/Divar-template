from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Ad, Tag


def search(request: HttpRequest) -> HttpResponse:
    searched = request.GET.get("searched", "")
    ad_titles = Ad.objects.filter(title__icontains=searched) if searched else []

    context: Dict[str, Any] = {
        "searched": searched,
        "ad_titles": ad_titles,
    }

    return render(request, "ads/search.html", context)


def tag_ad(request: HttpRequest, slug: str) -> HttpResponse:
    tag = get_object_or_404(Tag, slug=slug)
    ads = Ad.objects.filter(tags=tag)

    context: Dict[str, Any] = {
        "tag": tag,
        "ads": ads,
        "tags": Tag.objects.all().order_by("name"),
    }
    return render(request, "ads/tag_ads.html", context)


class AdListView(ListView):
    model = Ad
    template_name = "ads/ad_list.html"
    context_object_name = "ads"
    ordering = ["-created_at"]

    def get_queryset(self) -> Any:
        return super().get_queryset()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all().order_by("name")
        return context


class AdDetailView(DetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    context_object_name = "ad"


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    fields = ["title", "description", "image", "category"]
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("ads:ad_list")

    def form_valid(self, form: Any) -> HttpResponse:
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    fields = ["title", "description", "image", "category"]
    template_name = "ads/ad_form.html"
    success_url = reverse_lazy("ads:ad_list")

    def test_func(self) -> bool:
        ad: Ad = self.get_object()
        return bool(self.request.user == ad.owner)


class AdDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Ad
    template_name = "ads/ad_delete.html"
    success_url = reverse_lazy("ads:ad_list")

    def test_func(self) -> bool:
        ad = self.get_object()
        return bool(self.request.user == ad.owner)
