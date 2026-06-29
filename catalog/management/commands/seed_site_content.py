from django.core.management.base import BaseCommand

from catalog.models import (
    Brand,
    HeroImage,
    Product,
    PromotionPack,
    PromotionPackImage,
    Shop,
)


def localized(prefix, values):
    data = {}
    for lang, text in values.items():
        data[f"{prefix}_{lang}"] = text
    return data


def localized_group(prefixes, values):
    data = {}
    for lang, fields in values.items():
        for source, target in prefixes.items():
            value = fields.get(source, "")
            if isinstance(value, list):
                value = "\n".join(value)
            data[f"{target}_{lang}"] = value
    return data


class Command(BaseCommand):
    help = "Seed the editable public Vape & More site content."

    def handle(self, *args, **options):
        hero_images = [
            ("hero-01", "/assets/photo-01.png", "Vape & More hero image 1", 1),
            ("hero-02", "/assets/photo-02.png", "Vape & More hero image 2", 2),
            ("hero-03", "/assets/photo-03.png", "Vape & More hero image 3", 3),
        ]
        for key, image_path, alt, order in hero_images:
            HeroImage.objects.update_or_create(
                key=key,
                defaults={
                    "image_path": image_path,
                    "alt": alt,
                    "sort_order": order,
                    "is_active": True,
                },
            )

        brands = [
            {
                "key": "crown-bar-al-fakher",
                "label": "Crown Bar Al Fakher",
                "image_path": "/assets/photo-01.png",
                "logo_path": "/assets/marque/ALFAKHER LOGO.png",
                "sort_order": 1,
                "texts": {
                    "fr": {
                        "headline": "Crown Bar Al Fakher",
                        "copy": "Une marque premium à l’identité forte, présentée clairement dans la section marques et le pied de page.",
                    },
                    "ar": {
                        "headline": "Crown Bar Al Fakher",
                        "copy": "علامة فاخرة بهوية قوية، معروضة بوضوح ضمن قسم العلامات التجارية والتذييل.",
                    },
                    "en": {
                        "headline": "Crown Bar Al Fakher",
                        "copy": "A premium brand with a strong identity, presented clearly in the brands section and footer.",
                    },
                    "es": {
                        "headline": "Crown Bar Al Fakher",
                        "copy": "Una marca premium con una identidad fuerte, presentada claramente en la sección de marcas y en el pie de página.",
                    },
                },
            },
            {
                "key": "adalya",
                "label": "Adalya",
                "image_path": "/assets/photo-02.png",
                "logo_path": "/assets/marque/ADALYA LOGO.png",
                "sort_order": 2,
                "texts": {
                    "fr": {
                        "headline": "Adalya",
                        "copy": "Une gamme reconnue pour la richesse de ses arômes, ses profils variés et sa qualité régulière.",
                    },
                    "ar": {
                        "headline": "Adalya",
                        "copy": "مجموعة معروفة بغنى النكهات وتنوعها وجودتها المنتظمة.",
                    },
                    "en": {
                        "headline": "Adalya",
                        "copy": "A recognized range known for rich aromas, varied profiles, and consistent quality.",
                    },
                    "es": {
                        "headline": "Adalya",
                        "copy": "Una gama reconocida por sus aromas intensos, perfiles variados y calidad constante.",
                    },
                },
            },
            {
                "key": "nerd",
                "label": "Nerd",
                "image_path": "/assets/promos/TRIO PACK.png",
                "logo_path": "/assets/marque/Nerd LOGO.png",
                "sort_order": 3,
                "texts": {
                    "fr": {
                        "headline": "Nerd",
                        "copy": "Une collection moderne avec des formats pratiques, des saveurs distinctives et une expérience premium.",
                    },
                    "ar": {
                        "headline": "Nerd",
                        "copy": "تشكيلة عصرية بأحجام عملية ونكهات مميزة وتجربة فاخرة.",
                    },
                    "en": {
                        "headline": "Nerd",
                        "copy": "A modern collection with practical formats, distinctive flavors, and a premium experience.",
                    },
                    "es": {
                        "headline": "Nerd",
                        "copy": "Una colección moderna con formatos prácticos, sabores distintivos y una experiencia premium.",
                    },
                },
            },
        ]
        for brand in brands:
            defaults = {
                "label": brand["label"],
                "image_path": brand["image_path"],
                "logo_path": brand["logo_path"],
                "sort_order": brand["sort_order"],
                "is_active": True,
            }
            defaults.update(
                localized_group(
                    {"headline": "headline", "copy": "copy"}, brand["texts"]
                )
            )
            Brand.objects.update_or_create(key=brand["key"], defaults=defaults)

        Shop.objects.update_or_create(
            key="casablanca-bourgogne",
            defaults={
                "current": True,
                "map_query": "Vape & More, 4 Rue Ibnou Jahir, Bourgogne, Maroc",
                "directions_url": "https://maps.google.com/?q=4+Rue+Ibnou+Jahir,+Bourgogne,+Maroc",
                "sort_order": 1,
                "is_active": True,
                **localized(
                    "name",
                    {
                        "fr": "Vape & More Bourgogne",
                        "ar": "Vape & More بورغون",
                        "en": "Vape & More Bourgogne",
                        "es": "Vape & More Bourgogne",
                    },
                ),
                **localized(
                    "address",
                    {
                        "fr": "4 Rue Ibnou Jahir, Bourgogne, Maroc",
                        "ar": "4 شارع ابن جاهير، بورغون، المغرب",
                        "en": "4 Rue Ibnou Jahir, Bourgogne, Morocco",
                        "es": "4 Rue Ibnou Jahir, Bourgogne, Marruecos",
                    },
                ),
                **localized(
                    "hours",
                    {
                        "fr": "Ouvert tous les jours de 09h00 à 23h00",
                        "ar": "مفتوح يوميا من 09:00 إلى 23:00",
                        "en": "Open every day from 09:00 to 23:00",
                        "es": "Abierto todos los días de 09:00 a 23:00",
                    },
                ),
            },
        )

        packs = [
            {
                "key": "solo-vape",
                "discount_label": "-10%",
                "old_price": "225 DH",
                "price": "205 DH",
                "image_path": "/assets/promos/SOLO PACK 01.png",
                "gallery": [
                    "/assets/promos/SOLO PACK 01.png",
                    "/assets/promos/SOLO PACK 02.png",
                    "/assets/promos/SOLO PACK 03.png",
                ],
                "sort_order": 1,
                "texts": {
                    "fr": {
                        "title": "Solo Vape",
                        "target": "1 vape Nerd 20K au choix",
                        "description": "Faites défiler les 3 vapes solo disponibles et choisissez votre saveur.",
                        "whatsapp_message": "Bonjour, je veux commander le pack Solo Vape Nerd 20K.",
                    },
                    "ar": {
                        "title": "Solo Vape",
                        "target": "جهاز Nerd 20K واحد من اختياركم",
                        "description": "تصفحوا أجهزة السولو الثلاثة المتوفرة واختاروا النكهة.",
                        "whatsapp_message": "مرحبا، أريد طلب باقة Solo Vape Nerd 20K.",
                    },
                    "en": {
                        "title": "Solo Vape",
                        "target": "1 Nerd 20K vape of your choice",
                        "description": "Scroll through the 3 available solo vapes and choose your flavor.",
                        "whatsapp_message": "Hello, I would like to order the Solo Vape Nerd 20K pack.",
                    },
                    "es": {
                        "title": "Solo Vape",
                        "target": "1 vape Nerd 20K a elegir",
                        "description": "Desplázate por los 3 vapes solo disponibles y elige tu sabor.",
                        "whatsapp_message": "Hola, quiero pedir el pack Solo Vape Nerd 20K.",
                    },
                },
            },
            {
                "key": "freedom-trio-nerd-20k",
                "discount_label": "-20%",
                "is_best_offer": True,
                "old_price": "675 DH",
                "price": "540 DH",
                "image_path": "/assets/promos/TRIO PACK.png",
                "sort_order": 2,
                "texts": {
                    "fr": {
                        "title": "Freedom Trio Nerd 20K",
                        "target": "3 vapes au choix",
                        "description": "Le pack idéal pour profiter de plusieurs saveurs avec la meilleure réduction.",
                        "whatsapp_message": "Bonjour, je veux commander le pack Freedom Trio Nerd 20K.",
                    },
                    "ar": {
                        "title": "Freedom Trio Nerd 20K",
                        "target": "3 أجهزة من اختياركم",
                        "description": "الباقة المثالية للاستمتاع بعدة نكهات مع أفضل تخفيض.",
                        "whatsapp_message": "مرحبا، أريد طلب باقة Freedom Trio Nerd 20K.",
                    },
                    "en": {
                        "title": "Freedom Trio Nerd 20K",
                        "target": "3 vapes of your choice",
                        "description": "The ideal pack for enjoying several flavors with the best discount.",
                        "whatsapp_message": "Hello, I would like to order the Freedom Trio Nerd 20K pack.",
                    },
                    "es": {
                        "title": "Freedom Trio Nerd 20K",
                        "target": "3 vapes a elegir",
                        "description": "El pack ideal para disfrutar varios sabores con el mejor descuento.",
                        "whatsapp_message": "Hola, quiero pedir el pack Freedom Trio Nerd 20K.",
                    },
                },
            },
            {
                "key": "freedom-duo-drink",
                "discount_label": "-15%",
                "old_price": "464 DH",
                "price": "399 DH",
                "image_path": "/assets/promos/DUO PACK + DRINK.png",
                "sort_order": 3,
                "texts": {
                    "fr": {
                        "title": "Freedom Duo + Boisson",
                        "target": "2 vapes au choix + boisson offerte",
                        "description": "Deux Nerd 20K avec une boisson offerte pour compléter votre pack.",
                        "whatsapp_message": "Bonjour, je veux commander le pack Freedom Duo + Boisson.",
                    },
                    "ar": {
                        "title": "Freedom Duo + مشروب",
                        "target": "جهازان من اختياركم + مشروب هدية",
                        "description": "جهازا Nerd 20K مع مشروب هدية لإكمال الباقة.",
                        "whatsapp_message": "مرحبا، أريد طلب باقة Freedom Duo + مشروب.",
                    },
                    "en": {
                        "title": "Freedom Duo + Drink",
                        "target": "2 vapes of your choice + free drink",
                        "description": "Two Nerd 20K vapes with a free drink to complete your pack.",
                        "whatsapp_message": "Hello, I would like to order the Freedom Duo + Drink pack.",
                    },
                    "es": {
                        "title": "Freedom Duo + Bebida",
                        "target": "2 vapes a elegir + bebida gratis",
                        "description": "Dos Nerd 20K con una bebida gratis para completar tu pack.",
                        "whatsapp_message": "Hola, quiero pedir el pack Freedom Duo + Bebida.",
                    },
                },
            },
            {
                "key": "freedom-duo-mix",
                "discount_label": "-15%",
                "old_price": "415 DH",
                "price": "355 DH",
                "image_path": "/assets/promos/DUO PACK.png",
                "sort_order": 4,
                "texts": {
                    "fr": {
                        "title": "Freedom Duo Mix",
                        "target": "1 Nerd 5.5K + 1 Nerd 20K au choix",
                        "description": "Le duo mix parfait pour découvrir deux formats en une seule offre.",
                        "whatsapp_message": "Bonjour, je veux commander le pack Freedom Duo Mix.",
                    },
                    "ar": {
                        "title": "Freedom Duo Mix",
                        "target": "Nerd 5.5K واحد + Nerd 20K واحد",
                        "description": "الثنائي المثالي لاكتشاف حجمين في عرض واحد.",
                        "whatsapp_message": "مرحبا، أريد طلب باقة Freedom Duo Mix.",
                    },
                    "en": {
                        "title": "Freedom Duo Mix",
                        "target": "1 Nerd 5.5K + 1 Nerd 20K of your choice",
                        "description": "The perfect duo to discover two formats in one offer.",
                        "whatsapp_message": "Hello, I would like to order the Freedom Duo Mix pack.",
                    },
                    "es": {
                        "title": "Freedom Duo Mix",
                        "target": "1 Nerd 5.5K + 1 Nerd 20K a elegir",
                        "description": "El dúo perfecto para descubrir dos formatos en una sola oferta.",
                        "whatsapp_message": "Hola, quiero pedir el pack Freedom Duo Mix.",
                    },
                },
            },
        ]
        for pack_data in packs:
            gallery = pack_data.pop("gallery", [])
            texts = pack_data.pop("texts")
            defaults = {"is_active": True, "is_best_offer": False, **pack_data}
            defaults.update(
                localized_group(
                    {
                        "title": "title",
                        "target": "target",
                        "description": "description",
                        "whatsapp_message": "whatsapp_message",
                    },
                    texts,
                )
            )
            pack, _ = PromotionPack.objects.update_or_create(
                key=pack_data["key"], defaults=defaults
            )
            if not gallery:
                gallery = [pack.image_path]
            for index, image_path in enumerate(gallery, start=1):
                PromotionPackImage.objects.update_or_create(
                    pack=pack,
                    sort_order=index,
                    defaults={
                        "image_path": image_path,
                        "alt_fr": pack.title_fr,
                        "alt_ar": pack.title_ar,
                        "alt_en": pack.title_en,
                        "alt_es": pack.title_es,
                        "is_active": True,
                    },
                )

        products = [
            {
                "key": "nerd-20k-yellow",
                "brand": "nerd",
                "image_path": "/assets/promos/promo_1.png",
                "price": {"fr": "225 DH", "ar": "225 DH", "en": "225 DH", "es": "225 DH"},
                "sort_order": 1,
                "texts": {
                    "fr": {
                        "name": "Nerd 20K Yellow",
                        "description": "Format Nerd 20K disponible en boutique.",
                        "flavors": ["Saveurs à confirmer en boutique"],
                    },
                    "ar": {
                        "name": "Nerd 20K Yellow",
                        "description": "طراز Nerd 20K متوفر في المتجر.",
                        "flavors": ["يرجى تأكيد النكهات داخل المتجر"],
                    },
                    "en": {
                        "name": "Nerd 20K Yellow",
                        "description": "Nerd 20K format available in store.",
                        "flavors": ["Flavors to confirm in store"],
                    },
                    "es": {
                        "name": "Nerd 20K Yellow",
                        "description": "Formato Nerd 20K disponible en tienda.",
                        "flavors": ["Sabores a confirmar en tienda"],
                    },
                },
            },
            {
                "key": "nerd-20k-red",
                "brand": "nerd",
                "image_path": "/assets/promos/SOLO PACK 01.png",
                "price": {"fr": "225 DH", "ar": "225 DH", "en": "225 DH", "es": "225 DH"},
                "sort_order": 2,
                "texts": {
                    "fr": {
                        "name": "Nerd 20K Red",
                        "description": "Version rouge du Nerd 20K, disponible seule ou en pack promotionnel.",
                        "flavors": ["Saveurs à confirmer en boutique"],
                    },
                    "ar": {
                        "name": "Nerd 20K Red",
                        "description": "نسخة Nerd 20K الحمراء، متوفرة منفردة أو ضمن باقة.",
                        "flavors": ["يرجى تأكيد النكهات داخل المتجر"],
                    },
                    "en": {
                        "name": "Nerd 20K Red",
                        "description": "Red Nerd 20K version, available solo or in promotional packs.",
                        "flavors": ["Flavors to confirm in store"],
                    },
                    "es": {
                        "name": "Nerd 20K Red",
                        "description": "Versión roja de Nerd 20K, disponible sola o en packs promocionales.",
                        "flavors": ["Sabores a confirmar en tienda"],
                    },
                },
            },
            {
                "key": "nerd-20k-green",
                "brand": "nerd",
                "image_path": "/assets/promos/SOLO PACK 03.png",
                "price": {"fr": "225 DH", "ar": "225 DH", "en": "225 DH", "es": "225 DH"},
                "sort_order": 3,
                "texts": {
                    "fr": {
                        "name": "Nerd 20K Green",
                        "description": "Version verte du Nerd 20K, disponible seule ou en pack promotionnel.",
                        "flavors": ["Saveurs à confirmer en boutique"],
                    },
                    "ar": {
                        "name": "Nerd 20K Green",
                        "description": "نسخة Nerd 20K الخضراء، متوفرة منفردة أو ضمن باقة.",
                        "flavors": ["يرجى تأكيد النكهات داخل المتجر"],
                    },
                    "en": {
                        "name": "Nerd 20K Green",
                        "description": "Green Nerd 20K version, available solo or in promotional packs.",
                        "flavors": ["Flavors to confirm in store"],
                    },
                    "es": {
                        "name": "Nerd 20K Green",
                        "description": "Versión verde de Nerd 20K, disponible sola o en packs promocionales.",
                        "flavors": ["Sabores a confirmar en tienda"],
                    },
                },
            },
            {
                "key": "crown-bar-al-fakher",
                "brand": "crown-bar-al-fakher",
                "image_path": "/assets/photo-01.png",
                "price": {
                    "fr": "Prix en DH à confirmer",
                    "ar": "السعر بالدرهم قيد التأكيد",
                    "en": "Price in DH to be confirmed",
                    "es": "Precio en DH por confirmar",
                },
                "sort_order": 4,
                "texts": {
                    "fr": {
                        "name": "Crown Bar Al Fakher",
                        "description": "Informations à compléter dans le catalogue dès réception des photos, saveurs et prix exacts.",
                        "flavors": ["À compléter"],
                    },
                    "ar": {
                        "name": "Crown Bar Al Fakher",
                        "description": "سيتم استكمال التفاصيل في الكتالوغ عند توفر الصور والنكهات والأسعار الدقيقة.",
                        "flavors": ["سيتم استكمالها"],
                    },
                    "en": {
                        "name": "Crown Bar Al Fakher",
                        "description": "Catalog information will be completed once exact photos, flavors, and prices are available.",
                        "flavors": ["To be completed"],
                    },
                    "es": {
                        "name": "Crown Bar Al Fakher",
                        "description": "La información del catálogo se completará cuando estén disponibles las fotos, los sabores y los precios exactos.",
                        "flavors": ["Por completar"],
                    },
                },
            },
            {
                "key": "adalya-selection",
                "brand": "adalya",
                "image_path": "/assets/photo-02.png",
                "price": {
                    "fr": "Prix en DH à confirmer",
                    "ar": "السعر بالدرهم قيد التأكيد",
                    "en": "Price in DH to be confirmed",
                    "es": "Precio en DH por confirmar",
                },
                "sort_order": 5,
                "texts": {
                    "fr": {
                        "name": "Sélection Adalya",
                        "description": "Informations à compléter dans le catalogue dès réception des photos, saveurs et prix exacts.",
                        "flavors": ["À compléter"],
                    },
                    "ar": {
                        "name": "تشكيلة Adalya",
                        "description": "سيتم استكمال التفاصيل في الكتالوغ عند توفر الصور والنكهات والأسعار الدقيقة.",
                        "flavors": ["سيتم استكمالها"],
                    },
                    "en": {
                        "name": "Adalya Selection",
                        "description": "Catalog information will be completed once exact photos, flavors, and prices are available.",
                        "flavors": ["To be completed"],
                    },
                    "es": {
                        "name": "Selección Adalya",
                        "description": "La información del catálogo se completará cuando estén disponibles las fotos, los sabores y los precios exactos.",
                        "flavors": ["Por completar"],
                    },
                },
            },
        ]
        for product in products:
            texts = product.pop("texts")
            prices = product.pop("price")
            brand = Brand.objects.get(key=product.pop("brand"))
            defaults = {"brand": brand, "is_active": True, **product}
            defaults.update(localized("price", prices))
            defaults.update(
                localized_group(
                    {
                        "name": "name",
                        "description": "description",
                        "flavors": "flavors",
                    },
                    texts,
                )
            )
            Product.objects.update_or_create(key=product["key"], defaults=defaults)

        self.stdout.write(self.style.SUCCESS("Vape & More public content seeded."))
