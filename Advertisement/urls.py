from django.urls import path

from .views import (
    AdCreateView,
    AdDeleteView,
    AdDetailView,
    AdListView,
    AdUpdateView,
    search,
    tag_ad,
)

app_name = "ads"

urlpatterns = [
    path("", AdListView.as_view(), name="ad_list"),
    path("<int:pk>/", AdDetailView.as_view(), name="ad_detail"),
    path("create/", AdCreateView.as_view(), name="ad_create"),
    path("<int:pk>/edit/", AdUpdateView.as_view(), name="ad_update"),
    path("<int:pk>/delete/", AdDeleteView.as_view(), name="ad_delete"),
    path("search/", search, name="search"),
    path("tag/<slug:slug>/", tag_ad, name="tag"),
]
