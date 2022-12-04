from celery.schedules import crontab

from app.models import Chain


def generate_tasks():
    chain_ids = Chain.supported_chains()
    tasks = {"save_func_selectors":
             {
                 'func_selector': {
                     'task': 'save_func_selectors',
                     'schedule': crontab(hour='*/24')

                 }
             }
             }

    for chain_id in chain_ids:
        name = Chain(chainId=chain_id).chain_name
        tasks[name] = {
            'save_pairs': {
                'task': 'save_pairs',
                'schedule': crontab(hour='*/24'),
                'kwargs': {
                        'chain_id': chain_id
                }
            },
            'update_pairs': {
                'task': 'update_pairs',
                'schedule': crontab(minute='*/30'),
                'kwargs': {
                        'chain_id': chain_id
                }
            }
        }
    return tasks


_all_tasks = generate_tasks()


all_schedules = {}

for cat in _all_tasks:
    for task_name, task_det in _all_tasks[cat].items():
        all_schedules.update({task_name: task_det})
