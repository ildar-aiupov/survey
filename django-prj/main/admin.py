from django.contrib import admin

from main.models import (
    Survey,
    Question,
    Variant,
    Answer,
    SurveySession,
    QuestionSession,
)


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("pk", "name")


@admin.register(SurveySession)
class SurveySessionAdmin(admin.ModelAdmin):
    list_display = ("pk", "survey", "session")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "survey")


@admin.register(QuestionSession)
class QuestionSessionAdmin(admin.ModelAdmin):
    list_display = ("pk", "question", "session")


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "question", "next_question")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("pk", "survey", "question", "chosen_variant", "session")
