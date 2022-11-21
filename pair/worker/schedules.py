from celery.schedules import crontab
'''
All celery Tasks
'''

_all_tasks = {

    "Pair":
        {
            'save_pairs': {
                'task': 'save_pairs',
                'schedule': crontab(hour='*/24'),
            },

            'update_pairs': {
                'task': 'update_pairs',
                'schedule': crontab(minute='*/30')
            }
        },
}


all_schedules = {}

for cat in _all_tasks:
    for task_name, task_det in _all_tasks[cat].items():
        all_schedules.update({task_name: task_det})
