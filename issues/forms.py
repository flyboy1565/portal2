from django import forms


from .models import CommunicationsIssue
from .choices import issues_choices

class EditIssueForm(forms.Form):
    pk = forms.IntegerField(widget=forms.HiddenInput())
    issue = forms.ChoiceField(widget=forms.Select, choices=issues_choices())