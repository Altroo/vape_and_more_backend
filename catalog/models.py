from django.db import models


class TimestampedOrderedModel(models.Model):
    created_at = models.DateTimeField("date de creation", auto_now_add=True)
    updated_at = models.DateTimeField("date de modification", auto_now=True)
    sort_order = models.PositiveIntegerField(
        "position dans la page",
        default=0,
        help_text="Plus le nombre est bas, plus l'element apparait tot.",
    )
    is_active = models.BooleanField(
        "visible sur le site",
        default=True,
        help_text="Decochez pour masquer cet element sans le supprimer.",
    )

    class Meta:
        abstract = True


class ImageSourceModel(models.Model):
    image = models.ImageField(
        "image a charger", upload_to="site/images/", blank=True, null=True
    )
    image_path = models.CharField(
        "image deja presente dans le site",
        max_length=500,
        blank=True,
        help_text=(
            "Optionnel. A utiliser seulement pour une image deja fournie avec "
            "le site, par exemple /assets/photo-01.png."
        ),
    )

    class Meta:
        abstract = True


class HeroImage(TimestampedOrderedModel, ImageSourceModel):
    image = models.ImageField(
        "image a charger", upload_to="site/hero/", blank=True, null=True
    )
    key = models.SlugField("identifiant interne", max_length=120, unique=True)
    alt = models.CharField(
        "description courte de l'image",
        max_length=200,
        blank=True,
        help_text="Texte utile pour l'accessibilite. Il n'est pas affiche comme titre.",
    )

    class Meta:
        ordering = ("sort_order", "key")
        verbose_name = "visuel du bandeau d'accueil"
        verbose_name_plural = "visuels du bandeau d'accueil"

    def __str__(self):
        return self.alt or self.key


class Brand(TimestampedOrderedModel, ImageSourceModel):
    image = models.ImageField(
        "photo de la marque", upload_to="site/brands/", blank=True, null=True
    )
    key = models.SlugField("identifiant interne", max_length=120, unique=True)
    label = models.CharField("nom de la marque", max_length=160)
    logo = models.ImageField(
        "logo a charger", upload_to="site/brand-logos/", blank=True, null=True
    )
    logo_path = models.CharField(
        "logo deja present dans le site",
        max_length=500,
        blank=True,
        help_text=(
            "Optionnel. A utiliser seulement pour un logo deja fourni avec le "
            "site, par exemple /assets/marque/Nerd LOGO.png."
        ),
    )
    headline_fr = models.CharField("titre FR", max_length=200, blank=True)
    headline_ar = models.CharField("titre AR", max_length=200, blank=True)
    headline_en = models.CharField("titre EN", max_length=200, blank=True)
    headline_es = models.CharField("titre ES", max_length=200, blank=True)
    copy_fr = models.TextField("description FR", blank=True)
    copy_ar = models.TextField("description AR", blank=True)
    copy_en = models.TextField("description EN", blank=True)
    copy_es = models.TextField("description ES", blank=True)

    class Meta:
        ordering = ("sort_order", "label")
        verbose_name = "marque officielle"
        verbose_name_plural = "marques officielles"

    def __str__(self):
        return self.label


class Shop(TimestampedOrderedModel):
    key = models.SlugField("identifiant interne", max_length=120, unique=True)
    current = models.BooleanField(
        "compter comme boutique officielle",
        default=True,
        help_text="Cochez si cette boutique doit etre incluse dans le compteur du site.",
    )
    map_query = models.CharField(
        "recherche Google Maps",
        max_length=300,
        blank=True,
        help_text="Nom ou adresse utilisee pour afficher la carte.",
    )
    directions_url = models.URLField(
        "lien itineraire Google Maps", max_length=500, blank=True
    )
    name_fr = models.CharField("nom FR", max_length=200, blank=True)
    name_ar = models.CharField("nom AR", max_length=200, blank=True)
    name_en = models.CharField("nom EN", max_length=200, blank=True)
    name_es = models.CharField("nom ES", max_length=200, blank=True)
    address_fr = models.TextField("adresse FR", blank=True)
    address_ar = models.TextField("adresse AR", blank=True)
    address_en = models.TextField("adresse EN", blank=True)
    address_es = models.TextField("adresse ES", blank=True)
    hours_fr = models.CharField("horaires FR", max_length=240, blank=True)
    hours_ar = models.CharField("horaires AR", max_length=240, blank=True)
    hours_en = models.CharField("horaires EN", max_length=240, blank=True)
    hours_es = models.CharField("horaires ES", max_length=240, blank=True)

    class Meta:
        ordering = ("sort_order", "name_fr")
        verbose_name = "boutique officielle"
        verbose_name_plural = "boutiques officielles"

    def __str__(self):
        return self.name_fr or self.key


