from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from account.forms import ChangeUserForm
from django.contrib import messages
from .models import BlockTemplate, DescriptionField, Field, CombinedBlock, LibraryTemplate
from survey.models import SurveyResponse, FieldResponse
from .forms import BlockTemplateForm, DescriptionFieldForm
from .utils import parse_json
from django.contrib.sites.shortcuts import get_current_site
import json
from django.http import HttpResponse

# Change password imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordChangeForm


@login_required(login_url='/account/signin')
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    user_form = ChangeUserForm(instance=request.user)
    if request.method == 'POST':
        user_form = ChangeUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Профіль успішно оновлено.')
            return redirect('dashboard')

    change_password_form = CustomPasswordChangeForm(user=request.user)
    if request.method == 'POST':
        change_password_form = CustomPasswordChangeForm(
            user=request.user,
            data=request.POST,
        )
        if change_password_form.is_valid():
            user = change_password_form.save()
            # Update the session to keep the user logged in after password change
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Ваш пароль успішно змінено!')
            # Redirect to a relevant page, e.g., profile
            return redirect('dashboard')
        else:
            messages.error(request, 'Виправте помилку нижче.')
    else:
        change_password_form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'dashboard/settings.html', {'form': user_form, 'change_password_form': change_password_form})


def list_resumes_view(request):
    # Logic for listing resumes goes here
    answers = SurveyResponse.objects.all()
    context = {
        'answers': answers,
    }
    return render(request, 'dashboard/resume/resumes.html', context)


def questionnaires_view(request):
    # Logic for questionnaires goes here
    questionnaires = BlockTemplate.objects.filter(user=request.user)
    answers = SurveyResponse.objects.all().count()

    context = {
        'questionnaires': questionnaires,
        'answers': answers,
    }
    return render(request, 'dashboard/questionnaire/questionnaires.html', context)


def add_questionnaire(request):
    # Logic for adding a questionnaire goes here
    if request.method == 'POST':
        form = BlockTemplateForm(request.POST)
        if form.is_valid():
            block_template = form.save(commit=False)
            block_template.user = request.user
            block_template.save()
            messages.success(request, 'Анкету створено успішно!')
            return redirect('questionnaire_detail', id=block_template.id)
        else:
            messages.error(request, 'Виправте помилку нижче.')
    else:
        form = BlockTemplateForm()
    return render(request, 'dashboard/questionnaire/add_questionnaire.html', {'form': form})


def questionnaire_detail(request, id):
    # Logic for displaying questionnaire details goes here
    block_template = BlockTemplate.objects.get(id=id)
    description_fields = DescriptionField.objects.filter(
        block_template=block_template)
    fields = Field.objects.filter(block_template=block_template)
    combined_blocks = CombinedBlock.objects.filter(
        block_template=block_template).prefetch_related('fields')
    

    context = {
        'block_template': block_template,
        'parse_library_fields': None,   
        'description_fields': description_fields,
        'fields': fields,
        'combined_blocks': combined_blocks,
    }

    return render(request, 'dashboard/questionnaire/questionnaire_detail.html', context)


def questionnaire_edit(request, id):
    # Logic for editing a questionnaire goes here
    block_template = BlockTemplate.objects.get(id=id)
    if request.method == 'POST':
        form = BlockTemplateForm(request.POST, instance=block_template)
        if form.is_valid():
            form.save()
            messages.success(request, 'Анкету успішно оновлено')
            return redirect('questionnaire_detail', id=block_template.id)
        else:
            messages.error(request, 'Виправте помилку нижче.')
    else:
        form = BlockTemplateForm(instance=block_template)
    return render(request, 'dashboard/questionnaire/questionnaire_edit.html', {'form': form, 'block_template': block_template})


def delete_questionnaire(request, id):
    # Logic for deleting a questionnaire goes here
    block_template = BlockTemplate.objects.get(id=id)
    block_template.delete()
    messages.success(request, 'Анкету успішно видалено!')
    return redirect('questionnaires')


def add_new_header_block_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)
    form = DescriptionFieldForm()
    if request.method == 'POST':
        form = DescriptionFieldForm(request.POST)
        if form.is_valid():
            description_field = form.save(commit=False)
            description_field.block_template = block_template
            description_field.save()
            messages.success(request, 'Блок заголовка успішно додано')
            return redirect('questionnaire_detail', id=block_template.id)
        else:
            messages.error(request, 'Виправте помилки нижче.')

    context = {
        'block_template': block_template,
        'form': form,
    }
    return render(request, 'dashboard/questionnaire/add_new_header_block.html', context)


def update_header_block_view(request, id):
    description_field = DescriptionField.objects.get(id=id)

    form = DescriptionFieldForm(instance=description_field)
    if request.method == 'POST':
        form = DescriptionFieldForm(request.POST, instance=description_field)
        if form.is_valid():
            form.save()
            messages.success(request, 'Блок заголовка успішно оновлено')
            return redirect('questionnaire_detail', id=description_field.block_template.id)
        else:
            messages.error(request, 'Виправте помилки нижче')

    context = {
        'form': form,
        'description_field': description_field,
    }
    return render(request, 'dashboard/questionnaire/update_header_block.html', context)


