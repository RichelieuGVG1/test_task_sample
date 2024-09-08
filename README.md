# Поисковик по текстам документов

## Установка

1. Клонируйте репозиторий.
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

1. Запустите Elasticsearch:
    ```bash
    docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" elasticsearch:8.4.0
    ```
2. Запустите приложение FastAPI:
    ```bash
    uvicorn main:app --reload
    ```

## Эндпоинты

- `POST /search/` - Поиск по тексту.
- `DELETE /delete/{doc_id}` - Удаление документа.

## Документация

Документация доступна по адресу `http://127.0.0.1:8000/docs`.
