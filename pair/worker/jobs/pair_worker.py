import logging
from worker.worker import celery_instance, TaskWithRetry
from ..a2s import async_run

from app.utils.pair.save_pairs import save_chain_pairs
from app.utils.pair.update_pairs import update_chain_pairs
from app.utils.types import ChainId



@celery_instance.task(
    name="save_pairs",
    base=TaskWithRetry)
def save_pairs(chain_id: ChainId):
    logging.info("Inserting pairs in mongo")
    save_chain_pairs(chain_id)


@celery_instance.task(
    name="update_pairs",
    base=TaskWithRetry)
def update_pairs(chain_id: ChainId):
    logging.info("Updating pairs in mongo")
    update_chain_pairs(chain_id)
