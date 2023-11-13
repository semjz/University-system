Pyvengers group project


## celery
### setup requirements
* to start celery worker and using it, there are some prerequisite such as rabbitmq, docker, redis etc. but we use redis because of its ease of use and accessibility.

you need to start redis first. The most important field that needed to be in settings.py is CELERY_BROKER_URL. In bellow, you can see all fields that required in settings.py
```python
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'  # generally your redis host and port
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Tehran'

CELERY_RESULT_BACKEND = 'django-db'
```
Then you should add `celery` to your INSTALLED_APPS.

### celery.py
After that, you must create `celery.py` next to `settings.py` as bellow:
```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Tehran')
app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

```

The most important parts of the code above are:
1. `os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')`: To tell celery to use these settings.
2. `app = Celery('config')`: Creates an instance from Celery with the name `config`.
3. `app.config_from_object(settings, namespace='CELERY')`: This line tells to celery to use django settings and put celery settings to namespace `CELERY`.
4. `app.autodiscover_tasks()`: With this line celery discovers all tasks in project.

### tasks.py
then you have to create a `tasks.py` file in your app to define tasks that celery should follow. this file is something like this:
```python
from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Done"
```
The most important parts of the code above are:
1. `@shared_task(bind=True)`: This is a decorator to introduce tasks to celery and the parameter `bind` defines the self parameter as an object.
2. `test_func` is a test function to show you how to implement, here you can implement your functions and tasks that celery uses.

* You can create a task and use that task in your views. For example: you can write a `send_email` task and use this task in your registration view to send a registration email to the user while authentication is happening.

### celery commands
There are some commands that you should use to start a celery worker and use celery services:
1. `celery -A config.celery worker --pool=solo -l info`: This command starts a worker to listen to requests and do the tasks. the field `--pool=solo` is not necessary and is for Windows users.
2. `celery -A config beat -l info`: This command is for celery beat that will introduce in future...