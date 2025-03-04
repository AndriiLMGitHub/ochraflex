from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Field, BlockTemplate, DescriptionField, CombinedBlock, LibraryTemplate
from .utils import parse_json
import json


@csrf_exempt
def create_field(request, id):
    block_template = get_object_or_404(BlockTemplate, id=id)
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            field_type = request.POST.get('field_type')
            max_symbols = request.POST.get('max_symbols')
            extra_tag = request.POST.get('extra_tag', '').strip()
            static_value = request.POST.get('static_value', '').strip()
            help_info = request.POST.get('help_info', '')
            is_required = request.POST.get('is_required') == 'true'

            # Обробка опцій для типу "select"
            options = request.POST.getlist(
                'options')  # Очікується список опцій

            # Валідація для "Сталого значення"
            if max_symbols == 'static':
                if not static_value:
                    return JsonResponse({'status': 'error', 'message': 'Введіть значення для "Сталого значення".'})
                max_symbols = None  # "Стале значення" виключає ліміт символів
            else:
                static_value = None  # Очищаємо значення, якщо вибрано інший режим
                max_symbols = int(max_symbols) if max_symbols else None

            # Створення поля
            field = Field.objects.create(
                name=name,
                field_type=field_type,
                max_symbols=max_symbols,
                static_value=static_value,
                help_info=help_info,
                is_required=is_required,
                extra_tag=extra_tag,
                block_template=block_template,
            )

            # Додавання опцій, якщо поле типу "select"
            if (field_type == 'select' or field_type == 'radio' or field_type == 'checkbox') and options:
                if not isinstance(options, list):
                    return JsonResponse({'status': 'error', 'message': 'Опції повинні бути списком.'})
                # Зберігаємо опції у JSONField
                field.options = options
                field.save()

            return JsonResponse({'status': 'success', 'message': 'Поле успішно створено!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Метод не підтримується.'})


@csrf_exempt
def update_field(request, id):
    try:
        field = get_object_or_404(Field, id=id)  # Отримуємо існуюче поле
        if request.method == 'POST':
            # Отримання даних із запиту
            # Використовуємо поточне значення, якщо не передано нове
            name = request.POST.get('name', field.name)
            field_type = request.POST.get('field_type', field.field_type)
            max_symbols = request.POST.get('max_symbols', field.max_symbols)
            static_value = request.POST.get('static_value', field.static_value)
            help_info = request.POST.get('help_info', field.help_info)
            is_required = request.POST.get(
                'is_required', field.is_required) == 'true'

            # Обробка опцій для типу "select"
            options = request.POST.getlist(
                'options')  # Очікується список опцій

            # Валідація для "Сталого значення"
            if max_symbols == 'static':
                if not static_value:
                    return JsonResponse({'status': 'error', 'message': 'Введіть значення для "Сталого значення".'})
                max_symbols = None  # "Стале значення" виключає ліміт символів
            else:
                static_value = None  # Очищаємо значення, якщо вибрано інший режим
                max_symbols = int(max_symbols) if max_symbols else None

            # Оновлення даних поля
            field.name = name
            field.field_type = field_type
            field.max_symbols = max_symbols
            field.static_value = static_value
            field.help_info = help_info
            field.is_required = is_required

            # Оновлення опцій, якщо поле типу "select"
            if ((field_type == 'select' or field_type == 'radio' or field_type == 'checkbox') and options):
                if not isinstance(options, list):
                    return JsonResponse({'status': 'error', 'message': 'Опції повинні бути списком.'})
                # Зберігаємо опції у JSONField
                field.options = options

            field.save()

            return JsonResponse({'status': 'success', 'message': 'Поле успішно оновлено!'})

        return JsonResponse({'status': 'error', 'message': 'Метод не підтримується.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


def duplicate_block_view(request, combined_block_id):
    combined_block = get_object_or_404(CombinedBlock, id=combined_block_id)

    if request.method == 'POST':
        if combined_block.allow_dublicate == False:
            combined_block.allow_dublicate = True
            combined_block.save()
        else:
            combined_block.allow_dublicate = False
            combined_block.save()

        return JsonResponse({'success': True, 'message': 'Запитання дублювання успішно створено!'})
    else:
        return JsonResponse({'success': False, 'message': 'Запитання дублювання не створено.'})
    

def duplicate_library_template(request, library_id):
    library_template = get_object_or_404(LibraryTemplate, id=library_id)
    if request.method == 'POST':
        library_template.combined_block.allow_dublicate = not library_template.combined_block.allow_dublicate
        library_template.combined_block.save()
        return JsonResponse({'success': True, 'message': 'Запитання дублювання успішно створено!'})

    else:
        return JsonResponse({'success': False, 'message': 'Запитання дублювання не створено.'})


def create_field_template(request, id):
    library_template = get_object_or_404(LibraryTemplate, id=id)
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            field_type = request.POST.get('field_type')
            max_symbols = request.POST.get('max_symbols')
            extra_tag = request.POST.get('extra_tag', '').strip()
            static_value = request.POST.get('static_value', '').strip()
            help_info = request.POST.get('help_info', '')
            is_required = request.POST.get('is_required') == 'true'

            # Обробка опцій для типу "select"
            options = request.POST.getlist(
                'options')  # Очікується список опцій

            # Валідація для "Сталого значення"
            if max_symbols == 'static':
                if not static_value:
                    return JsonResponse({'status': 'error', 'message': 'Введіть значення для "Сталого значення".'})
                max_symbols = None  # "Стале значення" виключає ліміт символів
            else:
                static_value = None  # Очищаємо значення, якщо вибрано інший режим
                max_symbols = int(max_symbols) if max_symbols else None

            # Створення поля
            field=Field.objects.create(
                name=name,
                field_type=field_type,
                max_symbols=max_symbols,
                static_value=static_value,
                help_info=help_info,
                is_required=is_required,
                extra_tag=extra_tag,
            )

            if library_template.combined_block is not None:
                library_template.combined_block.fields.add(field)
                library_template.combined_block.save()
                library_template.save()
            else:
                library_template.field = field
                library_template.save()

            

            # Додавання опцій, якщо поле типу "select"
            if (field_type == 'select' or field_type == 'radio' or field_type == 'checkbox') and options:
                if not isinstance(options, list):
                    return JsonResponse({'status': 'error', 'message': 'Опції повинні бути списком.'})
                # Зберігаємо опції у JSONField
                field.options = options
                field.save()

            return JsonResponse({'status': 'success', 'message': 'Поле успішно створено!'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Метод не підтримується.'})