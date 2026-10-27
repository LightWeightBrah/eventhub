# EventHub

Platforma wydarzeń i biletów – projekt referencyjny z laboratoriów **Aplikacje WWW** (UWM Olsztyn, semestr 2026Z).
Django 6.1 + Django REST Framework, SQLite.

Zakres na tę chwilę: Lab 1–4 (projekt i aplikacja `events`, modele `Category` i `Event`, Django Admin,
zapytania ORM, szablony MVT, ręczny `EventSerializer`). Kolejne laby będą dopisywane w kolejnych commitach.

## Uruchomienie (Windows, PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

Adresy: <http://127.0.0.1:8000/events/> (lista), <http://127.0.0.1:8000/events/about/>, <http://127.0.0.1:8000/admin/>.

## Przydatne polecenia

```powershell
python -m events.orm_queries              # zapytania QuerySet z Lab 2
python manage.py serializer_shell_test    # generuje events/docs/serializer_shell_test.md (Lab 4)
```
