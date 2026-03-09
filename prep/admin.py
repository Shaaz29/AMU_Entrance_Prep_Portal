from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Course, MockTest, Question, Result


@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(MockTest)
class MockTestAdmin(ImportExportModelAdmin):
    list_display = ("id", "course", "year", "duration")
    list_filter = ("course", "year")
    search_fields = ("course__name",)


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    list_display = ("id", "mocktest", "type", "text", "correct_answer")
    list_filter = ("mocktest", "type")
    search_fields = ("text",)


@admin.register(Result)
class ResultAdmin(ImportExportModelAdmin):
    list_display = ("id", "user", "mocktest", "score", "date")
    list_filter = ("mocktest", "date")
    search_fields = ("user__username",)