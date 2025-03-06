from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from survey.models import SurveyResponse, FieldResponse
from app.models import BlockTemplate, DescriptionField, Field, CombinedBlock


def submit_survey_response(request, block_id):
    """Обробка надсилання відповіді на анкету анонімними та авторизованими користувачами."""
    block_template = get_object_or_404(BlockTemplate, id=block_id)
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
                return redirect("submit_survey", block_id=block_id)

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

                if field.field_type == Field.CHECKBOX:
                    field_value = ", ".join(request.POST.getlist(field_name))
                elif field.field_type == Field.RADIO:
                    field_value = request.POST.get(field_name, "").strip()
                else:
                    field_value = request.POST.get(field_name, "").strip()

                if field_value:
                    FieldResponse.objects.create(
                        survey_response=survey_response,
                        field=field,
                        value=field_value,
                        combined_block=combined_block  # Прив'язка до комбінованого блоку
                    )

        for template in block_template.library_templates.all():
            if template.field:
                field_name = f"field_{template.field.id}"

                if template.field.field_type == Field.CHECKBOX:
                    field_value = ", ".join(request.POST.getlist(field_name))
                elif template.field.field_type == Field.RADIO:
                    field_value = request.POST.get(field_name, "").strip()
                else:
                    field_value = request.POST.get(field_name, "").strip()

                if field_value:
                    FieldResponse.objects.create(
                        survey_response=survey_response,
                        field=template.field,  
                        value=field_value,
                        combined_block=template.combined_block  # Додаємо прив’язку, якщо потрібно
                    )
            elif template.combined_block:
                for field in template.combined_block.fields.all():
                    if field:
                        field_name = f"field_{field.id}"

                        if field.field_type == Field.CHECKBOX:
                            field_value = ", ".join(request.POST.getlist(field_name))
                        elif field.field_type == Field.RADIO:
                            field_value = request.POST.get(field_name, "").strip()
                        else:
                            field_value = request.POST.get(field_name, "").strip()

                        if field_value:
                            FieldResponse.objects.create(
                                survey_response=survey_response,
                                field=field,
                                value=field_value,
                                combined_block=template.combined_block  # Додаємо прив’язку, якщо потрібно
                            )

        messages.success(request, "Анкету успішно відправлено!")
        return redirect("survey_detail", block_id=block_template.id)
    

    return render(request, "survey/submit_survey.html", {
        "block_template": block_template,
        "fields": fields,
        "description_fields": description_fields,
        "combined_blocks": combined_blocks,
    })


@login_required
def survey_detail_view(request, block_id):
    """Деталі відповідей на анкету."""
    block_template = get_object_or_404(BlockTemplate, id=block_id)
    responses = SurveyResponse.objects.filter(block_template=block_template).prefetch_related('field_responses')

    return render(request, "survey/survey_detail.html", {
        "block_template": block_template,
        "responses": responses
    })
