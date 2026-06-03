import asyncio

from functools import wraps

from .consumer import dispatcher




def confirm_mail(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):

        if asyncio.iscoroutinefunction(func):
            response = await func(*args, **kwargs)
        else:
            response = func(*args, **kwargs)

        dispatcher.put_nowait({'type': 'auth', 'response': response})

        return response

    return wrapper


def update_stage(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):

        if asyncio.iscoroutinefunction(func):
            response = await func(*args, **kwargs)
        else:
            response = func(*args, **kwargs)

        dispatcher.put_nowait({'type': 'stage', 'response': response})

        return response

    return wrapper