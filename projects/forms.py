from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    """Form used to create and update projects."""

    class Meta:
        model = Project

        fields = (
            "title",
            "description",
            "start_date",
            "end_date",
            "stakeholders",
            "status",
        )

        widgets = {
            "start_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "end_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                }
            ),
            "stakeholders": forms.Textarea(
                attrs={
                    "rows": 3,
                }
            ),
        }