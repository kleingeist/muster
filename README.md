# muster
Webapp die Scans historisches Stoffmuster aufbereitet


## Configuration
Put all local configuration to the file `mustersite/local_settings.py` which is loaded by `mustersite/settings.py`. 
For example to setup up your datbase connection you should add the connection parameters to it
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'muster',
        'USER': 'myuser',
        'PASSWORD': 'mypass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
