<style>
  * {
    direction: rtl;
  }
</style>

# گزارش بررسی پکیج های مورد نیاز پروژه
### پس از بررسی داکیومنت پروژه و جستجو های انجام شده نتیجه این بررسی به صورت زیر ارائه می شود:

## A. نتیجه دریافتی با استفاده از هوش مصنوعی Google Bard:
    1. django
    2. djangorestframework
    3. psycopg2
    4. celery
    5. redis
    6. docker
    7. django-rest-swagger
    8. minio
    9. nginx
    10. python-dotenv
    11. python-log-formatter

## B. نتیجه دریافتی با استفاده از هوش مصنوعی ChatGPT 3.5:
    1. django
    2. djangorestframework
    3. psycopg2
    4. celery
    5. redis
    6. docker
    7. django-crispy-forms
    8. django-filter
    9. django-rest-swagger
    10. python-decouple
    11. nginx
    12. minio

## C. جمع بندی:
با بررسی مواردی که توسط این دو هوش مصنوعی مطرح شد و جستجوهای انجام شده برخی از این موارد انتخاب شدند که پیاده سازی برخی از آنها روی سرور، داکرو خود جنگو است که در زیر به تفکیک دسته بندی شده اند:

### 1. پکیج های پایتونی که باید روی جنگو نصب شوند:
    - djangorestframework
    - psycopg2
    - celery
    - django-redis
    - django-celery-beat
    - django-filter (اختیاری)
    - django-rest-swagger
    - python-dotenv

### 2. پکیج هایی که باید در داکر پیاده شوند:
    - MinIO
    - PostgreSQL
    - redis
    - celery

### 3. مواردی که باید مستقیم روی سرور پیاده شوند:
    - NginX

### 4. موارد دیگر:
    - log: برای پیاده سازی لاگ هم میتوان از logging در خود جنگو استفاده کرد هم میتوان از کتابخانه های مختلف پایتون مثل 
    logging, logzero,... استفاده کرد
    - translation: برای ترجمه چند راه وجود دارد:
    راه اول استفاده از توابعی مثل gettext که از توابع حود جنگو هست برای ترجمه مدل ها و پیام ها است.
    راه دوم استفاده از پکیج هایی مثل django-rosetta و django-crispy-forms که برای ترجمه فرمها و موارد مربوط به UI می باشد است.

* لطفا موارد فوق را بررسی کنید و اصلاحات مورد نیاز را اعلام فرمایید.
