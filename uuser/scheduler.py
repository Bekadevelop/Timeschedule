from apscheduler.schedulers.blocking import BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils.timezone import now
from uuser.check_and_send_notifications import check_and_send_notifications
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

def scheduled_job():
    logger.info("Scheduled job is running...")
    try:
        check_and_send_notifications()
        logger.info(f"check_and_send_notifications запущен в {now()}")
    except Exception as ex:
        logger.error(f"Ошибка в scheduled_job: {repr(ex)}")

def start():
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_jobstore(DjangoJobStore(), "default")
    logger.info("Starting scheduler...")

    # Добавляем задание
    scheduler.add_job(
        scheduled_job,
        trigger='interval',
        minutes=90,
        id="check_and_send_notifications_job",
        replace_existing=True
    )
    logger.info("Scheduler started.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")
