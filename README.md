# Поисковик по текстам документов с использованием PostgreSQL и Elasticsearch

## Установка

1. Клонируйте репозиторий.
2. Запустите Docker Compose:
    ```bash
    docker-compose up --build
    ```
2. Создайте виртуальное окружение и активируйте его:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

## Запуск

1. Запустите Daemon:
    ```bash
    "C:\Program Files\Docker\Docker\DockerCli.exe" -SwitchDaemon
    ```
2. Запустите Docker:
    ```bash
    docker-compose up --build
    ```
3. Загрузите данные из CSv файла (файл в директории проекта):
    ```bash
    curl -X POST "http://localhost:8000/upload-csv/" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=@posts.csv"
    ```
## Эндпоинты

- `POST /search/` - Поиск по тексту.
- `DELETE /delete/{doc_id}` - Удаление документа.

## Документация

Документация доступна по адресу `http://127.0.0.1:8000/docs`.


