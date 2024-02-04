from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название опроса")


class SurveySession(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    session = models.CharField(max_length=500, verbose_name="Сессия")


class Question(models.Model):
    name = models.CharField(max_length=500, verbose_name="Вопрос")
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="questions"
    )


class QuestionSession(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    session = models.CharField(max_length=500, verbose_name="Сессия")


class Variant(models.Model):
    name = models.CharField(max_length=500, verbose_name="Вариант ответа")
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="variants"
    )
    next_question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Answer(models.Model):
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        verbose_name="Опрос",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Вопрос",
    )
    chosen_variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        verbose_name="Выбранный вариант ответа",
    )
    session = models.CharField(max_length=500, verbose_name="Сессия")
