from django.conf import settings
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Brand, HeroImage, Product, PromotionPack, Shop
from .serializers import (
    BrandSerializer,
    HeroImageSerializer,
    ProductSerializer,
    PromotionPackSerializer,
    ShopSerializer,
)


class PublicQuerysetMixin:
    permission_classes = (AllowAny,)
    authentication_classes = ()


class HeroImageListView(PublicQuerysetMixin, generics.ListAPIView):
    serializer_class = HeroImageSerializer

    def get_queryset(self):
        return HeroImage.objects.filter(is_active=True).order_by("sort_order", "key")


class BrandListView(PublicQuerysetMixin, generics.ListAPIView):
    serializer_class = BrandSerializer

    def get_queryset(self):
        return Brand.objects.filter(is_active=True).order_by("sort_order", "label")


class ShopListView(PublicQuerysetMixin, generics.ListAPIView):
    serializer_class = ShopSerializer

    def get_queryset(self):
        return Shop.objects.filter(is_active=True).order_by("sort_order", "name_fr")


class PromotionPackListView(PublicQuerysetMixin, generics.ListAPIView):
    serializer_class = PromotionPackSerializer

    def get_queryset(self):
        return (
            PromotionPack.objects.filter(is_active=True)
            .prefetch_related("images")
            .order_by("sort_order", "title_fr")
        )


class ProductListView(PublicQuerysetMixin, generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = None

    def get_queryset(self):
        return (
            Product.objects.filter(is_active=True, brand__is_active=True)
            .select_related("brand")
            .order_by("sort_order", "name_fr")
        )


class PublicSiteView(PublicQuerysetMixin, APIView):
    def get(self, request):
        brands = Brand.objects.filter(is_active=True).order_by("sort_order", "label")
        shops = Shop.objects.filter(is_active=True).order_by("sort_order", "name_fr")
        hero_images = HeroImage.objects.filter(is_active=True).order_by(
            "sort_order", "key"
        )
        promotion_packs = (
            PromotionPack.objects.filter(is_active=True)
            .prefetch_related("images")
            .order_by("sort_order", "title_fr")
        )
        products = (
            Product.objects.filter(is_active=True, brand__is_active=True)
            .select_related("brand")
            .order_by("sort_order", "name_fr")
        )

        context = {"request": request}
        return Response(
            {
                "phone": getattr(settings, "SITE_PHONE", ""),
                "email": getattr(settings, "SITE_EMAIL", ""),
                "defaultLang": getattr(settings, "SITE_DEFAULT_LANG", "fr"),
                "counts": {
                    "officialBrands": brands.count(),
                    "officialShops": shops.filter(current=True).count(),
                },
                "heroImages": HeroImageSerializer(
                    hero_images, many=True, context=context
                ).data,
                "brands": BrandSerializer(brands, many=True, context=context).data,
                "shops": ShopSerializer(shops, many=True, context=context).data,
                "promotionPacks": PromotionPackSerializer(
                    promotion_packs, many=True, context=context
                ).data,
                "catalog": ProductSerializer(products, many=True, context=context).data,
            }
        )
