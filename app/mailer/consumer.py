import asyncio

from .mailer import Mailer
from ..rents import RentRead

dispatcher = asyncio.Queue()

mailer = Mailer()

async def consumer():
    """listener"""
    while True:
        task = await dispatcher.get()
        if task['type'] == 'auth':
            await process_auth(task['response'])
        if task['type'] == 'stage':
            await process_stage(task['response'])



async def process_auth(task):
    try:
        email = task.get("email")
        code = task.get("cod_for_test")
        await mailer.send_email(
            recipient=email,
            subject="Confirmation Code",
            body=f"Code: {code}"
        )
    except Exception as e:
        print(f"WORKER ERROR: {e}")
    finally:
        dispatcher.task_done()


async def process_stage(task: RentRead):
    try:
        email = task.client.email
        body  = f'Your order has been updated.\nCurrent stage: {task.stage}.\nComments: {task.comment}'
        await mailer.send_email(
            recipient=email,
            subject="Order update",
            body=body
        )
    except Exception as e:
        print(f"WORKER ERROR: {e}")
    finally:
        dispatcher.task_done()