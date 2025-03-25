from django.urls import path
from . import views, views_json, views_library, views_combined

urlpatterns = [
     # Dashboard routes
     path('settings/', views.dashboard_view, name='dashboard'),
     path('resumes/', views.list_resumes_view, name='list_resumes'),
     path('questionnaires/', views.questionnaires_view, name='questionnaires'),
     path('questionnaires/add/', views.add_questionnaire, name='add_questionnaire'),
     path(
          'questionnaires/<str:id>/',
          views.questionnaire_detail,
          name='questionnaire_detail'
     ),
     path(
          'questionnaires/<str:id>/edit/',
          views.questionnaire_edit,
          name='questionnaire_edit'
     ),
     path(
          'questionnaires/<str:id>/delete/',
          views.delete_questionnaire,
          name='delete_questionnaire'
     ),

     # Add more routes as needed for the dashboard app
     path(
          'questionnaires/<str:id>/add/new/header/block/',
          views.add_new_header_block_view,
          name='add_new_header_block'
     ),
     path('questionnaires/update/header/block/<str:id>/',
          views.update_header_block_view, name='update_header_block'),
     path('questionnaires/delete/header/block/<str:id>/',
          views.delete_header_block_view, name="delete_header_block"),


     path(
          'questionnaires/<str:id>/add/new/field/',
          views.add_new_field_view,
          name='add_new_field'
     ),
     path(
          'questionnaires/<str:id>/add/new/textarea/field/',
          views.add_new_textarea_field_view,
          name='add_new_textarea_field'
     ),

     path(
          'questionnaires/update/field/<str:id>/',
          views.update_text_field_view,
          name='update_text_field'
     ),
     path(
          'questionnaires/update/textarea/field/<str:id>/',
          views.update_textarea_field_view,
          name='update_textarea_field'
     ),
     path(
          'questionnaires/update/select/field/<str:id>/',
          views.update_select_field_view,
          name='update_select_field'
     ),
     path(
          'questionnaires/update/one/value/<str:id>/',
          views.edit_one_value_view,
          name='edit_one_value'
     ),
     path(
          'questionnaires/update/multiple/values/<str:id>/',
          views.edit_multiple_values_view,
          name='edit_multiple_values'
     ),
     path(
          'questionnaires/update/boolean/field/<str:id>/',
          views.edit_yes_or_no_view,
          name='edit_yes_or_no'
     ),
     path(
          'questionnaires/update/phone/field/<str:id>/',
          views.edit_phone_field_view,
          name='edit_phone_field'
     ),
     path(
          'questionnaires/update/date/field/<str:id>/',
          views.edit_date_field_view,
          name='edit_date_field'
     ),
     path(
          'questionnaires/<str:id>/add/new/select/field/',
          views.add_new_select_field_view,
          name='add_new_select_field'
     ),
     path(
          'questionnaires/<str:id>/add/new/one/value/',
          views.add_new_one_value_view,
          name='add_new_one_value'
     ),
     path(
          'questionnaires/<str:id>/add/new/multiple/value/',
          views.add_new_multiple_value_view,
          name='add_new_multiple_value'
     ),
     path(
          'questionnaires/<str:id>/add/new/boolean/value/',
          views.add_new_boolean_field_view,
          name='add_new_boolean_field'
     ),
     path(
          'questionnaires/<str:id>/add/new/phone/value/',
          views.add_new_phone_field_view,
          name='add_new_phone_field'
     ),
     path(
          'questionnaires/<str:id>/add/new/date/value/',
          views.add_new_date_field_view,
          name='add_new_date_field'
     ),
     path(
          'questionnaires/<str:id>/delete/field/',
          views.delete_field_view,
          name='delete_field'
     ),
     path(
          'questionnaires/<str:id>/add/alt/language/date/field',
          views.de_language_date_field_view,
          name="de_language_date_field"
     ),
     path(
          'questionnaires/<str:id>/add/alt/language/phone/field',
          views.de_language_phone_field_view,
          name="de_language_phone_field"
     ),
     path(
          'questionnaires/<str:id>/add/alt/language/yes/or/no/field',
          views.de_language_yes_or_no_field_view,
          name="de_language_yes_or_no_field"
     ),
     path(
          'questionnaires/<str:id>/add/alt/language/multiple/field',
          views.de_language_multiple_values_view,
          name="de_language_multiple_values"
     ),
     path(
          'questionnaires/<str:id>/add/alt/language/one/field',
          views.de_language_one_value_view, name="de_language_one_value"
     ),
     path(
          'questionnaires/<str:id>/add/alt/language/select/field',
          views.de_language_select_field_view,
          name="de_language_select_field"
     ),
     path(
          'questionnaires/<str:id>/add/alt/language/textarea/field',
          views.de_language_textarea_field_view,
          name="de_language_textarea_field"
     ),
     path(
          'questionnaires/<str:id>/add/alt/language/text/field',
          views.de_language_text_field_view,
          name="de_language_text_field"
     ),


     # Combined URLS
     path(
          'questionnaires/<str:id>/preview/',
          views.preview_questionnaire_view,
          name="preview_questionnaire"
     ),
     path(
          'questionnaires/<str:id>/view/result/',
          views.questionnaire_result_view,
          name="questionnaire_result"
     ),
     path(
          'questionnaires/<str:uuid>/',
          views.questionnaire_user_result_view,
          name="questionnaire_user_result"
     ),
     path(
          'questionnaires/<str:id>/combine/',
          views.questionnaire_combine_view,
          name="questionnaire_combine"
     ),
     path(
          'questionnaires/<str:quest_id>/combine/duplicate/<str:combined_block_id>/',
          views_combined.get_combined_block_view,
          name="get_combined_block"
     ),
     path(
          'questionnaires/<str:quest_id>/combine/delete/<str:combined_block_id>/',
          views.delete_combined_block_view,
          name="delete_combined_block"
     ),
     path(
          'questionnaires/<str:id>/combine/create/block/',
          views_combined.create_combined_block_view,
          name="create_combined_block"
     ),
     path(
          'questionnaires/<str:quest_id>/combine/update/block/<str:combined_block_id>/',
          views_combined.edit_combined_block_view,
          name="edit_combined_block"
     ),
     path(
          'questionnaires/<str:id>/',
          views.questionnaire_combined_detail_view,
          name="questionnaire_combined_detail"
     ),


     # Library URLs
     path('library/', views_library.library_view, name='library'),
     path(
          'library/all/templates/<str:id>/',
          views_library.fetch_library_templates_view,
          name='fetch_library_templates'
     ),
     path(
          'library/create/block/',
          views_library.library_create_block_view,
          name='library_create_block'
     ),
     path(
          'library/choose/template/type/<str:library_id>/',
          views_library.choose_template_type_view,
          name='choose_template_type'
     ),
     path(
          'library/update/block/<int:id>/',
          views_library.edit_template_library_view,
          name='edit_template_library'
     ),
     path(
          'add/field/<int:field_id>/',
          views_library.add_field_to_template_view,
          name='add_field_to_template'
     ),
     path(
          'add/description/<int:description_id>/',
          views_library.add_description_to_template_view,
          name='add_description_to_template'
     ),
     path(
          'library/create/combined/block/template/<str:id>/',
          views_library.create_combined_block_template_view,
          name='create_combined_block_template'
     ),
     # Додавання комбінованого блоку у шаблон
     path(
          'add/combined/block/<int:combined_block_id>/',
          views_library.add_combined_block_to_template_view,
          name='add_combined_block_to_template'
     ),
     path('add/library/template/<int:block_id>/add-template/<int:template_id>/',
          views_library.add_library_template_to_block_view,
          name="add_library_template_to_block"
          ),
     path(
          'delete/template/<int:template_id>/',
          views_library.delete_template_view,
          name="delete_template"
     ),
     path(
          'detele/field/from/db/<str:library_template_id>/<str:field_id>/',
          views_library.delete_field_from_db_view,
          name="delete_field_from_db"
     ),
     path(
          'delete/description/field/from/db/<str:library_template_id>/',
          views_library.delete_description_field_from_db_view,
          name='delete_description_field_from_db'
     ),
     path(
          'delete/template/block/<str:id>/',
          views_library.delete_combined_block_from_template_library_view,
          name="delete_combined_block_from_template_library"
     ),
     #  Library URLs -> Library creation fields
     path(
          'create/template/field/<int:id>/',
          views_library.create_field_to_template_view,
          name="create_field_to_template"
     ),
     path(
          'update/template/descriptions/fields/<int:id>/',
          views_library.update_description_field_template_view,
          name="update_description_field_template"
     ),
     path(
          'create/template/fields/textfield/<int:id>/',
          views_library.create_textfield_template_view,
          name="create_textfield_template"
     ),
     path(
          'create/template/fields/textareafield/<int:id>/',
          views_library.create_textarea_field_template_view,
          name="create_textarea_field_template"
     ),
     path(
          'create/template/fields/selectfield/<int:id>/',
          views_library.create_select_field_template_view,
          name="create_select_field_template"
     ),
     path(
          'create/template/fields/one/field/<int:id>/',
          views_library.create_one_value_field_template_view,
          name="create_one_value_field_template"
     ),
     path(
          'create/template/fields/multiple/field/<int:id>/',
          views_library.create_multiple_values_field_template_view,
          name="create_multiple_values_field_template"
     ),
     path(
          'create/template/fields/yes/or/no/field/<int:id>/',
          views_library.create_yes_or_no_field_template_view,
          name="create_yes_or_no_field_template"
     ),
     path(
          'create/template/fields/phone/field/<int:id>/',
          views_library.create_phone_field_template_view,
          name="create_phone_field_template"
     ),
     path(
          'create/template/fields/date/field/<int:id>/',
          views_library.create_date_field_template_view,
          name="create_date_field_template"
     ),

     # Remove template from library
     path('remove/template/from/library/<str:template_id>/',
          views_library.remove_library_template_from_block_view,
          name="remove_library_template_from_block"
     ),
     # Create after delete description field
     path(
          'create/template/fields/description/field/<int:id>/',
          views_library.create_description_field_template_view,
          name="create_description_field_template"
     ),
     path(
          'delete/template/fields/field/<str:library_id>/<str:field_id>/',
          views_library.delete_field_from_library_template_view,
          name="delete_field_from_library_template"
     ),
     path(
          'delete/template/fields/description/field/<str:library_id>/',
          views_library.detete_description_field_from_library_view,
          name="detete_description_field_from_library"
     ),
     # Allow duplicate library template
     path('allow_duplicate/library/template/<int:id>/',
          views_library.allow_duplicate_library_template_view,
          name='allow_duplicate_library_template'
     ),

     # User View Routes
     path('user/questionare/create/answer/<str:uuid>/', views.questionnaire_user_result_view, name='questionnaire_user_result'),



     # JSON API routes for creating and updating fields
     path(
          'api/fields/create/<str:id>/',
          views_json.create_field,
          name='create_field'
     ),
     path(
          'api/fields/update/<str:id>/',
          views_json.update_field,
          name='update_field'
     ),
     path(
          'api/fields/create/duplicate/<str:combined_block_id>/',
          views_json.duplicate_block_view,
          name='duplicate_block'
     ),

     # Library routes for creating and updating
     path(
          'api/library/create/fields/<str:id>/',
          views_json.create_field_template,
          name='create_field_template'
     ),
     path(
          'api/library/allow/duplicate/<int:library_id>/',
          views_json.duplicate_library_template,
          name='duplicate_library_template'
     ),
]