def delete_header_block_view(request, id):
    description_field = DescriptionField.objects.get(id=id)
    block_template_id = description_field.block_template.id
    description_field.delete()
    messages.success(request, 'Блок заголовка успішно видалено')
    return redirect('questionnaire_detail', id=block_template_id)


def add_new_field_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/add_new_text_field.html', context)


def add_new_textarea_field_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/add_new_textarea_field.html', context)


def add_new_select_field_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/add_new_select_field.html', context)


def add_new_one_value_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/add_new_one_value.html', context)


def add_new_multiple_value_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/add_new_multiple_value.html', context)


def add_new_boolean_field_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/add_new_yes_or_no.html', context)


def add_new_phone_field_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/add_new_phone_filed.html', context)


def add_new_date_field_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/add_new_date_field.html', context)


# --- Update Questionnaire ----
def update_text_field_view(request, id):
    field = Field.objects.get(id=id)
    block_template = field.block_template

    context = {
        'field': field,
        'block_template': block_template
    }
    return render(request, 'dashboard/questionnaire/edit/edit_text_field.html', context)


def update_textarea_field_view(request, id):
    field = Field.objects.get(id=id)
    block_template = field.block_template

    context = {
        'field': field,
        'block_template': block_template
    }
    return render(request, 'dashboard/questionnaire/edit/edit_textarea_field.html', context)


def update_select_field_view(request, id):
    field = Field.objects.get(id=id)
    block_template = field.block_template

    context = {
        'field': field,
        'options': json.loads(field.options[0]),
        'block_template': block_template
    }
    return render(request, 'dashboard/questionnaire/edit/edit_select_field.html', context)


def edit_one_value_view(request, id):
    field = Field.objects.get(id=id)
    block_template = field.block_template

    context = {
        'field': field,
        'options': json.loads(field.options[0]),
        'block_template': block_template
    }
    return render(request, 'dashboard/questionnaire/edit/edit_one_value.html', context)


def edit_multiple_values_view(request, id):
    field = Field.objects.get(id=id)
    block_template = field.block_template

    context = {
        'field': field,
        'options': json.loads(field.options[0]),
        'block_template': block_template
    }
    return render(request, 'dashboard/questionnaire/edit/edit_multiple_values.html', context)


def edit_yes_or_no_view(request, id):
    field = Field.objects.get(id=id)
    block_template = field.block_template

    context = {
        'field': field,
        # 'options':json.loads(field.options[0]),
        'block_template': block_template
    }
    return render(request, 'dashboard/questionnaire/edit/edit_yes_or_no.html', context)


def edit_phone_field_view(request, id):
    field = Field.objects.get(id=id)
    block_template = field.block_template

    context = {
        'field': field,
        # 'options':json.loads(field.options[0]),
        'block_template': block_template
    }
    return render(request, 'dashboard/questionnaire/edit/edit_phone_field.html', context)


def edit_date_field_view(request, id):
    field = Field.objects.get(id=id)
    block_template = field.block_template

    context = {
        'field': field,
        # 'options':json.loads(field.options[0]),
        'block_template': block_template
    }
    return render(request, 'dashboard/questionnaire/edit/edit_date_field.html', context)

# --- Update Questionnaire ----


def delete_field_view(request, id):
    field = Field.objects.get(id=id)
    block_template = field.block_template
    field.delete()
    messages.success(request, 'Поле видалено успішно!')
    return redirect('questionnaire_detail', id=block_template.id)


# Language Questionnaire View

def de_language_date_field_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/alt-lg/add_de_lang_on_date_filed.html', context)


def de_language_phone_field_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/alt-lg/add_de_lang_on_phone_field.html', context)


def de_language_yes_or_no_field_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/alt-lg/add_de_lang_yes_or_no_field.html', context)


def de_language_multiple_values_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/alt-lg/add_de_lang_multiple_values.html', context)


def de_language_one_value_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/alt-lg/add_de_lang_one_value.html', context)


def de_language_select_field_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/alt-lg/add_de_lang_select_field.html', context)


def de_language_textarea_field_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/alt-lg/add_de_lang_textarea_field.html', context)


def de_language_text_field_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)

    context = {
        'block_template': block_template,
    }
    return render(request, 'dashboard/questionnaire/alt-lg/add_de_lang_text_field.html', context)


# Combine views

