from uuid import uuid4

from django.contrib import admin
from django.utils.text import slugify

from .models import Brand, HeroImage, Product, PromotionPack, PromotionPackImage, Shop


LANGUAGE_TITLES = {
    "fr": "Textes en francais",
    "ar": "Textes en arabe",
    "en": "Textes en anglais",
    "es": "Textes en espagnol",
}


def unique_key(model, source, obj=None):
    base = slugify(source or model._meta.verbose_name) or model._meta.model_name
    base = base[:90].strip("-") or model._meta.model_name
    key = base
    queryset = model.objects.all()
    if obj and obj.pk:
        queryset = queryset.exclude(pk=obj.pk)
    while queryset.filter(key=key).exists():
        key = f"{base[:82].strip('-')}-{uuid4().hex[:6]}"
    return key


class TranslationFieldsetMixin:
    language_fields = ()

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))
        if self.language_fields:
            for lang in ("fr", "ar", "en", "es"):
                fieldsets.append(
                    (
                        LANGUAGE_TITLES[lang],
                        {"fields": [f"{field}_{lang}" for field in self.language_fields]},
                    )
                )
        return fieldsets


class GeneratedKeyAdminMixin:
    slug_source_fields = ()

    def get_slug_source(self, obj):
        for field_name in self.slug_source_fields:
            value = getattr(obj, field_name, "")
            if value:
                return value
        return str(obj) or obj._meta.verbose_name

    def save_model(self, request, obj, form, change):
        if hasattr(obj, "key") and not obj.key:
            obj.key = unique_key(type(obj), self.get_slug_source(obj), obj)
        super().save_model(request, obj, form, change)


@admin.register(HeroImage)
class HeroImageAdmin(GeneratedKeyAdminMixin, admin.ModelAdmin):
    slug_source_fields = ("alt",)
    list_display = ("alt", "sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("alt",)
    ordering = ("sort_order", "key")
    fieldsets = (
        (
            "Image du bandeau d'accueil",
            {
                "description": (
                    "Ajoutez les images qui defilent dans le bandeau principal "
                    "de la page d'accueil."
                ),
                "fields": (
                    "image",
                    "image_path",
                    "alt",
                    "sort_order",
                    "is_active",
                ),
            },
        ),
    )


@admin.register(Brand)
class BrandAdmin(GeneratedKeyAdminMixin, TranslationFieldsetMixin, admin.ModelAdmin):
    language_fields = ("headline", "copy")
    slug_source_fields = ("label", "headline_fr", "headline_en")
    list_display = ("label", "sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("label", "headline_fr", "headline_en", "copy_fr", "copy_en")
    ordering = ("sort_order", "label")
    fieldsets = (
        (
            "Marque officielle",
            {
                "description": (
                    "Cette section alimente la zone Nos marques et le compteur "
                    "Marques officielles."
                ),
                "fields": (
                    "label",
                    "image",
                    "image_path",
                    "logo",
                    "logo_path",
                    "sort_order",
                    "is_active",
                )
            },
        ),
    )


@admin.register(Shop)
class ShopAdmin(GeneratedKeyAdminMixin, TranslationFieldsetMixin, admin.ModelAdmin):
    language_fields = ("name", "address", "hours")
    slug_source_fields = ("name_fr", "name_en")
    list_display = ("name_fr", "current", "sort_order", "is_active")
    list_filter = ("current", "is_active")
    search_fields = ("name_fr", "name_en", "address_fr", "address_en")
    ordering = ("sort_order", "name_fr")
    fieldsets = (
        (
            "Boutique officielle",
            {
                "description": (
                    "Les boutiques cochees comme officielles sont comptees dans "
                    "le chiffre affiche sur le site."
                ),
                "fields": (
                    "current",
                    "map_query",
                    "directions_url",
                    "sort_order",
                    "is_active",
                )
            },
        ),
    )


class PromotionPackImageInline(admin.TabularInline):
    model = PromotionPackImage
    extra = 0
    fields = (
        "image",
        "image_path",
        "alt_fr",
        "alt_ar",
        "alt_en",
        "alt_es",
        "sort_order",
        "is_active",
    )
    ordering = ("sort_order", "id")
    verbose_name = "photo du pack"
    verbose_name_plural = "photos du pack"


@admin.register(PromotionPack)
class PromotionPackAdmin(GeneratedKeyAdminMixin, TranslationFieldsetMixin, admin.ModelAdmin):
    language_fields = ("title", "target", "description", "whatsapp_message")
    slug_source_fields = ("title_fr", "title_en")
    list_display = ("title_fr", "discount_label", "price", "sort_order", "is_active")
    list_filter = ("is_best_offer", "is_active")
    search_fields = ("title_fr", "title_en", "description_fr", "description_en")
    ordering = ("sort_order", "title_fr")
    inlines = (PromotionPackImageInline,)
    fieldsets = (
        (
            "Pack promotionnel",
            {
                "description": (
                    "Ces packs alimentent la section Packs promotionnels de la "
                    "page d'accueil."
                ),
                "fields": (
                    "discount_label",
                    "is_best_offer",
                    "image",
                    "image_path",
                    "old_price",
                    "price",
                    "sort_order",
                    "is_active",
                )
            },
        ),
    )


@admin.register(Product)
class ProductAdmin(GeneratedKeyAdminMixin, TranslationFieldsetMixin, admin.ModelAdmin):
    language_fields = ("name", "description", "flavors", "price")
    slug_source_fields = ("name_fr", "name_en")
    list_display = ("name_fr", "brand", "sort_order", "is_active")
    list_filter = ("brand", "is_active")
    search_fields = ("name_fr", "name_en", "description_fr", "description_en")
    ordering = ("sort_order", "name_fr")
    fieldsets = (
        (
            "Produit du catalogue",
            {
                "description": (
                    "Ces produits alimentent la page Catalogue. Les saveurs se "
                    "saisissent avec une saveur par ligne."
                ),
                "fields": (
                    "brand",
                    "image",
                    "image_path",
                    "sort_order",
                    "is_active",
                )
            },
        ),
    )
