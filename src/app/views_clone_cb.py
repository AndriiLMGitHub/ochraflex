from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import CombinedBlock, Field, DescriptionField, BlockTemplate, LibraryTemplate
from django.db import transaction

@require_POST
def clone_combined_block(request, block_id, block_template_id):
    original_block = get_object_or_404(CombinedBlock, id=block_id)
    block_template = get_object_or_404(BlockTemplate, id=block_template_id)

    with transaction.atomic():
        # Клонування description_field
        original_description = original_block.description_field
        cloned_description = None
        if original_description:
            cloned_description = DescriptionField.objects.create(
                block_template=original_description.block_template,
                title=original_description.title,
                description=original_description.description,
                is_combined=original_description.is_combined
            )

        
        # Створення нового CombinedBlock
        cloned_block = CombinedBlock.objects.create(
            block_template=block_template,
            description_field=cloned_description,
            allow_dublicate=original_block.allow_dublicate,
            is_cloned=True,
            is_from_library_template = True if original_block.library_templates.exists() else False,
            is_copy_from_original=True if not original_block.library_templates.exists() else False,
            original=original_block  # ← Зв'язок з оригіналом
        )

        # Клонування полів
        for field in original_block.fields.all():
            cloned_field = Field.objects.create(
                name=field.name,
                field_type=field.field_type,
                options=field.options,
                static_value=field.static_value,
                max_symbols=field.max_symbols,
                max_numbers=field.max_numbers,
                help_info=field.help_info,
                is_required=field.is_required,
                extra_tag=field.extra_tag,
                is_combined=field.is_combined,
                from_library=field.from_library,
                block_template=field.block_template
            )
            cloned_block.fields.add(cloned_field)

    return JsonResponse({"status": "success", "new_block_id": cloned_block.id})