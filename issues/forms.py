from django import forms


from .models import CommunicationsIssue, AdditionalIssue
from .choices import issues_choices

class EditIssueForm(forms.Form):
    pk = forms.IntegerField(widget=forms.HiddenInput())
    issue = forms.ChoiceField(widget=forms.Select, choices=issues_choices())
    
    
class AdditionalIssueForm(forms.ModelForm):
    
    class Meta:
        model = AdditionalIssue
        fields = ('description', 'expires_at', 'effected_systems', 'ticket_number')