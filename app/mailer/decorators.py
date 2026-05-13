import asyncio

from functools import wraps

from app.mailer.consumer import dispatcher




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