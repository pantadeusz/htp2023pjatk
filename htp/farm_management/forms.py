from django import forms
from .models import Farm, FarmActivity


class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'location', 'total_area', 'compliance_status']


class FarmActivityForm(forms.ModelForm):
    class Meta:
        model = FarmActivity
        fields = ['farm', 'activity_type', 'date_time', 'area_covered', 'details']

    def __init__(self, *args, **kwargs):
        super(FarmActivityForm, self).__init__(*args, **kwargs)
        # Limit the available farms to choose from in the form
        self.fields['farm'].queryset = Farm.objects.all()


class FarmActivityAddForm(forms.ModelForm):
    class Meta:
        model = FarmActivity
        fields = ['activity_type', 'date_time', 'area_covered', 'details']

    farm = forms.ModelChoiceField(
        queryset=Farm.objects.all(),
        widget=forms.HiddenInput(),
    )

    def __init__(self, *args, **kwargs):
        super(FarmActivityAddForm, self).__init__(*args, **kwargs)
        self.fields['farm'].required = False  # Make the field not required

