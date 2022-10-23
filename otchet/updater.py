from apscheduler.schedulers.background import BackgroundScheduler
from .something_update import update_something, print_hola

scheduler = BackgroundScheduler()
scheduler.add_job(update_something, 'interval', seconds=100)
scheduler.add_job(print_hola, 'interval', seconds=50)
