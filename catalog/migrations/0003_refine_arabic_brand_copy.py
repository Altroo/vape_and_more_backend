from django.db import migrations


COPY_UPDATES = (
    (
        "crown-bar-al-fakher",
        "علامة فاخرة بهوية قوية، معروضة بوضوح ضمن قسم العلامات التجارية والتذييل.",
        "تعرّف على أجهزة Crown Bar من Al Fakher واختر النكهة التي تناسبك.",
    ),
    (
        "adalya",
        "مجموعة معروفة بغنى النكهات وتنوعها وجودتها المنتظمة.",
        "نكهات متنوعة من Adalya، مع جودة ثابتة وخيارات تناسب مختلف الأذواق.",
    ),
)


def refine_arabic_copy(apps, schema_editor):
    Brand = apps.get_model("catalog", "Brand")
    for key, previous, revised in COPY_UPDATES:
        Brand.objects.using(schema_editor.connection.alias).filter(
            key=key, copy_ar=previous
        ).update(copy_ar=revised)


def restore_arabic_copy(apps, schema_editor):
    Brand = apps.get_model("catalog", "Brand")
    for key, previous, revised in COPY_UPDATES:
        Brand.objects.using(schema_editor.connection.alias).filter(
            key=key, copy_ar=revised
        ).update(copy_ar=previous)


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0002_alter_brand_options_alter_heroimage_options_and_more"),
    ]

    operations = [migrations.RunPython(refine_arabic_copy, restore_arabic_copy)]
