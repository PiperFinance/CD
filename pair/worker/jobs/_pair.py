import logging
from worker.worker import celery_instance, TaskWithRetry
from ..a2s import async_run

from app.utils.pair.save_pairs import save_all_pairs
from app.utils.pair.update_pairs import update_all_pairs


@celery_instance.task(
    name="save_pairs",
    base=TaskWithRetry)
def save_pairs():
    logging.info("Inserting pairs in mongo")
    async_run(save_all_pairs())


@celery_instance.task(
    name="update_pairs",
    base=TaskWithRetry)
def update_pairs():
    logging.info("Updating pairs in mongo")
    async_run(update_all_pairs())