def questionnaire_combine_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)
    fields = Field.objects.filter(block_template=block_template)
    description_fields = DescriptionField.objects.filter(
        block_template=block_template)
    combined_blocks = CombinedBlock.objects.filter(
        block_template=block_template)

    fields = Field.objects.filter(block_template=block_template)

    if request.method == 'POST':
        checked_ids = request.POST.getlist('combined')

        # Отримуємо список полів
        fields = Field.objects.filter(
            id__in=checked_ids)
        Field.objects.filter(id__in=checked_ids).update(
            is_combined=True)  # Встановлюємо вибрані
        Field.objects.exclude(id__in=checked_ids).update(
            is_combined=False)  # Знімаємо "is_combined=True" для чекбоксів, які були зняті

        DescriptionField.objects.filter(
            id__in=checked_ids).update(is_combined=True)
        DescriptionField.objects.exclude(
            id__in=checked_ids).update(is_combined=False)

        # Перевіряємо, чи існує CombinedBlock для цього шаблону
        for description_field in description_fields:
            combined_block, created = CombinedBlock.objects.get_or_create(
                block_template=block_template,
                description_field=description_field
            )
            # Perform additional operations on combined_block if needed

        # Оновлюємо поля у CombinedBlock
        combined_block.fields.set(fields)
        combined_block.save()

        if created:
            messages.success(request, 'Комбінація полів створено успішно!')
        else:
            messages.success(request, 'Комбінація полів оновлена успішно!')

        return redirect('questionnaire_combined_detail', id=block_template.id)

    context = {
        'block_template': block_template,
        'fields': fields,
        'description_fields': description_fields,
        'combined_blocks': combined_blocks
    }
    return render(request, 'dashboard/questionnaire/combine/q_detail_combine.html', context)


def dublicate_questionnaire_combined_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)
    fields = Field.objects.filter(block_template=block_template)
    description_fields = DescriptionField.objects.filter(
        block_template=block_template)

    context = {
        'block_template': block_template,
        'fields': fields,
        'description_fields': description_fields,
    }
    return render(request, 'dashboard/questionnaire/combine/q_detail_duplicate.html', context)


def questionnaire_combined_detail_view(request, id):
    block_template = BlockTemplate.objects.get(id=id)
    description_fields = DescriptionField.objects.filter(
        block_template=block_template)
    fields = Field.objects.filter(
        block_template=block_template, is_combined=True)
    combined_blocks = CombinedBlock.objects.filter(
        block_template=block_template)

    context = {
        'block_template': block_template,
        'description_fields': description_fields,
        'fields': fields,
        'combined_blocks': combined_blocks
    }
    return render(request, 'dashboard/questionnaire/combine/q_combined.html', context)

def delete_combined_block_view(request,quest_id, combined_block_id):
    block_template = get_object_or_404(BlockTemplate, id=quest_id)
    combined_block = get_object_or_404(CombinedBlock, id=combined_block_id)
    description_field = combined_block.description_field
    fields = combined_block.fields.all().filter(block_template=block_template, is_combined=True)

    if fields or description_field:
        fields.update(is_combined=False)
        description_field.is_combined = False
        description_field.save()
    
    combined_block.delete()

    messages.success(request, 'Комбінація полів видалена успішно!')

    return redirect('questionnaire_detail', id=block_template.id)


def preview_questionnaire_view(request, id):
    block_template = get_object_or_404(BlockTemplate, id=id)
    fields = Field.objects.filter(block_template=block_template)
    description_fields = DescriptionField.objects.filter(
        block_template=block_template)
    combined_blocks = CombinedBlock.objects.filter(
        block_template=block_template).prefetch_related('fields')

    context = {
        'block_template': block_template,
        'fields': fields,
        'description_fields': description_fields,
        'combined_blocks': combined_blocks,
    }

    return render(request, 'dashboard/questionnaire/preview_questionnaire.html', context)


def questionnaire_result_view(request, id):
    block_template = get_object_or_404(BlockTemplate, id=id)
    fields = Field.objects.filter(block_template=block_template)
    description_fields = DescriptionField.objects.filter(
        block_template=block_template)
    combined_blocks = CombinedBlock.objects.filter(
        block_template=block_template).prefetch_related('fields')
    
    messages.success(request, 'Збережено успішно!!')
    
    current_site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    pre_url = f'{protocol}://{current_site.domain}'

    context = {
        'block_template': block_template,
        'fields': fields,
        'description_fields': description_fields,
        'combined_blocks': combined_blocks,
        'pre_url': pre_url,
    }

    return render(request, 'dashboard/questionnaire/questionare_view.html', context)

def questionnaire_user_result_view(request, uuid):
    block_template = get_object_or_404(BlockTemplate, uuid=uuid)
    fields = Field.objects.filter(block_template=block_template)
    description_fields = DescriptionField.objects.filter(
        block_template=block_template)
    combined_blocks = CombinedBlock.objects.filter(
        block_template=block_template).prefetch_related('fields')
    
    if not block_template.language:
        return redirect('choose_language_questionare', block_template.id)
    

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

        return render(request, 'survey/thanks.html')

    context = {
        'block_template': block_template,
        'fields': fields,
        'description_fields': description_fields,
        'combined_blocks': combined_blocks,
    }

    return render(request, 'survey/user_view.html', context)



def share_questionare_view(request, block_id):
    block_template = get_object_or_404(BlockTemplate, id=block_id)
    current_site = get_current_site(request)
    protocol = 'https' if request.is_secure() else 'http'
    pre_url = f'{protocol}://{current_site.domain}'

    context = {
        'block_template': block_template,
        'pre_url': pre_url,
    }
    return render(request, 'dashboard/questionnaire/share.html', context)