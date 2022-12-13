from celery import Celery
from worker.schedules import all_schedules


def config(REDIS_URL, CELERY_BROKER_URL, CELERY_RESULT_URL):
    '''
    TimeZone is set to Tehran
    Connection is to mongo
    Tasks are stored at celery_schedules.p
    '''

    celery_instance = Celery(
        "BT",
        include=[

            'Worker.jobs',
        ],
    )

    celery_instance.conf.broker_url = \
        CELERY_BROKER_URL or \
        REDIS_URL
    celery_instance.conf.result_backend = \
        CELERY_RESULT_URL or \
        REDIS_URL

    # We're using TCP keep-alive instead
    celery_instance.conf.broker_heartbeat = None

    # print({"celery_instance.conf" : celery_instance.conf})

    celery_instance.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='Asia/Tehran',
        enable_utc=True,
        mongodb_backend_settings={
            'database': 'celery',
            'taskmeta_collection': 'tasks_meta',
        },
        broker_heartbeat=2,
        worker_pool_restarts=True,
        worker_hijack_root_logger=False,
        worker_redirect_stdouts=False
    )

    gelf_config.config(
        celery_instance.log.get_default_logger(),
        "CeleryV2"
    )
    gelf_config.config(
        celery_instance.log.setup_task_loggers(),
        "CeleryV2.workers"
    )

    celery_instance.conf.beat_schedule = all_schedules

    return celery_instance
