import asyncio
import inspect
import json
from functools import wraps
from fastapi import Request

from app.mailer.consumer import dispatcher


def debug_request_response(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # 1. Пытаемся достать Request из аргументов роутера
        # (FastAPI прокидывает его в kwargs, если он указан в сигнатуре)
        request = kwargs.get("request")

        print("\n" + "=" * 50)
        print(f"DEBUG: Calling route: {func.__name__}")

        request: Request = kwargs.get("request")

        print("\n" + "=" * 50)
        print(f"DEBUG: Calling route: {func.__name__}")

        if request and isinstance(request, Request):
            # Читаем сырое тело запроса
            body_bytes = await request.body()

            # Если тело есть, пробуем декодировать из JSON в читаемый вид
            if body_bytes:
                try:
                    body_json = json.loads(body_bytes)
                    print(f"REQUEST BODY: {json.dumps(body_json, indent=2, ensure_ascii=False)}")
                except Exception:
                    print(f"REQUEST BODY (raw): {body_bytes.decode(errors='ignore')}")
            else:
                print("REQUEST BODY: Empty")

            # !!! КРИТИЧЕСКИЙ МОМЕНТ !!!
            # После чтения body() поток пуст. Нужно "перезаправить" его,
            # чтобы Pydantic-модели в роутере смогли его прочитать снова.
            async def receive():
                return {"type": "http.request", "body": body_bytes}

            request._receive = receive

        # 2. Выполняем роутер
        # response = await func(*args, **kwargs)
        if asyncio.iscoroutinefunction(func):
            response = await func(*args, **kwargs)
        else:
            response = func(*args, **kwargs)

        # 3. Печатаем респонс
        print(f"RESPONSE DATA: {response}")
        print("=" * 50 + "\n")

        return response

    return wrapper


def confirm_mail(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):

        if asyncio.iscoroutinefunction(func):
            response = await func(*args, **kwargs)
        else:
            response = func(*args, **kwargs)

        dispatcher.put_nowait(response)

        return response

    return wrapper