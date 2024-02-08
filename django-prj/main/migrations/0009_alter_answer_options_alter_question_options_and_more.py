# Generated by Django 5.0.1 on 2024-02-08 23:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0008_alter_questionsession_unique_together"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="answer",
            options={"verbose_name": "Ответ", "verbose_name_plural": "Ответы"},
        ),
        migrations.AlterModelOptions(
            name="question",
            options={"verbose_name": "Вопрос", "verbose_name_plural": "Вопросы"},
        ),
        migrations.AlterModelOptions(
            name="questionsession",
            options={
                "verbose_name": "Вопрос-Сессия",
                "verbose_name_plural": "Вопросы-Сессии",
            },
        ),
        migrations.AlterModelOptions(
            name="survey",
            options={"verbose_name": "Опрос", "verbose_name_plural": "Опросы"},
        ),
        migrations.AlterModelOptions(
            name="surveysession",
            options={
                "verbose_name": "Опрос-Сессия",
                "verbose_name_plural": "Опросы-Сессии",
            },
        ),
        migrations.AlterModelOptions(
            name="variant",
            options={"verbose_name": "Вариант", "verbose_name_plural": "Варианты"},
        ),
        migrations.AlterField(
            model_name="question",
            name="survey",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="main.survey",
                verbose_name="Oпрос",
            ),
        ),
        migrations.AlterField(
            model_name="questionsession",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="main.question",
                verbose_name="Вопрос",
            ),
        ),
        migrations.AlterField(
            model_name="survey",
            name="name",
            field=models.CharField(max_length=500, verbose_name="Опрос"),
        ),
        migrations.AlterField(
            model_name="surveysession",
            name="survey",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="main.survey",
                verbose_name="Опрос",
            ),
        ),
        migrations.AlterField(
            model_name="variant",
            name="next_question",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.question",
                verbose_name="Следующий вопрос",
            ),
        ),
        migrations.AlterField(
            model_name="variant",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="variants",
                to="main.question",
                verbose_name="Вопрос",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="answer",
            unique_together={("survey", "question", "session")},
        ),
        migrations.AlterUniqueTogether(
            name="surveysession",
            unique_together={("survey", "session")},
        ),
    ]