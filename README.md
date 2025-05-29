Веб приложение, использующее сторонние API для предоставления данных о погоде в разных городах на 16 дней вперед.

## Стек технологий ##
__Языки программирования__ - Python 3.9.13
__requests 2.32.3__ - библиотека для выполнения HTTP-запросов
__Django 3.2.16__ - высокоуровневый Python-фреймворк для веб-разработки



### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Egor-lazarev/o-complex.git

или

git clone git@github.com:Egor-lazarev/o-complex.git
```

```
cd o-complex
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

для windows: python -m venv venv

```
source venv/bin/activate
```
для windows: source venv/Scripts/activate

```
python3 -m pip install --upgrade pip
```
для windows: python -m pip install --upgrade pip

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```
для windows: python manage.py migrate

Запустить проект:

```
python3 manage.py runserver

для windows: python manage.py runserver