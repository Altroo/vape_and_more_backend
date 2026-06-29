from rest_framework import serializers

from .models import Brand, HeroImage, Product, PromotionPack, PromotionPackImage, Shop

LANGUAGES = ("fr", "ar", "en", "es")


def media_url(request, obj, image_field="image", path_field="image_path"):
    image = getattr(obj, image_field, None)
    if image:
        try:
            url = image.url
        except ValueError:
            url = ""
        if url:
            return request.build_absolute_uri(url) if request else url
    return getattr(obj, path_field, "")


def localized_object(obj, fields):
    values = {}
    for lang in LANGUAGES:
        values[lang] = {
            output_name: getattr(obj, f"{field_name}_{lang}", "")
            for output_name, field_name in fields.items()
        }
    return values


def localized_lines(obj, field_name):
    return {
        lang: [
            line.strip()
            for line in getattr(obj, f"{field_name}_{lang}", "").splitlines()
            if line.strip()
        ]
        for lang in LANGUAGES
    }


class HeroImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HeroImage
        fields = ("key", "image", "alt", "sort_order")

    def get_image(self, obj):
        return media_url(self.context.get("request"), obj)


class BrandSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    logo = serializers.SerializerMethodField()
    texts = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ("key", "label", "image", "logo", "texts", "sort_order")

    def get_image(self, obj):
        return media_url(self.context.get("request"), obj)

    def get_logo(self, obj):
        return media_url(self.context.get("request"), obj, "logo", "logo_path")

    def get_texts(self, obj):
        return localized_object(obj, {"headline": "headline", "copy": "copy"})


class ShopSerializer(serializers.ModelSerializer):
    directions = serializers.CharField(source="directions_url")
    texts = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = (
            "key",
            "current",
            "map_query",
            "directions",
            "texts",
            "sort_order",
        )

    def get_texts(self, obj):
        return localized_object(
            obj, {"name": "name", "address": "address", "hours": "hours"}
        )


class PromotionPackImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    alt = serializers.SerializerMethodField()

    class Meta:
        model = PromotionPackImage
        fields = ("image", "alt", "sort_order")

    def get_image(self, obj):
        return media_url(self.context.get("request"), obj)

    def get_alt(self, obj):
        return {lang: getattr(obj, f"alt_{lang}", "") for lang in LANGUAGES}


class PromotionPackSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    texts = serializers.SerializerMethodField()
    whatsapp_messages = serializers.SerializerMethodField()

    class Meta:
        model = PromotionPack
        fields = (
            "key",
            "discount_label",
            "is_best_offer",
            "image",
            "images",
            "old_price",
            "price",
            "texts",
            "whatsapp_messages",
            "sort_order",
        )

    def get_image(self, obj):
        return media_url(self.context.get("request"), obj)

    def get_images(self, obj):
        gallery = obj.images.filter(is_active=True).order_by("sort_order", "id")
        return PromotionPackImageSerializer(
            gallery, many=True, context=self.context
        ).data

    def get_texts(self, obj):
        return localized_object(
            obj,
            {
                "title": "title",
                "target": "target",
                "description": "description",
            },
        )

    def get_whatsapp_messages(self, obj):
        return {lang: getattr(obj, f"whatsapp_message_{lang}", "") for lang in LANGUAGES}


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.CharField(source="brand.label")
    brand_key = serializers.CharField(source="brand.key")
    image = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    texts = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "key",
            "brand",
            "brand_key",
            "image",
            "price",
            "texts",
            "sort_order",
        )

    def get_image(self, obj):
        return media_url(self.context.get("request"), obj)

    def get_price(self, obj):
        return {lang: getattr(obj, f"price_{lang}", "") for lang in LANGUAGES}

    def get_texts(self, obj):
        texts = localized_object(
            obj, {"name": "name", "description": "description"}
        )
        flavors = localized_lines(obj, "flavors")
        for lang in LANGUAGES:
            texts[lang]["flavors"] = flavors[lang]
        return texts
