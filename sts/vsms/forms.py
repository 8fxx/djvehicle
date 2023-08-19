from django import forms
from vsms.models import vehicle, status

class NewVehicleForm(forms.ModelForm):
    dateofimport = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    servicedate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = vehicle
        fields = ('__all__')
        exclude = ['createdby','photo','laststatus','issuedtounit','lastlocation']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['name'].widget.attrs.update({'class':'form-control'})
        self.fields['brand'].widget.attrs.update({'class':'form-select'})
        self.fields['type'].widget.attrs.update({'class':'form-select'})
        self.fields['transmission'].widget.attrs.update({'class':'form-select'})
        self.fields['inventorynumber'].widget.attrs.update({'class':'form-control'})
        self.fields['model'].widget.attrs.update({'class':'form-control'})
        self.fields['enginetype'].widget.attrs.update({'class':'form-control'})
        self.fields['enginenumber'].widget.attrs.update({'class':'form-control'})
        self.fields['enginecc'].widget.attrs.update({'class':'form-control'})  
        self.fields['capacity'].widget.attrs.update({'class':'form-control'})
        
        self.fields['dateofimport'].label = "Date of Import"
        
        
        self.fields['dateofimport'].widget.attrs.update({'class':'form-control'})
        self.fields['fuelcapacity'].label = "Fuel Capacity in Liters"
        self.fields['fuelcapacity'].widget.attrs.update({'class':'form-control'})
        self.fields['price'].widget.attrs.update({'class':'form-control'})
        self.fields['tonage'].widget.attrs.update({'class':'form-control'})
        self.fields['servicedate'].label = "Service Date"
        self.fields['servicedate'].widget.attrs.update({'class':'form-control'})


class NewStatusForm(forms.ModelForm):
    class Meta:
        model = status
        fields = ('update','type','remarks','allotmentunit','allotmentlocation')
        exclude = ('statusapproved','createdby')

    def __init__(self, *args, **kwargs):
            super().__init__(*args,**kwargs)
            self.fields['update'].widget.attrs.update({'class':'form-select'})
            self.fields['type'].widget.attrs.update({'class':'form-select'})
            self.fields['remarks'].widget.attrs.update({'class':'form-control'})
            self.fields['allotmentunit'].widget.attrs.update({'class':'form-select'})
            self.fields['allotmentlocation'].widget.attrs.update({'class':'form-select'})

class filterform(forms.Form):
    name = forms.CharField()