class PromotionPack(TimestampedOrderedModel, ImageSourceModel):
    image = models.ImageField(
        "image principale", upload_to="site/promotions/", blank=True, null=True
    )
    key = models.SlugField("identifiant interne", max_length=120, unique=True)
    discount_label = models.CharField("badge de remise", max_length=40, blank=True)
    is_best_offer = models.BooleanField("mettre en avant", default=False)
    old_price = models.CharField("ancien prix", max_length=80, blank=True)
    price = models.CharField("prix affiche", max_length=80, blank=True)
    title_fr = models.CharField("titre FR", max_length=200, blank=True)
    title_ar = models.CharField("titre AR", max_length=200, blank=True)
    title_en = models.CharField("titre EN", max_length=200, blank=True)
    title_es = models.CharField("titre ES", max_length=200, blank=True)
    target_fr = models.CharField("sous-titre FR", max_length=240, blank=True)
    target_ar = models.CharField("sous-titre AR", max_length=240, blank=True)
    target_en = models.CharField("sous-titre EN", max_length=240, blank=True)
    target_es = models.CharField("sous-titre ES", max_length=240, blank=True)
    description_fr = models.TextField("description FR", blank=True)
    description_ar = models.TextField("description AR", blank=True)
    description_en = models.TextField("description EN", blank=True)
    description_es = models.TextField("description ES", blank=True)
    whatsapp_message_fr = models.TextField("message WhatsApp FR", blank=True)
    whatsapp_message_ar = models.TextField("message WhatsApp AR", blank=True)
    whatsapp_message_en = models.TextField("message WhatsApp EN", blank=True)
    whatsapp_message_es = models.TextField("message WhatsApp ES", blank=True)

    class Meta:
        ordering = ("sort_order", "title_fr")
        verbose_name = "pack promotionnel"
        verbose_name_plural = "packs promotionnels"

    def __str__(self):
        return self.title_fr or self.key


class PromotionPackImage(TimestampedOrderedModel, ImageSourceModel):
    image = models.ImageField(
        "image a charger",
        upload_to="site/promotion-gallery/",
        blank=True,
        null=True,
    )
    pack = models.ForeignKey(
        PromotionPack, related_name="images", on_delete=models.CASCADE
    )
    alt_fr = models.CharField("description courte FR", max_length=200, blank=True)
    alt_ar = models.CharField("description courte AR", max_length=200, blank=True)
    alt_en = models.CharField("description courte EN", max_length=200, blank=True)
    alt_es = models.CharField("description courte ES", max_length=200, blank=True)

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "photo du pack"
        verbose_name_plural = "photos du pack"

    def __str__(self):
        return self.alt_fr or self.image_path or str(self.pk)


class Product(TimestampedOrderedModel, ImageSourceModel):
    image = models.ImageField(
        "image du produit", upload_to="site/products/", blank=True, null=True
    )
    key = models.SlugField("identifiant interne", max_length=120, unique=True)
    brand = models.ForeignKey(
        Brand,
        verbose_name="marque",
        related_name="products",
        on_delete=models.PROTECT,
    )
    name_fr = models.CharField("nom FR", max_length=200, blank=True)
    name_ar = models.CharField("nom AR", max_length=200, blank=True)
    name_en = models.CharField("nom EN", max_length=200, blank=True)
    name_es = models.CharField("nom ES", max_length=200, blank=True)
    description_fr = models.TextField("description FR", blank=True)
    description_ar = models.TextField("description AR", blank=True)
    description_en = models.TextField("description EN", blank=True)
    description_es = models.TextField("description ES", blank=True)
    flavors_fr = models.TextField(
        "saveurs FR", blank=True, help_text="Une saveur par ligne."
    )
    flavors_ar = models.TextField(
        "saveurs AR", blank=True, help_text="Une saveur par ligne."
    )
    flavors_en = models.TextField(
        "saveurs EN", blank=True, help_text="Une saveur par ligne."
    )
    flavors_es = models.TextField(
        "saveurs ES", blank=True, help_text="Une saveur par ligne."
    )
    price_fr = models.CharField("prix FR", max_length=120, blank=True)
    price_ar = models.CharField("prix AR", max_length=120, blank=True)
    price_en = models.CharField("prix EN", max_length=120, blank=True)
    price_es = models.CharField("prix ES", max_length=120, blank=True)

    class Meta:
        ordering = ("sort_order", "name_fr")
        verbose_name = "produit du catalogue"
        verbose_name_plural = "produits du catalogue"

    def __str__(self):
        return self.name_fr or self.key
