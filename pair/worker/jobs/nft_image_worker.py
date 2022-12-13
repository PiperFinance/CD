import logging
from worker.worker import celery_instance, TaskWithRetry

from app.utils.nft.save_nft_images import save_chain_nft_images
from app.utils.types import ChainId


@celery_instance.task(
    name="save_nft_images",
    base=TaskWithRetry)
def save_pairs(chain_id: ChainId):
    logging.info("Saving nft images")
    save_chain_nft_images(chain_id)
