from django.test import TestCase
from django.urls import reverse

from .models import Brand, HeroImage, Product, Shop


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
        self.assertEqual(payload["catalog"][0]["texts"]["fr"]["flavors"], ["Rouge", "Vert"])
