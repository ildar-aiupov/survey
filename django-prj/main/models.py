from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название опроса")

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"


class SurveySession(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name="Опрос")
    session = models.CharField(max_length=500, verbose_name="Сессия")

    class Meta:
        unique_together = ("survey", "session")
        verbose_name = "Опрос-Сессия"
        verbose_name_plural = "Опросы-Сессии"


class Question(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название вопроса")
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="questions", verbose_name="Oпрос"
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class QuestionSession(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name="Вопрос"
    )
    session = models.CharField(max_length=500, verbose_name="Сессия")

    class Meta:
        unique_together = ("question", "session")
        verbose_name = "Вопрос-Сессия"
        verbose_name_plural = "Вопросы-Сессии"


class Variant(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название варианта")
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name="Вопрос",
    )
    next_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Следующий вопрос",
    )

    class Meta:
        verbose_name = "Вариант"
        verbose_name_plural = "Варианты"

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

    class Meta:
        unique_together = ("survey", "question", "session")
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
