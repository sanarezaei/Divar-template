from django.contrib import admin

from .models import Ad, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "owner", "created_at")
    list_filter = ("tags", "created_at")
    search_fields = ("title", "description", "owner__username")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    list_select_related = ("category", "owner")
