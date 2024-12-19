from django.contrib import admin
from .models import (
    CustomUser, StudentGroup, Subject, Cabinet, Schedule, Student, Teacher, UserSubscription
)
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .forms import ScheduleForm
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):  # Наследуем от UserAdmin для поддержки паролей
    model = CustomUser
    list_display = ('username', 'role', 'email', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),  # Добавляем кастомное поле `role`
    )


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('students',)
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('teachers',)
    search_fields = ('name',)


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    list_display = ('number', 'description')
    search_fields = ('number',)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'end_time', 'get_groups', 'get_subjects', 'get_teachers', 'cabinet')
    filter_horizontal = ('groups', 'subjects', 'teachers')
    form = ScheduleForm  # Используем форму, где вся валидация

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = "Groups"

    def get_subjects(self, obj):
        return ", ".join([subject.name for subject in obj.subjects.all()])
    get_subjects.short_description = "Subjects"

    def get_teachers(self, obj):
        return ", ".join([teacher.username for teacher in obj.teachers.all()])
    get_teachers.short_description = "Teachers"


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'group')
    list_filter = ('group',)
    search_fields = ('user__username',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)


@admin.register(UserSubscription)
class AdminUserSubscription(admin.ModelAdmin):
    list_display = ('user', 'get_shortened_subscription')
    search_fields = ('user__username', 'subscription')

    def get_shortened_subscription(self, obj):
        # Обрезаем подписку для компактного отображения
        return obj.subscription[:50] + "..." if len(obj.subscription) > 50 else obj.subscription
    get_shortened_subscription.short_description = "Subscription"
