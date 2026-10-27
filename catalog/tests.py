from importlib import import_module
from types import SimpleNamespace

from django.apps import apps
from django.db import connection
from django.test import TestCase
from django.urls import reverse

from .models import Brand, HeroImage, Product, Shop


class ArabicBrandCopyTests(TestCase):
    migration = import_module("catalog.migrations.0003_refine_arabic_brand_copy")

    def test_seed_copy_is_refined_and_can_be_restored(self):
        for key, previous, revised in self.migration.COPY_UPDATES:
            brand = Brand.objects.create(
                key=key, label=key, copy_ar=previous, copy_fr="Original"
            )
            self.migration.refine_arabic_copy(
                apps, SimpleNamespace(connection=connection)
            )
            brand.refresh_from_db()
            self.assertEqual(brand.copy_ar, revised)
            self.assertEqual(brand.copy_fr, "Original")
            self.migration.restore_arabic_copy(
                apps, SimpleNamespace(connection=connection)
            )
            brand.refresh_from_db()
            self.assertEqual(brand.copy_ar, previous)

    def test_custom_arabic_copy_is_preserved(self):
        for key, _, _ in self.migration.COPY_UPDATES:
            Brand.objects.create(key=key, label=key, copy_ar="وصف مخصص للمتجر")
        self.migration.refine_arabic_copy(apps, SimpleNamespace(connection=connection))
        self.migration.restore_arabic_copy(apps, SimpleNamespace(connection=connection))
        self.assertEqual(Brand.objects.filter(copy_ar="وصف مخصص للمتجر").count(), 2)


class PublicSiteApiTests(TestCase):
    def test_site_payload_exposes_dynamic_content_and_counts(self):
        brand = Brand.objects.create(
            key="nerd",
            label="Nerd",
            logo_path="/assets/marque/Nerd LOGO.png",
            headline_fr="Nerd",
            copy_fr="Collection moderne",
        )
        HeroImage.objects.create(
            key="hero-1", image_path="/assets/photo-01.png", alt="Hero"
        )
        Shop.objects.create(key="bourgogne", current=True, name_fr="Bourgogne")
        Product.objects.create(
            key="nerd-20k",
            brand=brand,
            image_path="/assets/promos/promo_1.png",
            name_fr="Nerd 20K",
            flavors_fr="Rouge\nVert",
            price_fr="225 DH",
        )

        response = self.client.get(reverse("public-site"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["counts"]["officialBrands"], 1)
        self.assertEqual(payload["counts"]["officialShops"], 1)
        self.assertEqual(payload["heroImages"][0]["image"], "/assets/photo-01.png")
        self.assertEqual(payload["catalog"], [])

        products_response = self.client.get(reverse("catalog-products"))
        self.assertEqual(products_response.status_code, 200)
        self.assertEqual(products_response.json(), [])
