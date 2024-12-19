from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import StudentRegistrationForm, TeacherRegistrationForm
from .models import CustomUser
from django.utils.timezone import now
from datetime import datetime, timedelta
from .models import Schedule
import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserSubscription
from uuser.models import CustomUser


logger = logging.getLogger(__name__)

def register_student(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'student'  # Устанавливаем роль
            user.save()
            login(request, user)  # Логиним пользователя сразу
            return redirect('student_page')
        else:
            logger.warning(f"Ошибка регистрации студента: {form.errors}")
    else:
        form = StudentRegistrationForm()
    return render(request, 'uuser/register_student.html', {'form': form})

def register_teacher(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'teacher'  # Устанавливаем роль
            user.save()
            login(request, user)  # Логиним пользователя сразу
            return redirect('teacher_page')
        else:
            logger.warning(f"Ошибка регистрации учителя: {form.errors}")
    else:
        form = TeacherRegistrationForm()
    return render(request, 'uuser/register_teacher.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Перенаправляем в зависимости от роли
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

@login_required
def schedule_view(request):
    user = request.user

    # Проверяем авторизацию и роль пользователя
    if not user.is_authenticated or user.role not in ['student', 'teacher']:
        return render(request, 'uuser/access_denied.html')

    # Дата 1 сентября текущего года
    current_date = now().date()
    year = current_date.year
    first_september = datetime(year, 9, 1).date()
    if current_date < first_september:
        first_september = datetime(year - 1, 9, 1).date()

    # Рассчитываем текущую неделю
    delta_days = (current_date - first_september).days
    current_week = delta_days // 7 + 1

    selected_week = request.GET.get('week', current_week)
    try:
        selected_week = int(selected_week)
    except ValueError:
        selected_week = current_week

    start_of_week = first_september + timedelta(weeks=(selected_week - 1))
    end_of_week = start_of_week + timedelta(days=6)

    if user.role == 'student' and hasattr(user, 'student_profile'):
        student_group = user.student_profile.group
        schedules = Schedule.objects.filter(
            groups=student_group,
            date_time__date__range=(start_of_week, end_of_week)
        )
    elif user.role == 'teacher':
        schedules = Schedule.objects.filter(
            teachers=user,
            date_time__date__range=(start_of_week, end_of_week)
        )
    else:
        schedules = []

    total_weeks = ((datetime(year + 1, 6, 30).date() - first_september).days) // 7 + 1

    return render(request, 'uuser/schedule.html', {
        'schedules': schedules,
        'selected_week': selected_week,
        'current_week': current_week,
        'start_of_week': start_of_week,
        'end_of_week': end_of_week,
        'weeks_range': range(1, total_weeks + 1),
    })

@csrf_exempt
@login_required
def save_subscription(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Чтение данных из запроса
            UserSubscription.objects.create(
                user=request.user,
                subscription=json.dumps(data)  # Сохранение подписки в базу
            )
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error"}, status=400)



