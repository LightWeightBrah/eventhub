"""
Wypełnia bazę przykładowymi danymi (3 kategorie, 5 wydarzeń) - Lab 2, krok 4.

Użycie:
    python manage.py seed_demo
"""
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from events.models import Category, Event


class Command(BaseCommand):
    help = "Tworzy przykładowe kategorie i wydarzenia (można uruchamiać wielokrotnie)."

    def handle(self, *args, **options):
        organizer = User.objects.filter(is_superuser=True).first()
        if organizer is None:
            organizer, _ = User.objects.get_or_create(username='organizator')
            organizer.set_unusable_password()
            organizer.save()

        categories = {}
        for name, slug, desc in [
            ('Technologia', 'technologia', 'Konferencje i meetupy IT.'),
            ('Biznes', 'biznes', 'Wydarzenia branżowe i networkingowe.'),
            ('Warsztaty', 'warsztaty', 'Praktyczne warsztaty projektowe.'),
        ]:
            categories[slug], _ = Category.objects.get_or_create(
                slug=slug, defaults={'name': name, 'description': desc}
            )

        now = timezone.now().replace(minute=0, second=0, microsecond=0)
        events = [
            ('Django Conference 2026', 'django-conference-2026', 'technologia',
             'Dwudniowa konferencja o Django, DRF i nowoczesnym backendzie w Pythonie.',
             'Olsztyn, Centrum Konferencyjne UWM', 20, 300, '149.00'),
            ('Meetup Python Olsztyn', 'meetup-python-olsztyn', 'technologia',
             'Otwarte spotkanie społeczności Pythona. Lightning talki i networking.',
             'Olsztyn, Browar Dziki', 7, 60, '0.00'),
            ('Forum Przedsiębiorców Warmii i Mazur', 'forum-przedsiebiorcow', 'biznes',
             'Spotkanie lokalnych firm, panele dyskusyjne i wymiana kontaktów.',
             'Olsztyn, Hotel Warmiński', 35, 120, '89.00'),
            ('Warsztaty Design i UX', 'warsztaty-design-ux', 'warsztaty',
             'Praktyczne warsztaty projektowania interfejsów, prototypy w Figmie.',
             'Online (link po rejestracji)', 14, 25, '59.00'),
            ('Warsztaty Git dla początkujących', 'warsztaty-git', 'warsztaty',
             'Bezpłatne warsztaty: commity, gałęzie, GitHub i praca w zespole.',
             'Olsztyn, WMiI UWM, sala 101', 10, 30, '0.00'),
        ]
        created = 0
        for title, slug, cat_slug, desc, location, days, capacity, price in events:
            _, was_created = Event.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'category': categories[cat_slug],
                    'organizer': organizer,
                    'description': desc,
                    'location': location,
                    'date': now + timedelta(days=days),
                    'capacity': capacity,
                    'price': Decimal(price),
                    'is_published': True,
                },
            )
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(
            f"Gotowe: {Category.objects.count()} kategorii, "
            f"{Event.objects.count()} wydarzeń (nowych: {created}). "
            f"Organizator: {organizer.username}."
        ))
