from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import BlockTemplate, DescriptionField, Field


class CustomPasswordChangeForm(PasswordChangeForm):
    first_name = forms.CharField(
        max_length=30, required=False, label="First Name")
    last_name = forms.CharField(
        max_length=30, required=False, label="Last Name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class BlockTemplateForm(forms.ModelForm):
    class Meta:
        model = BlockTemplate
        fields = (
            'name', 'description',
        )


class DescriptionFieldForm(forms.ModelForm):
    class Meta:
        model = DescriptionField
        fields = (
            'title', 'description',
        )
