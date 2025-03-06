from django.contrib import admin
from .models import Field, BlockTemplate, DescriptionField, CombinedBlock, LibraryTemplate

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'field_type', 'is_combined','is_required', 'id')
    list_filter = ('field_type', 'is_required',)
    filter_fields = ('block_template',)


@admin.register(BlockTemplate)
class BlockTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'uuid')
    filter_horizontal = (
        'library_templates',
    )


@admin.register(DescriptionField)
class DescriptionFieldAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_combined')


@admin.register(CombinedBlock)
class CombinedBlockAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'fields',
    )


@admin.register(LibraryTemplate)
class LibraryTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at','id')
    list_filter = ('created_at',)
    filter_fields = ('block_template',)
