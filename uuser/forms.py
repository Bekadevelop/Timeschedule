from django import forms
from .models import Student, Teacher
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from uuser.models import Schedule, Subject, CustomUser


class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']  # Поля, которые будут отображаться в форме


    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
            Student.objects.create(user=user)
        return user

class TeacherRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'
        if commit:
            user.save()
            Teacher.objects.create(user=user)
        return user




class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        subjects = cleaned_data.get('subjects')
        teachers = cleaned_data.get('teachers')
        cabinet = cleaned_data.get('cabinet')
        date_time = cleaned_data.get('date_time')

        # Проверка связи учителей с предметами
        if subjects and teachers:
            for subject in subjects:
                for teacher in teachers:
                    if teacher not in subject.teachers.all():
                        raise ValidationError(f"Учитель {teacher.username} не связан с предметом {subject.name}.")

        # Проверка занятости учителей
        if subjects and teachers and date_time:
            overlapping_schedules = Schedule.objects.filter(date_time=date_time)
            current_subj_ids = set(subjects.values_list('id', flat=True))
            for sch in overlapping_schedules:
                sch_subj_ids = set(sch.subjects.values_list('id', flat=True))
                for teacher in teachers:
                    if teacher in sch.teachers.all():
                        # Если предметы различаются
                        if current_subj_ids != sch_subj_ids:
                            raise ValidationError(
                                f"Учитель {teacher.username} уже ведёт другой предмет в это время."
                            )

        # Проверка занятости кабинета
        if cabinet and date_time:
            overlapping_cabinet = Schedule.objects.filter(date_time=date_time, cabinet=cabinet)
            if overlapping_cabinet.exists():
                raise ValidationError("Кабинет уже занят в указанное время.")

        return cleaned_data
