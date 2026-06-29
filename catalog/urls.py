from django.urls import path

from .views import (
    BrandListView,
    HeroImageListView,
    ProductListView,
    PromotionPackListView,
    PublicSiteView,
    ShopListView,
)

urlpatterns = [
    path("content/", PublicSiteView.as_view(), name="public-site"),
    path("hero-images/", HeroImageListView.as_view(), name="hero-images"),
    path("brands/", BrandListView.as_view(), name="brands"),
    path("shops/", ShopListView.as_view(), name="shops"),
    path("promotions/", PromotionPackListView.as_view(), name="promotions"),
    path("products/", ProductListView.as_view(), name="products"),
    path("catalog/products/", ProductListView.as_view(), name="catalog-products"),
]
