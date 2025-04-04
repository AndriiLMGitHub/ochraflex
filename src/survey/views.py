from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from survey.models import SurveyResponse, FieldResponse, SurveyResponseFavorite
from app.models import BlockTemplate, DescriptionField, Field, CombinedBlock
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from django.templatetags.static import static
from django.conf import settings
from django.utils.html import escape
import io
from django.http import FileResponse
import base64
from django.utils import timezone
import tempfile



def submit_survey_response(request, uuid):
    """Обробка надсилання відповіді на анкету анонімними та авторизованими користувачами."""
    block_template = get_object_or_404(BlockTemplate, uuid=uuid)
    fields = Field.objects.filter(block_template=block_template)
    description_fields = DescriptionField.objects.filter(block_template=block_template)
    combined_blocks = CombinedBlock.objects.filter(block_template=block_template).prefetch_related('fields')


    if request.method == "POST":
        # Перевіряємо, чи користувач авторизований
        if request.user.is_authenticated:
            user = request.user
            email = None
        else:
            user = None
            email = request.POST.get("email", "").strip()

            # Якщо e-mail не заповнений, повертаємо помилку
            if not email:
                messages.error(request, "Будь ласка, введіть e-mail, щоб ми могли зв'язатися з вами.")
                return redirect("submit_survey", uuid=uuid)
            
        # Отримуємо всі поля введення (крім прихованих)
        form_data = {key: value for key, value in request.POST.items() if key.startswith("field_")}

        # Отримуємо час введення та метод введення для кожного поля
        input_times = {key.replace("field_", ""): request.POST.get(f"input_time_{key.replace('field_', '')}", "0") for key in form_data.keys()}
        input_methods = {key.replace("field_", ""): request.POST.get(f"input_method_{key.replace('field_', '')}", "unknown") for key in form_data.keys()}


        # Логування або збереження в базу
        for field_name, value in form_data.items():
            field_id = field_name.replace("field_", "")
            print(f"Поле: {field_name}, Значення: {value}, Час: {input_times.get(field_id, '0')} мс, Метод: {input_methods.get(field_id, 'unknown')}")

        # Створюємо відповідь на анкету
        survey_response = SurveyResponse.objects.create(
            user=user,
            email=email,
            block_template=block_template
        )

        # Збереження відповідей для стандартних полів
        for field in fields:
            field_name = f"field_{field.id}"

            if field.field_type == Field.CHECKBOX:
                # Checkbox може мати кілька значень
                field_value = ", ".join(request.POST.getlist(field_name))  # Об'єднуємо список значень у рядок
            elif field.field_type == Field.RADIO:
                # Radio має лише одне вибране значення
                field_value = request.POST.get(field_name, "").strip()
            else:
                field_value = request.POST.get(field_name, "").strip()

            if field_value and not field.is_combined:
                FieldResponse.objects.create(
                    survey_response=survey_response,
                    field=field,
                    value=field_value
                )

        # Збереження відповідей для комбінових полів
        # Обробка комбінованих блоків та їх полів
        for combined_block in combined_blocks:
            for field in combined_block.fields.all():
                field_name = f"field_{field.id}"
                input_time_name = f"input_time_{field.id}"
                input_method_name = f"input_method_{field.id}"

                if field.field_type == Field.CHECKBOX:
                    field_value = ", ".join(request.POST.getlist(field_name))
                elif field.field_type == Field.RADIO:
                    field_value = request.POST.get(field_name, "").strip()
                else:
                    field_value = request.POST.get(field_name, "").strip()

                # Отримуємо час заповнення та метод введення
                input_time = request.POST.get(input_time_name, "0")
                input_method = request.POST.get(input_method_name, "unknown")

                if field_value:
                    FieldResponse.objects.create(
                        survey_response=survey_response,
                        field=field,
                        value=field_value,
                        combined_block=combined_block,  # Прив'язка до комбінованого блоку
                        input_time=int(input_time),  # Записуємо час у мілісекундах
                        input_method=input_method  # Записуємо метод введення
                    )

        for template in block_template.library_templates.all():
            if template.field:
                field_name = f"field_{template.field.id}"
                input_time_name = f"input_time_{field.id}"
                input_method_name = f"input_method_{field.id}"

                if template.field.field_type == Field.CHECKBOX:
                    field_value = ", ".join(request.POST.getlist(field_name))
                elif template.field.field_type == Field.RADIO:
                    field_value = request.POST.get(field_name, "").strip()
                else:
                    field_value = request.POST.get(field_name, "").strip()

                # Отримуємо час заповнення та метод введення
                input_time = request.POST.get(input_time_name, "0")
                input_method = request.POST.get(input_method_name, "unknown")

                if field_value:
                    FieldResponse.objects.create(
                        survey_response=survey_response,
                        field=template.field,  
                        value=field_value,
                        combined_block=template.combined_block,  # Додаємо прив’язку, якщо потрібно
                        input_time=int(input_time),  # Записуємо час у мілісекундах
                        input_method=input_method  # Записуємо метод введення
                    )
            elif template.combined_block:
                for field in template.combined_block.fields.all():
                    if field:
                        field_name = f"field_{field.id}"
                        input_time_name = f"input_time_{field.id}"
                        input_method_name = f"input_method_{field.id}"

                        if field.field_type == Field.CHECKBOX:
                            field_value = ", ".join(request.POST.getlist(field_name))
                        elif field.field_type == Field.RADIO:
                            field_value = request.POST.get(field_name, "").strip()
                        else:
                            field_value = request.POST.get(field_name, "").strip()

                        # Отримуємо час заповнення та метод введення
                        input_time = request.POST.get(input_time_name, "0")
                        input_method = request.POST.get(input_method_name, "unknown")

                        if field_value:
                            FieldResponse.objects.create(
                                survey_response=survey_response,
                                field=field,
                                value=field_value,
                                combined_block=template.combined_block,  # Додаємо прив’язку, якщо потрібно
                                input_time=int(input_time),  # Записуємо час у мілісекундах
                                input_method=input_method  # Записуємо метод введення
                            )

        messages.success(request, "Анкету успішно відправлено!")
        return redirect("survey_detail", uuid=block_template.uuid, response_id=survey_response.id)
    

    return render(request, "survey/submit_survey.html", {
        "block_template": block_template,
        "fields": fields,
        "description_fields": description_fields,
        "combined_blocks": combined_blocks,
    })


