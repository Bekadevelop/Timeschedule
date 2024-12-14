from django.utils.timezone import now, timedelta, localtime
from uuser.models import Schedule, CustomUser
from uuser.notifications import push_notification
import logging

logger = logging.getLogger(__name__)


def check_and_send_notifications():
    current_time = localtime()
    time_threshold = current_time + timedelta(minutes=90)
    logger.info(f"Current time: {current_time}, Time threshold: {time_threshold}")

    # Предзагружаем связанные объекты, чтобы уменьшить количество запросов
    upcoming_schedules = (
        Schedule.objects
        .filter(date_time__range=(current_time, time_threshold))
        .select_related('cabinet')
        .prefetch_related('groups', 'teachers', 'groups__students', 'subjects')
    )

    schedule_count = upcoming_schedules.count()
    logger.info(f"Found {schedule_count} upcoming schedules.")

    for schedule in upcoming_schedules:
        groups = schedule.groups.all()
        teachers = schedule.teachers.all()
        students = CustomUser.objects.filter(
            student_groups__in=groups,
            role='student'
        ).distinct()

        # Формируем список названий предметов и групп
        subject_names = ", ".join(subject.name for subject in schedule.subjects.all())
        group_names = ", ".join(group.name for group in groups)

        # Информация о кабинете
        cabinet_info = schedule.cabinet.number if schedule.cabinet else 'not specified'

        # Время занятия
        lesson_time = schedule.date_time.strftime('%H:%M')

        # Рецепиенты - учителя и студенты
        recipients = set(teachers) | set(students)
        logger.info(f"Found {len(recipients)} recipients for schedule ID {schedule.id}.")

        for user in recipients:
            # Устанавливаем разные заголовки для учителей и студентов
            if user.role == 'teacher':
                title = f"Upcoming lesson for {group_names} on {subject_names}"
            else:  # student
                title = f"Upcoming lesson: {subject_names}"

            message = {
                'title': title,
                'body': f"The lesson will start at {lesson_time} in the cabinet {cabinet_info}."
            }

            try:
                push_notification(user.id, message)
                logger.info(f"Notification sent to user ID {user.id}.")
            except Exception as ex:
                logger.error(f"Error sending notification to {user.username}: {repr(ex)}")
