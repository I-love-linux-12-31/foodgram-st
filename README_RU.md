# Foodgram-st
## Описание проекта

Foodgram - это веб-приложение и API для публикации рецептов и составления списка нужных ингредиентов созданые с использованием Django 5. 
Авторизованные пользователи могут публиковать рецепты, добавлять понравившиеся рецепты в избранное, 
подписываться на публикации других авторов и формировать список покупок для выбранных рецептов.

Любые посетители сайта могут изучить каталог рецептов.

**Автор: Кузнецов Ярослав**

## Структура проекта

### Основные компоненты
* backend - API и веб-интерфейс для администратора
* frontend - Интерфейс пользователя
* gateway / nginx - Веб-сервер
* db(Только контейнер, опционально) - База данных: PostgreSQL

### Дополнительные компоненты
* infra - Конфигурация для запуска фронт-энда без других сервисов
* data - Подготовленные заранее данные(ссылка для совместимости)
* docs - документация
* postman-collection - Тесты для API

### Файлы
* docker-compose.yaml - Конфигурация docker-compose 
* docker-example.env - Пример файла с переменными окружения для запуска приложения
* README.md / README_RU.md - Описание проекта
* setup.cfg - Конфигурация линтера

## Технологии
### backend
* Python 3.13
* Django 5.2
* Django REST Framework
* PostgreSQL

### frontend
* React

### другое
* Docker / Podman
* NGINX

## Запуск

### Контейнеризированная версия: Быстрый деплой
Скачивания проекта не требуется!
**Поддерживается только Linux!**

Docker-compose:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/I-love-linux-12-31/foodgram-st/refs/heads/main/docs/fast_deploy.sh)
```
Podman-compose
```bash
USE_PODMAN=1 bash <(curl -fsSL https://raw.githubusercontent.com/I-love-linux-12-31/foodgram-st/refs/heads/main/docs/fast_deploy.sh)
```

Что делает скрипт:
1) Скачивает файлы конфигурации
2) Запускает контейнеры через (docker/podman compose)

### Контейнеризированная версия: Со сборкой
```bash
git clone https://github.com/I-love-linux-12-31/foodgram-st.git
cd foodgram-st
```

Docker-compose
```bash
cp ./docker-example.env ./docker.env # Create .env file from template
# Edit docker.env file 
docker-compose build 
docker-compose up
```

### Запуск только backend сервера
Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate
```

Переменные окружения автоматически загружаются из ``backend/.env`` файла. 
Если он находится в другом каталоге/с другим именем, его потребуется загрузить вручную

Активация .env файла, где ".env" название/путь к файлу.
```bash
set -a
source .env
```

**⚠️ Внимание.** ``DEBUG=1`` помимо отладочного режима указывает бэкенду, что он должен сам обрабатывать запросы к статике, без nginx.

#### Продакшн
```bash

```

#### Сервер разработки

```bash
cd backend
DEBUG=1 ./run_dev_server.sh
```
