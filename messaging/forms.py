from django import forms

from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            "recipient",
            "subject",
            "body",
        ]
        widgets = {
            "body": forms.Textarea(
                attrs={
                    "rows": 6,
                }
            ),
        }