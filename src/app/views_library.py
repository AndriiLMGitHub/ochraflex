from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import LibraryTemplate, DescriptionField, Field, CombinedBlock, BlockTemplate
from django.db.models import Count, Q
from .utils import parse_json_field
import json



def library_view(request):
    library_fields_without_fields = LibraryTemplate.objects.filter(
        field__isnull=True,
        description_field__isnull=True,
        combined_block__isnull=True,
    )
    library_fields = LibraryTemplate.objects.annotate(
        num_fields=Count('field')).filter(num_fields__gt=0).prefetch_related('field')
    library_descriptions = LibraryTemplate.objects.filter(
        field__isnull=True,
        combined_block__isnull=True,
        description_field__isnull=False
        )
    library_blocks = LibraryTemplate.objects.annotate(
        num_fields=Count('combined_block')).filter(num_fields__gt=0).prefetch_related('combined_block__fields')
    
    if library_fields_without_fields:
        library_fields_without_fields.delete()


    context = {
        'library_fields': library_fields,
        'library_descriptions': library_descriptions,
        'library_blocks': library_blocks,
        'library_fields_all': library_fields_without_fields,
    }

    return render(request, 'dashboard/library/library.html', context)


def fetch_library_templates_view(request, id):
    block_template = get_object_or_404(BlockTemplate,id=id)
    library_templates = LibraryTemplate.objects.filter(
        Q(field__isnull=False) | 
        Q(description_field__isnull=False) | 
        Q(combined_block__isnull=False)
    )
    context = {
            'block_template': block_template,
            'library_templates': library_templates,  # Отримуємо всі шаблони бібліотеки, які відносяться до поточного блоку
    }

    return render(request, 'dashboard/library/all_library_templates.html', context)


def add_library_template_to_block_view(request, block_id, template_id):
    """Додає шаблон бібліотеки у блок"""
    
    block = get_object_or_404(BlockTemplate, id=block_id)
    template = get_object_or_404(LibraryTemplate, id=template_id)

    block.library_templates.add(template)  # Додаємо шаблон у блок
    messages.success(request, f'Шаблон "{template.name}" успішно додано до блоку "{block.name}"!')

    return redirect('questionnaire_detail', id=block.id)  # Редірект на деталі блоку

def remove_library_template_from_block_view(request, template_id):
    """Видаляє шаблон бібліотеки з блоку"""
    template = get_object_or_404(LibraryTemplate, id=template_id)
    block = BlockTemplate.objects.filter(library_templates=template).first() # Отримуємо блок, у якому знаходиться шаблон
    block.library_templates.remove(template)  # Видаляємо шаблон з блоку
    
    messages.success(request, f'Шаблон "{template.name}" успішно видалено з блоку "{block.name}"!')

    return redirect('questionnaire_detail', id=block.id)  # Редірект на деталі блоку


def library_create_block_view(request):
    """Створює шаблон у бібліотеці шаблонів"""
    if request.method == 'POST':
        name = request.POST.get('name')
        library_template=LibraryTemplate.objects.create(
            name=name,
            # user=request.user # to current user
        )
        library_template.save()
        messages.success(request, 'Шаблон успішно створено! Виберіть тип шаблону!')

        return redirect('choose_template_type', library_template.id)  # Перенаправлення на створення шаблонів

    context = {
    }

    return render(request, 'dashboard/library/create_templates/create_library_template.html', context)

# --- Start -> Create views templates ---

def create_field_to_template_view(request, id):
    library_template=get_object_or_404(LibraryTemplate, id=id)
    field = library_template.field

    context = {
        'library_template': library_template,
        'field': field 
    }

    return render(request, 'dashboard/library/create_templates/create_fields_template.html', context)

