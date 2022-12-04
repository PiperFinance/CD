import logging
from worker.worker import celery_instance, TaskWithRetry
from ..a2s import async_run

from app.utils.transaction.four_bytes_function_selector import save_all_4bytes_function_selectors


@celery_instance.task(
    name="save_func_selectors",
    base=TaskWithRetry)
def save_four_bytes_func_selectors():
    logging.info("Inserting function selectors in redis")
    save_all_4bytes_function_selectors()

