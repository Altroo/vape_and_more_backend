from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.utils import timezone


class Command(BaseCommand):
    help = (
        "Prepare an existing username-based database for the accounts.CustomUser "
        "migration before running migrate."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--fallback-domain",
            default="local.invalid",
            help="Domain used when a legacy auth_user row has no email address.",
        )

    def handle(self, *args, **options):
        tables = set(connection.introspection.table_names())
        if "django_migrations" not in tables:
            self.stdout.write(
                self.style.SUCCESS(
                    "No migration history exists yet; run migrate normally."
                )
            )
            return

        custom_user = apps.get_model("accounts", "CustomUser")
        custom_user_table = custom_user._meta.db_table
        migration_recorded = self._migration_recorded()

        if custom_user_table not in tables:
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(custom_user)
            self.stdout.write(self.style.SUCCESS(f"Created {custom_user_table}."))
            tables = set(connection.introspection.table_names())

        with transaction.atomic():
            copied = 0
            if "auth_user" in tables:
                copied = self._copy_legacy_users(custom_user, options["fallback_domain"])
                self.stdout.write(
                    self.style.SUCCESS(f"Copied {copied} legacy auth user(s).")
                )

            if not migration_recorded:
                self._record_initial_migration()
                self.stdout.write(
                    self.style.SUCCESS("Recorded accounts.0001_initial as applied.")
                )

        if copied == 0 and "auth_user" in tables:
            self.stdout.write("No legacy auth users needed copying.")

    def _migration_recorded(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 1
                FROM django_migrations
                WHERE app = %s AND name = %s
                """,
                ["accounts", "0001_initial"],
            )
            return cursor.fetchone() is not None

    def _record_initial_migration(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO django_migrations (app, name, applied)
                VALUES (%s, %s, %s)
                """,
                ["accounts", "0001_initial", timezone.now()],
            )

    def _copy_legacy_users(self, custom_user, fallback_domain):
        copied = 0
        used_emails = set(
            custom_user.objects.values_list("email", flat=True).iterator()
        )
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, username, email, password, first_name, last_name,
                       is_staff, is_active, is_superuser, last_login, date_joined
                FROM auth_user
                ORDER BY id
                """
            )
            columns = [column[0] for column in cursor.description]
            legacy_users = [dict(zip(columns, row, strict=True)) for row in cursor]

        for legacy_user in legacy_users:
            email = self._email_for_legacy_user(
                legacy_user["email"],
                legacy_user["username"],
                fallback_domain,
                used_emails,
            )
            used_emails.add(email)
            _, created = custom_user.objects.update_or_create(
                id=legacy_user["id"],
                defaults={
                    "email": email,
                    "password": legacy_user["password"],
                    "first_name": legacy_user["first_name"],
                    "last_name": legacy_user["last_name"],
                    "is_staff": legacy_user["is_staff"],
                    "is_active": legacy_user["is_active"],
                    "is_superuser": legacy_user["is_superuser"],
                    "last_login": self._aware_datetime(legacy_user["last_login"]),
                    "date_joined": self._aware_datetime(legacy_user["date_joined"]),
                },
            )
            if created:
                copied += 1
        return copied

    def _aware_datetime(self, value):
        if value and timezone.is_naive(value):
            return timezone.make_aware(value, timezone.get_current_timezone())
        return value

    def _email_for_legacy_user(self, email, username, fallback_domain, used_emails):
        candidate = (email or "").strip().lower()
        if not candidate:
            username_part = (username or "admin").strip().lower() or "admin"
            candidate = f"{username_part}@{fallback_domain}"

        if candidate not in used_emails:
            return candidate

        name, separator, domain = candidate.partition("@")
        if not separator:
            name = candidate
            domain = fallback_domain
        index = 2
        while f"{name}-{index}@{domain}" in used_emails:
            index += 1
        return f"{name}-{index}@{domain}"
