from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import LibraryTemplate, DescriptionField, Field, CombinedBlock, BlockTemplate
from .utils import parse_json


def create_combined_block_view(request, id):
    block_template = get_object_or_404(BlockTemplate, id=id)
    library_templates = block_template.library_templates.all()

    """Створює блок на основі вибраних чекбоксів полів (combined) та описового блоку (ds-combined)"""
    if request.method == "POST":
        field_ids = request.POST.getlist('combined')  # Отримуємо вибрані чекбокси полів
        description_field_id = request.POST.get('ds-combined')  # Отримуємо вибраний description_field

        selected_fields = Field.objects.filter(id__in=field_ids)  # Отримуємо об'єкти Field
        description_field = DescriptionField.objects.filter(id=description_field_id).first()  # Отримуємо DescriptionField

        if not selected_fields:
            messages.error(request, "Ви не вибрали жодного поля!")
            return redirect('create_combined_block', id=block_template.id)

        if not description_field:
            messages.error(request, "Ви не вибрали описовий блок!")
            return redirect('create_combined_block', id=block_template.id)
        
        selected_fields.update(is_combined=True)
        description_field.is_combined = True
        description_field.save()

        # Створюємо CombinedBlock
        combined_block = CombinedBlock.objects.create(
            block_template=block_template,
            description_field=description_field
        )

        # Додаємо вибрані поля в CombinedBlock
        combined_block.fields.set(selected_fields)

        messages.success(request, "Новий комбінований блок успішно створено!")

        return redirect('get_combined_block', quest_id=block_template.id, combined_block_id=combined_block.id)

    # Отримуємо всі доступні поля та описові блоки для форми
    fields = Field.objects.filter(block_template=block_template)
    description_fields = DescriptionField.objects.filter(block_template=block_template)

    em1 = len(fields.filter(is_combined=True)) == len(fields)
    em2 = len(description_fields.filter(is_combined=True)) == len(description_fields)
    empty = em1==True and em2==True

    context = {
        'block_template': block_template,
        'fields': parse_json(fields),
        'description_fields': description_fields,
        'library_templates': library_templates,
        'empty': empty,
    }

    return render(request, 'dashboard/questionnaire/combine/q_detail_combine.html', context)


def get_combined_block_view(request, quest_id, combined_block_id):
    block_template = get_object_or_404(BlockTemplate, id=quest_id)
    combined_block = get_object_or_404(CombinedBlock, id=combined_block_id)

    context = {
        'block_template': block_template,
        'combined_block': combined_block,
    }

    return render(request, 'dashboard/questionnaire/combine/q_combined.html', context)

def edit_combined_block_view(request, quest_id, combined_block_id):
    block_template = get_object_or_404(BlockTemplate, id=quest_id)
    fields = Field.objects.filter(block_template=block_template)
    description_fields = DescriptionField.objects.filter(block_template=block_template)
    combined_block = get_object_or_404(CombinedBlock, id=combined_block_id)
    description_field = combined_block.description_field
    combined_block_fields = combined_block.fields.all()
    
    block_template = combined_block.block_template  # Отримуємо шаблон блоку

    if request.method == "POST":
        field_ids = request.POST.getlist('combined')  # Отримуємо вибрані чекбокси (нові поля)
        description_field_id = request.POST.get('ds-combined')  # Отримуємо новий description_field

        # Отримуємо нові вибрані поля
        new_selected_fields = Field.objects.filter(id__in=field_ids)

        # Отримуємо старі поля (які були вибрані раніше)
        old_selected_fields = combined_block.fields.all()

        # Визначаємо, які поля потрібно **видалити** (були вибрані, але користувач зняв чекбокс)
        fields_to_remove = old_selected_fields.exclude(id__in=field_ids)

        # Визначаємо, які поля потрібно **додати** (нові, яких не було в старих)
        fields_to_add = new_selected_fields.exclude(id__in=old_selected_fields.values_list('id', flat=True))

        # Видаляємо старі поля (якщо користувач зняв чекбокс)
        for field in fields_to_remove:
            field.is_combined = False
            field.save()
            combined_block.fields.remove(field)

        # Додаємо нові поля
        for field in fields_to_add:
            field.is_combined = True
            field.save()
            combined_block.fields.add(field)

        # Оновлення description_field
        if description_field_id:
            new_description_field = get_object_or_404(DescriptionField, id=description_field_id)

            # Якщо description_field змінився, оновлюємо попередній
            if combined_block.description_field and combined_block.description_field != new_description_field:
                combined_block.description_field.is_combined = False
                combined_block.description_field.save()

            # Оновлюємо або встановлюємо новий description_field
            new_description_field.is_combined = True
            new_description_field.save()
            combined_block.description_field = new_description_field

        # Якщо користувач повністю прибрав description_field
        elif combined_block.description_field:
            combined_block.description_field.is_combined = False
            combined_block.description_field.save()
            combined_block.description_field = None

        combined_block.save()

        messages.success(request, "Комбінований блок успішно оновлено!")
        return redirect('get_combined_block', quest_id=quest_id, combined_block_id=combined_block.id)
    

    context = {
        'block_template': block_template,
        'combined_block': combined_block,
        'description_field': description_field,
        'combined_block_fields': combined_block_fields,
        'fields': fields,
        'description_fields': description_fields,
    }

    return render(request, 'dashboard/questionnaire/combine/q_edit_combine.html', context)