def create_description_field_template_view(request, id):
    library_template=get_object_or_404(LibraryTemplate, id=id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if library_template.combined_block is not None:
            if library_template.combined_block.description_field is not None:
                library_template.combined_block.description_field.title = title
                library_template.combined_block.description_field.description = description
                library_template.combined_block.description_field.save()
                library_template.combined_block.save()
                library_template.save()

                messages.success(request, 'Опис успішно змінено!')

                return redirect('create_combined_block_template', library_template.id)  # Перенаправлення на створення шаблонів
            
            elif library_template.combined_block.description_field is None:
                library_template.combined_block.description_field = DescriptionField.objects.create(
                    title=title,
                    description=description,
                )
                library_template.combined_block.description_field.save()
                library_template.combined_block.save()
                library_template.save()
                
                messages.success(request, 'Опис успішно додано!')
                return redirect('create_combined_block_template', library_template.id)  # Перенаправлення на створення шаблонів
            
        else:
            if library_template.description_field is None:
                library_template.description_field = DescriptionField.objects.create(
                    title=title,
                    description=description,
                )
                library_template.description_field.save()
                library_template.save()

                messages.success(request, 'Опис успішно додано!')

                return redirect('create_field_to_template', library_template.id)  # Перенаправлення на створення шаблонів
            else:
                library_template.description_field.title = title
                library_template.description_field.description = description
                library_template.description_field.save()

                messages.success(request, 'Опис успішно змінено!')
                return redirect('create_field_to_template', library_template.id)  # Перенаправлення на створення шаблонів


    context = {
        'library_template': library_template,
    }

    return render(request, 'dashboard/library/create_templates/create_description_field_template.html', context)
    
def update_description_field_template_view(request, id):
    library_template=get_object_or_404(LibraryTemplate, id=id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if library_template.combined_block:
            library_template.combined_block.description_field.title = title
            library_template.combined_block.description_field.description = description
            library_template.combined_block.description_field.save()
            messages.success(request, 'Опис успішно змінено!')
            return redirect('create_combined_block_template', library_template.id)  # Перенаправлення на створення шаблонів
        else:
            library_template.description_field.title = title
            library_template.description_field.description = description
            library_template.description_field.save()
            messages.success(request, 'Опис успішно змінено!')
            return redirect('create_field_to_template', library_template.id)  # Перенаправлення на створення шаблонів

    context = {
        'library_template': library_template,
    }
    return render(request, 'dashboard/library/create_templates/update_description_field_template.html', context)


def allow_duplicate_library_template_view(request, id):
    library_template=get_object_or_404(LibraryTemplate, id=id)

    if request.method == 'POST':
        library_template.allow_duplicate = not library_template.allow_duplicate
        library_template.save()
        messages.success(request, 'Дублікати дозволені успішно змінено!')

        return redirect('create_field_to_template', library_template.id)  # Перенаправлення на створення шаблонів

    context = {
        'library_template': library_template,
    }

    return render(request, 'dashboard/library/create_templates/allow_duplicate_template.html', context)


def create_combined_block_template_view(request, id):
    """Створює загальний блок з полями"""
    library_template = get_object_or_404(LibraryTemplate, id=id)

    if library_template.combined_block is None:
        library_template.combined_block=CombinedBlock.objects.create(
            allow_dublicate=False,
            # user=request.user
        )
        library_template.save()
    context = {
        'library_template': library_template,
    }

    return render(request, 'dashboard/library/create_templates/create_cm_fields_template.html', context)



# --- End -> Create views templates ---

# --- Start -> Delete views templates ---

def delete_field_from_library_template_view(request, library_id, field_id):
    """Видаляє поля з шаблону"""
    library_template = get_object_or_404(LibraryTemplate, id=library_id)
    field = get_object_or_404(Field, id=field_id)

    if library_template.combined_block:
        library_template.combined_block.fields.remove(field)
        library_template.combined_block.save()
        messages.success(request, f'Поле {field.name} успішно видалено з загального блоку!')
        return redirect('create_combined_block_template', library_template.id)
    else:
        library_template.field.delete()
        library_template.field=None
        library_template.save()
        messages.success(request, f'Поле успішно видалено з загального блоку!')
        return redirect('create_field_to_template', library_template.id)  # Перенаправлення на список шаблонів

def detete_description_field_from_library_view(request, library_id):
    """Видаляє опис з шаблону"""
    library_template = get_object_or_404(LibraryTemplate, id=library_id)
    if library_template.combined_block:
        library_template.combined_block.description_field.delete()
        library_template.combined_block.description_field = None
        library_template.combined_block.save()
        messages.success(request, 'Опис успішно видалено з шаблону!')
    else:
        library_template.description_field.delete()
        library_template.description_field = None
        library_template.save()
        messages.success(request, 'Опис успішно видалено з шаблону!')

    return redirect('create_field_to_template', library_template.id)  # Перенаправлення на список шаблонів


def delete_field_from_db_view(request, field_id, library_template_id):
    """Видаляє поле з бази даних"""
    library_template = get_object_or_404(LibraryTemplate, id=library_template_id)
    field = get_object_or_404(Field, id=field_id)
    field.delete()
    messages.success(request, f'Поле "{field.name}" успішно видалено з бази даних!')
    return redirect('create_combined_block_template', library_template.id)  # Перенаправлення на список шаблонів

def delete_description_field_from_db_view(request, library_template_id):
    """Видаляє опис з бази даних"""
    library_template = get_object_or_404(LibraryTemplate, id=library_template_id)
    library_template.combined_block.description_field.delete()
    library_template.combined_block.description_field = None
    library_template.combined_block.save()
    library_template.save()

    messages.success(request, 'Опис успішно видалено з бази даних!')
    return redirect('create_combined_block_template', library_template.id)  # Перенаправлення на список шаблонів

# --- End -> Delete views templates ---


def add_field_to_template_view(request, field_id):
    """Додає окреме поле у бібліотеку шаблонів"""
    field = get_object_or_404(Field, id=field_id)

    template, created = LibraryTemplate.objects.get_or_create(
        name=f'Шаблон поля: {field.name}',
        defaults={
            'description': f'Поле {field.name} з типом {field.field_type}',
            'field': field,
        }
    )
    if created:
        template.save()
        messages.success(request, f'Поле "{field.name}" додано у шаблон!')
    elif not created:
        messages.success(request, f'Поле "{field.name}" оновлено успішно!.')

    return redirect('library')  # Перенаправлення на список шаблонів


def add_description_to_template_view(request, description_id):
    """Додає окремий опис у бібліотеку шаблонів"""
    description_field = get_object_or_404(DescriptionField, id=description_id)

    template, created = LibraryTemplate.objects.get_or_create(
        name=f'Шаблон опису: {description_field.title}',
        defaults={
            'description': f'Опис: {description_field.description}',
            'description_field': description_field,
        }
    )
    if not created:
        template.description_field = description_field
        template.save()

    messages.success(
        request,
        f'Опис "{description_field.title}" додано у шаблон!'
    )
    return redirect('library')  # Перенаправлення на список шаблонів


def add_combined_block_to_template_view(request, combined_block_id):
    """Додає комбінований блок у бібліотеку шаблонів"""
    combined_block = get_object_or_404(CombinedBlock, id=combined_block_id)

    template = LibraryTemplate.objects.create(
        #user=request.user,
        name=f'Шаблон для {combined_block.block_template.name}',
        description=f'Шаблон для {combined_block.block_template.name}',
        combined_block=combined_block,  # Використовуємо ForeignKey
    )

    # Додаємо опис, якщо є
    if combined_block.description_field:
        template.description_field = combined_block.description_field

    template.save()

    messages.success(request,f'Новий шаблон для {combined_block.block_template.name} створено успішно!')
    return redirect('library')

def delete_combined_block_from_template_library_view(request, id):
    """Видаляє комбінований блок з шаблону"""
    template = get_object_or_404(LibraryTemplate, id=id)

    # Видаляємо поле з комбінованого блоку, якщо ��
    if template.combined_block and (template.description_field or template.combined_block.field):
        template.combined_block = None
        template.description_field = None
        template.field = None
        # Видаляємо комбінований блок з шаблону
        template.delete()
        messages.success(request, f'Комбінований блок з шаблону успішно видалено!')
        return redirect('library')
    else:
        messages.error(request, '��аблон не має комбінованого блоку або поля!')
        return redirect('library')


def edit_template_library_view(request, id):
    """Редагує шаблон в бібліотеці шаблонів"""
    template = get_object_or_404(LibraryTemplate, id=id)
    description_field = template.description_field
    field = template.field

    if request.method == 'POST':
        if description_field:
            template.description_field.title = request.POST.get('title')
            template.description_field.description = request.POST.get('description')
            template.description_field.save()
        elif field:
            template.field = field
        
        template.save()

        messages.success(request, 'Шаблон оновлено успішно!')
        return redirect('library')

    context = {
        'template': template,
    }

    return render(request, 'dashboard/library/edit_library_template.html', context)


def delete_template_view(request, template_id):
    """Видаляє шаблон"""
    template = get_object_or_404(LibraryTemplate, id=template_id)

    template.delete()

    messages.success(request, 'Шаблон видалено успішно!')
    return redirect('library')  # Перенаправлення на список шаблонів


def choose_template_type_view(request, library_id):
    """Вибір типу шаблону для створення"""
    library_template = get_object_or_404(LibraryTemplate, id=library_id)

    context = {
        'library_template': library_template,
    }

    return render(request, 'dashboard/library/create_templates/choose_type_template.html', context)



# Template view "Creating fields"

def create_textfield_template_view(request, id):
    library_template=get_object_or_404(LibraryTemplate, id=id)

    context = {
        'library_template': library_template,
    }

    return render(request, 'dashboard/library/create_templates/create_text_field.html', context)

def create_textarea_field_template_view(request, id):
    library_template=get_object_or_404(LibraryTemplate, id=id)

    context = {
        'library_template': library_template,
    }

    return render(request, 'dashboard/library/create_templates/create_textarea_field.html', context)

def create_select_field_template_view(request, id):
    library_template=get_object_or_404(LibraryTemplate, id=id)

    context = {
        'library_template': library_template,
    }

    return render(request, 'dashboard/library/create_templates/create_select_field.html', context)

def create_one_value_field_template_view(request, id):
    library_template=get_object_or_404(LibraryTemplate, id=id)

    context = {
        'library_template': library_template,
    }

    return render(request, 'dashboard/library/create_templates/create_one_value_template.html', context)

def create_multiple_values_field_template_view(request, id):
    library_template=get_object_or_404(LibraryTemplate, id=id)

    context = {
        'library_template': library_template,
    }

    return render(request, 'dashboard/library/create_templates/create_multiple_values_template.html', context)

def create_yes_or_no_field_template_view(request, id):
    library_template=get_object_or_404(LibraryTemplate, id=id)

    context = {
        'library_template': library_template,
    }

    return render(request, 'dashboard/library/create_templates/create_yes_or_no_template.html', context)

def create_phone_field_template_view(request, id):
    library_template=get_object_or_404(LibraryTemplate, id=id)

    context = {
        'library_template': library_template,
    }

    return render(request, 'dashboard/library/create_templates/create_phone_field.html', context)

def create_date_field_template_view(request, id):
    library_template=get_object_or_404(LibraryTemplate, id=id)

    context = {
        'library_template': library_template,
    }

    return render(request, 'dashboard/library/create_templates/create_date_field.html', context)