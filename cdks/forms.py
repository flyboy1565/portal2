from django.forms import ModelForm

from .models import Kit, Shipping


class NewKit(ModelForm):
    
    class Meta:
        model = Kit
        exclude = ('status', 'online',)
        
        
class ShipKit(ModelForm):
    
    class Meta:
        model = Shipping
        fields = ('at_store', 'ticket_number', 
                  'tracking_number_to_store', 
                  'tracking_number_to_help_support'
                )