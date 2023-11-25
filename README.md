# Hack the planet hackathon project

By PJATK team

 * Paweł Czapiewski
 * Tadeusz Puźniakowski
 * Weronika Sadowska
 


# Run

I Assume no IDE - this is how we can start project on headless computer (server)
```sh
python3 -m venv ./venv
. ./venv/bin/activate
pip install tensorflow==2.15.0; pip install django Django==4.2
cd htp
python manage.py migrate
python manage.py runserver
```
The server will be at 


# Additional documentation

* [Django](https://docs.djangoproject.com/en/4.2/intro/tutorial01/)
