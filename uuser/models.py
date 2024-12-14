from django.db import models
from django.contrib.auth.models import AbstractUser


# Кастомная модель пользователя
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username + " " + self.role


# Группа студентов
class StudentGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    students = models.ManyToManyField(CustomUser, related_name="student_groups", limit_choices_to={'role': 'student'}, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Student Group"
        verbose_name_plural = "Student Groups"


# Предмет
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    teachers = models.ManyToManyField(CustomUser, related_name="subject_teachers", limit_choices_to={'role': 'teacher'}, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"


# Кабинет
class Cabinet(models.Model):
    number = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = "Cabinet"
        verbose_name_plural = "Cabinets"


# Расписание
from django.core.exceptions import ValidationError
from django.db import models

from django.core.exceptions import ValidationError
from django.db import models

class Schedule(models.Model):
    groups = models.ManyToManyField('StudentGroup', related_name="schedule_groups")
    subjects = models.ManyToManyField('Subject', related_name="schedule_subjects")
    teachers = models.ManyToManyField('CustomUser', related_name="schedule_teachers", limit_choices_to={'role': 'teacher'})
    cabinet = models.ForeignKey('Cabinet', on_delete=models.SET_NULL, null=True, blank=True, related_name="schedule_entries")
    date_time = models.DateTimeField()
    end_time = models.TimeField()

    # НЕ определяем здесь clean() или убираем любую валидацию, связанную с M2M
    def __str__(self):
        return f"Schedule on {self.date_time.strftime('%Y-%m-%d %H:%M')}"



class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    group = models.ForeignKey(StudentGroup, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"



class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="teacher_profile")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"


from django.db import models

class UserSubscription(models.Model):
    subscription = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriptions')
