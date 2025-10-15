from typing import Any

from django.db.models import Model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Ad, Category, Tag


@receiver(post_save, sender=Category)
def create_tag_for_category(
    sender: type[Model], instance: Category, created: bool, **kwargs: Any
) -> None:
    if created:
        Tag.objects.get_or_create(
            name=instance.name, defaults={"slug": slugify(instance.name)}
        )


@receiver(post_save, sender=Ad)
def add_category_tag(
    sender: type[Model], instance: Category, created: bool, **kwargs: Any
) -> None:
    if created and instance.category:
        tag, _ = Tag.objects.get_or_create(
            name=instance.category.name, defaults={"slug": instance.category.slug}
        )

        instance.tags.add(tag)
