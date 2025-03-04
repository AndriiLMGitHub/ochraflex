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
    combined_blocks = CombinedBlock.objects.filter(block_template=block_template)

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
            field_value = request.POST.get(f"field_{field.id}", "").strip()
            if field_value:
                FieldResponse.objects.create(
                    survey_response=survey_response,
                    field=field,
                    value=field_value
                )

        # Збереження відповідей для описових блоків
        # for description_field in description_fields:
        #     desc_value = request.POST.get(f"description_{description_field.id}", "").strip()
        #     if desc_value:
        #         FieldResponse.objects.create(
        #             survey_response=survey_response,
        #             field=None,
        #             value=desc_value
        #         )

        # Збереження відповідей для комбінованих блоків
        for combined_block in combined_blocks:
            combined_value = request.POST.get(f"combined_block_{combined_block.id}", "").strip()
            if combined_value:
                FieldResponse.objects.create(
                    survey_response=survey_response,
                    combined_block=combined_block,
                    value=combined_value
                )

        messages.success(request, "Анкету успішно відправлено!")
        return redirect("survey_detail", block_id=block_template.id)

    return render(request, "survey/submit_survey.html", {
        "block_template": block_template,
        "fields": fields,
        "description_fields": description_fields,
        "combined_blocks": combined_blocks
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
