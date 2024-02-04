from django.shortcuts import render
from django.db import connection
from django.db.models import Count

from main.models import (
    Survey,
    Question,
    Variant,
    Answer,
    SurveySession,
    QuestionSession,
)
from main.forms import TestForm


def index(request):
    # создаем sessionid, если его еще нет
    if not request.session.session_key:
        request.session.cycle_key()

    # формируем и отрисовываем список опросов, отсекая пройденные данным юзером и пустые (без вопросов в БД)
    passed_surveys_ids = SurveySession.objects.filter(
        session=request.session.session_key
    ).values("survey")
    surveys = (
        Survey.objects.exclude(id__in=passed_surveys_ids)
        .annotate(questions_count=Count("questions"))
        .exclude(questions_count=0)
        .order_by("name")
    )
    context = {"surveys": surveys}
    return render(request, "index.html", context)


def pass_survey(request, survey_id, question_id=None):
    survey = Survey.objects.get(id=survey_id)

    # однократно помечаем опрос меткой сессии как пройденный
    if not SurveySession.objects.filter(
        survey=survey, session=request.session.session_key
    ).exists():
        SurveySession.objects.create(survey=survey, session=request.session.session_key)

    # формируем и отрисовываем первый вопрос
    if request.method != "POST":
        first_question = survey.questions.first()
        form = TestForm(variants=first_question.variants.all().order_by("name"))
        context = {
            "survey": survey,
            "cur_question": first_question,
            "form": form,
            "request": request,
        }
        return render(request, "form_view.html", context)

    # заносим полученный ответ в БД
    form = TestForm(request.POST)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.survey = survey
        answer.question = Question.objects.get(id=question_id)
        answer.session = request.session.session_key
        answer.save()

    # помечаем текущий вопрос меткой сессии как отвеченный
    cur_question = Question.objects.get(id=question_id)
    QuestionSession.objects.create(
        question=cur_question, session=request.session.session_key
    )

    # формируем и отрисовываем следующий вопрос, если есть
    chosen_variant_id = form.data["chosen_variant"]
    chosen_variant = Variant.objects.get(id=chosen_variant_id)
    next_question = chosen_variant.next_question
    if next_question is None:
        context = {
            "message": "Опрос окончен. Вы ответили на все вопросы. Благодарим за участие в опросе!"
        }
        return render(request, "info.html", context=context)
    form = TestForm(variants=next_question.variants.all().order_by("name"))
    context = {
        "survey": survey,
        "cur_question": next_question,
        "form": form,
        "request": request,
    }
    return render(request, "form_view.html", context)


def delete_history(request):
    Answer.objects.all().delete()
    SurveySession.objects.all().delete()
    QuestionSession.objects.all().delete()
    context = {"message": "Вся история прохождения опросов удалена"}
    return render(request, "info.html", context=context)


def show_statistics(request):
    with connection.cursor() as cursor:
        # считаем участников опросов: если никто опросы не проходил, то статистику не выводим
        cursor.execute("SELECT COUNT(DISTINCT(session)) FROM main_answer;")
        users_total = cursor.fetchall()[0][0]
        if users_total == 0:
            context = {
                "message": "На данный момент опросы никто не проходил. Статистики нет."
            }
            return render(request, "info.html", context=context)

        # считаем статистику по вопросам
        cursor.execute(
            """SELECT main_question.id, COUNT(DISTINCT(session)) AS count
            FROM main_question
            LEFT JOIN main_answer ON main_question.id=main_answer.question_id
            GROUP BY main_question.id
            ORDER BY count DESC, main_question.id ASC;"""
        )
        result = cursor.fetchall()
        prev_count = -1
        order_num = 0
        questions_userscount = {}
        questions_info = []
        for question_id, userscount_answered_question in result:
            part = userscount_answered_question * 100 / users_total
            if userscount_answered_question != prev_count:
                prev_count = userscount_answered_question
                order_num += 1
            questions_userscount[question_id] = userscount_answered_question
            new_line = f"Порядковый номер вопроса по кол-ву ответивших {order_num}. Вопрос id={question_id}. Ответило на этот вопрос {userscount_answered_question} участника ({part}% от всех участников опроса)"
            questions_info.append(new_line)

        # считаем статистику по вариантам ответов
        cursor.execute(
            """SELECT main_variant.id, main_variant.question_id, COUNT(DISTINCT(session))
            FROM main_variant
            LEFT JOIN main_answer ON main_variant.id=main_answer.chosen_variant_id
            GROUP BY main_variant.id, main_variant.question_id;"""
        )
        result = cursor.fetchall()
        variants_info = []
        for variant_id, question_id, userscount_chosed_variant in result:
            userscount_answered_question = questions_userscount[question_id]
            new_line = f"Вариант id={variant_id} вопроса id={question_id}. Выбрало этот вариант {userscount_chosed_variant} участников"
            if userscount_answered_question == 0:
                new_line += " (на этот вопрос никто не ответил)"
            else:
                part = userscount_chosed_variant * 100 / userscount_answered_question
                new_line += f" ({part}% от всех ответивших на этот вопрос)"
            variants_info.append(new_line)
    context = {
        "users_total": users_total,
        "questions_info": questions_info,
        "variants_info": variants_info,
    }
    return render(request, "show_statistics.html", context)


def custom_handler404(request, exception):
    return render(request, "custom_handler404.html")


def custom_handler500(request, *args, **kwargs):
    return render(request, "custom_handler500.html")