@login_required
def survey_detail_view(request, uuid, response_id):
    """Деталі відповідей на анкету."""
    block_template = get_object_or_404(BlockTemplate, uuid=uuid)
    survey_response = SurveyResponse.objects.get(block_template=block_template, id=response_id)

    current_site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    pre_url = f'{protocol}://{current_site.domain}'

    return render(request, "survey/survey_detail.html", {
        "block_template": block_template,
        "response": survey_response,
        'pre_url': pre_url,
    })

def generate_partial_pdf(request, uuid, response_id):
    block_template = get_object_or_404(BlockTemplate, uuid=uuid)
    survey_response = SurveyResponse.objects.get(block_template=block_template, id=response_id)

    current_site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    pre_url = f'{protocol}://{current_site.domain}'

    context = {
        "block_template": block_template,
        "response": survey_response,
        'pre_url': pre_url,
        'logo_url': request.build_absolute_uri(static('images/main_logo.png')),
        'css_url': request.build_absolute_uri(static('css/pdf-styles.css')),
    }
    # Рендеримо весь HTML-шаблон з контекстом
    html_string = render_to_string('survey/pdf_template.html', context)

    # Створюємо тимчасовий файл для збереження PDF
    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as output_file:
        # Конвертуємо HTML в PDF
        HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(target=output_file.name)

        # Читаємо вміст PDF файлу
        output_file.seek(0)
        pdf_content = output_file.read()

    # Повертаємо PDF як HTTP відповідь
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="output.pdf"'
    response.write(pdf_content)

    return response

def delete_survey_view(request, survey_id):
    """Позначити відповідь як видалену"""
    response = get_object_or_404(SurveyResponse, id=survey_id)
    
    # Перевіряємо, чи не є вже видаленою
    if not response.is_deleted:
        response.is_deleted = True
        response.deleted_at = timezone.now()  # Встановлюємо час видалення
        response.save()
        messages.success(request, 'Відповідь позначена як видалена!')

    return redirect('list_resumes')


def permanently_delete_responses(request):
    """Видалення відповідей, які були позначені як видалені більше ніж 30 днів тому"""
    now = timezone.now()
    
    # Фільтруємо відповіді, які позначені як видалені і пройшло більше 30 днів
    responses_to_permanently_delete = SurveyResponse.objects.filter(
        is_deleted=True,
        deleted_at__lte=now - timezone.timedelta(days=30)
    )
    
    # Видаляємо ці відповіді
    count, _ = responses_to_permanently_delete.delete()
    
    return HttpResponse(f"Було видалено {count} відповідей, старіших за 30 днів.")


def test_pdf_view(request, uuid, response_id):
    block_template = get_object_or_404(BlockTemplate, uuid=uuid)
    survey_response = SurveyResponse.objects.get(block_template=block_template, id=response_id)

    context = {
        'block_template': block_template,
        'response': survey_response,
        'logo_url': request.build_absolute_uri(static('images/main_logo.png')), 
        'css_url': request.build_absolute_uri(static('css/pdf-styles.css')),  # Прив'язка до стилів CSS
    }

    return render(request, "survey/pdf_template.html", context)


def add_to_favorites(request, response_id):
    """Додати відповідь до улюблених користувача."""
    if not request.user.is_authenticated:
        messages.error(request, "Ви повинні бути авторизовані, щоб додавати в улюблені.")
        return redirect('signin')  # чи на сторінку, яка відповідає за логін

    survey_response = get_object_or_404(SurveyResponse, id=response_id)

    # Перевірка, чи вже є в улюблених
    if SurveyResponseFavorite.objects.filter(user=request.user, survey_response=survey_response).exists():
        messages.error(request, "Ця відповідь вже в улюблених.")
    else:
        SurveyResponseFavorite.objects.create(user=request.user, survey_response=survey_response)
        messages.success(request, "Відповідь додано до улюблених.")

    return redirect('list_resumes')


def remove_from_favorites(request, response_id):
    """Видалити відповідь з улюблених користувача."""
    if not request.user.is_authenticated:
        messages.error(request, "Ви повинні бути авторизовані, щоб видаляти з улюблених.")
        return redirect('signin')

    survey_response = get_object_or_404(SurveyResponse, id=response_id)

    # Видалення з улюблених
    favorite = SurveyResponseFavorite.objects.filter(user=request.user, survey_response=survey_response).first()
    if favorite:
        favorite.delete()
        messages.success(request, "Відповідь видалено з улюблених.")
    else:
        messages.info(request, "Ця відповідь не була у ваших улюблених.")

    return redirect('list_resumes')
