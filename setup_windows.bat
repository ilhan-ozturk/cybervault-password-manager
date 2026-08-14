@echo off
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
python manage.py migrate
echo.
echo Setup complete. Before real use, set VAULT_ENCRYPTION_KEY and strong secrets in .env.
echo Start with: python manage.py runserver
