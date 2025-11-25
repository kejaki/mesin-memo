from django import forms
from django.forms import inlineformset_factory
from .models import ContentItem, ContentComment, JobRole

class ContentItemForm(forms.ModelForm):
    class Meta:
        model = ContentItem
        fields = ['title', 'content_type', 'platform', 'target_date', 'description', 'draft_link', 'is_claimable']
        widgets = {
            'target_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ContentCommentForm(forms.ModelForm):
    class Meta:
        model = ContentComment
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tulis komentar...'}),
        }

class JobRoleForm(forms.ModelForm):
    class Meta:
        model = JobRole
        fields = ['role_type', 'slots_needed', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Opsional: Jelaskan detail role ini'}),
        }

# Formset for inline job roles
JobRoleFormSet = inlineformset_factory(
    ContentItem,
    JobRole,
    form=JobRoleForm,
    extra=3,  # Show 3 empty forms by default
    can_delete=True,
    min_num=0,
    validate_min=False
)
