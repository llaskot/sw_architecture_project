import asyncio

from app.mailer.mailer import Mailer

dispatcher = asyncio.Queue()

mailer = Mailer()

async def consumer():
    """listener"""
    while True:
        task = await dispatcher.get()
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