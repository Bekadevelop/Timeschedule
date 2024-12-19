from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, TeacherRegistrationForm
from django.utils.timezone import now
from datetime import datetime, timedelta
from .models import Schedule, CustomUser, UserSubscription
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from pywebpush import webpush, WebPushException
import logging

logger = logging.getLogger(__name__)


def register_student(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Сохранение данных формы
            return render(request, 'uuser/register_success.html')
    else:
        form = StudentRegistrationForm()  # Пустая форма для GET-запроса

    return render(request, 'uuser/register_student.html', {'form': form})

def register_teacher(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('dashboard')
            except Exception as e:
                return render(request, 'error.html', {'message': str(e)})
    else:
        form = TeacherRegistrationForm()
    return render(request, 'register_teacher.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == "student":
                return redirect('student_page')
            elif user.role == "teacher":
                return redirect('teacher_page')
        else:
            return render(request, 'uuser/login.html', {'error': 'Invalid username or password'})

    return render(request, 'uuser/login.html')

@login_required
def student_page(request):
    return render(request, 'uuser/student_page.html', {
        'message': f'Привет, студент {request.user.username}!'
    })

@login_required
def teacher_page(request):
    return render(request, 'uuser/teacher_page.html', {
        'message': f'Привет, учитель {request.user.username}!'
    })


def schedule_view(request):
    user = request.user

    # Проверка на авторизацию
    if not user.is_authenticated:
        return render(request, 'uuser/access_denied.html')

    # Проверка роли пользователя
    if user.role not in ['student', 'teacher']:
        return render(request, 'uuser/access_denied.html')

    # Дата 1 сентября текущего года
    current_date = now().date()
    year = current_date.year
    first_september = datetime(year, 9, 1).date()

    # Если текущая дата раньше 1 сентября, используем 1 сентября предыдущего года
    if current_date < first_september:
        first_september = datetime(year - 1, 9, 1).date()

    # Рассчитываем номер текущей недели от 1 сентября
    delta_days = (current_date - first_september).days
    current_week = delta_days // 7 + 1

    # Получаем номер выбранной недели из GET-параметра (по умолчанию текущая неделя)
    selected_week_str = request.GET.get('week', str(current_week))
    try:
        selected_week = int(selected_week_str)
    except ValueError:
        logger.warning(f"Invalid week value: {selected_week_str}")
        selected_week = current_week

    # Рассчитываем начало и конец выбранной недели
    start_of_week = first_september + timedelta(weeks=(selected_week - 1))
    end_of_week = start_of_week + timedelta(days=6)

    # Фильтрация расписания по роли пользователя
    if user.role == 'student':
        if not hasattr(user, 'student_profile') or not user.student_profile.group:
            # print(user.username, user.student_profile.student_groups)
            return render(request, 'uuser/error.html', {
                'message': 'У вас нет профиля студента или группы. Обратитесь к администратору.'
            })
        student_group = user.student_profile.group
        schedules = Schedule.objects.filter(groups=student_group, date_time__date__range=(start_of_week, end_of_week))
    elif user.role == 'teacher':
        schedules = Schedule.objects.filter(teachers=user, date_time__date__range=(start_of_week, end_of_week))

    # Определяем общее количество недель (41 неделя с 1 сентября до 30 июня следующего года)
    total_weeks = ((datetime(year + 1, 6, 30).date() - first_september).days) // 7 + 1

    # Передача данных в шаблон
    context = {
        'schedules': schedules,
        'selected_week': selected_week,
        'current_week': current_week,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'weeks_range': range(1, total_weeks + 1),
    }

    if hasattr(settings, 'VAPID_PUBLIC_KEY'):
        context['vapid_public_key'] = settings.VAPID_PUBLIC_KEY

    return render(request, 'uuser/schedule.html', context)


@csrf_exempt
@login_required
def save_subscription(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # data содержит endpoint, keys и т.д.
        # Сохраняем
        UserSubscription.objects.create(
            user=request.user,
            subscription=json.dumps(data) # просто сохраняем JSON строкой
        )
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"}, status=400)



def push_notification(user_id):
    user_subscriptions = UserSubscription.objects.filter(user_id=user_id)
    for subscription in user_subscriptions:
        data = json.dumps({
            'title': 'Hello',
            'body': 'there',
        })
        try:
            webpush(
                subscription_info=json.loads(subscription.subscription),
                data=data,
                vapid_private_key='./private_key.pem',
                vapid_claims={
                    'sub': 'mailto:{}'.format(settings.ADMIN_EMAIL),
                }
            )
        except WebPushException as ex:
            # print("Error sending push:", ex)
            # # Если ex.response.status_code == 410, то можно удалить подписку из БД
            if ex.response and ex.response.status_code == 410:
                # Если код ответа 410, удаляем устаревшую подписку
                subscription.delete()
                logger.warning(f"Subscription removed due to error 410: {ex}")
            else:
                # Логируем ошибку для других случаев
                logger.error(f"Push notification failed: {ex}")

