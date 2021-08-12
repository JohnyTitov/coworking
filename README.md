## Coworking center website (Django)
1.  Install this libraries to your python path.
    
        pip install django  
        pip install django-bootstrap4  
        pip install django-phonenumber-field[phonenumbers]  
        pip install Pillow  

2.  Create `migrations` in the database. Then create a `superuser`.       
        
        python manage.py migrate
        python manage.py createsuperuser

3.  After starting the server Django go to http://127.0.0.1:8000/admin and add at least one room.  
    This will allow the calendar to be displayed.


4.  For send messages on e-mail write this code in settings.py:

        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        DEFAULT_FROM_EMAIL = "your_email@mail.ru"
        EMAIL_HOST = 'smtp.mail.ru'
        EMAIL_PORT = 2525
        EMAIL_HOST_USER = "your_email@mail.ru"
        EMAIL_HOST_PASSWORD = "your_password"
        EMAIL_USE_TLS = True