from fastapi import FastAPI

# Импортируем RabbitRouter из faststream, чтобы интегрировать RabbitMQ в FastAPI
from faststream.rabbit.fastapi import RabbitRouter

# Создаем экземпляр приложения FastAPI
# Это главный объект, к которому будем добавлять роуты и middleware
app = FastAPI()

# Создаем экземпляр RabbitRouter
# RabbitRouter позволяет создавать эндпоинты, которые напрямую работают с RabbitMQ
router = RabbitRouter()


# Создаем POST-эндпоинт /order
# Когда клиент отправляет POST-запрос на /order с параметром name, 
# вызывается функция make_order
@router.post('/order')
async def make_order(name: str):
    """
    Эндпоинт для создания нового заказа.

    Параметры:
    - name (str): имя или идентификатор заказа, переданный клиентом

    Логика:
    1. Формируем сообщение в формате 'Новый заказ - {name}'
    2. Отправляем сообщение в очередь RabbitMQ с именем 'orders'
    3. Возвращаем клиенту подтверждение успеха
    """
    # Отправляем сообщение в очередь RabbitMQ
    # router.broker.publish — асинхронная функция, публикует сообщение в указанную очередь
    await router.broker.publish(
        f'Новый заказ - {name}',  # текст сообщения
        queue='orders'           # название очереди в RabbitMQ
    )

    # Возвращаем простой JSON-контракт, который говорит, что запрос обработан успешно
    return {'data': 'SUCCESS!'}


# Подключаем RabbitRouter к нашему FastAPI приложению
# Теперь все роуты из router будут доступны через app
app.include_router(router)
