from django import forms

from uploads.core.models import Document


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )

class ContactForm(forms.Form):
    mrz_type = forms.CharField(required=True)
    valid_score = forms.CharField(required=True)
    date_of_birth = forms.CharField(required=True)
    type = forms.CharField(required=True)
    number = forms.CharField(required=True)
    date_of_birth = forms.CharField(required=True)
    expiration_date = forms.CharField(required=True)
    nationality = forms.CharField(required=True)
    sex = forms.CharField(required=True)
    names = forms.CharField(required=True)
    surname = forms.CharField(required=True)
    personal_number = forms.CharField(required=True)
    check_number = forms.CharField(required=True)
    check_date_of_birth = forms.CharField(required=True)
    check_expiration_date = forms.CharField(required=True)
    check_composite = forms.CharField(required=True)
    check_personal_number = forms.CharField(required=True)
    valid_number = forms.BooleanField(required=True)
    valid_date_of_birth = forms.BooleanField(required=True)
    valid_expiration_date = forms.BooleanField(required=True)
    valid_composite = forms.BooleanField(required=True)
    valid_personal_number = forms.BooleanField(required=True)
    method = forms.CharField(required=True)
    walltime = forms.CharField(required=True)
    filename = forms.CharField(required=True)





"""
{
  "mrz_type": "TD3", 
  "valid_score": 100, 
  "type": "P<", 
  "country": "UTO", 
  "number": "L898902C3", 
  "date_of_birth": "740812", 
  "expiration_date": "120415", 
  "nationality": "UTO", 
  "sex": "F", 
  "names": "ANNA MARIA", 
  "surname": "ERIKSSON", 
  "personal_number": "ZE184226B<<<<<", 
  "check_number": "6", 
  "check_date_of_birth": "2", 
  "check_expiration_date": "9", 
  "check_composite": "0", 
  "check_personal_number": "1", 
  "valid_number": true, 
  "valid_date_of_birth": true, 
  "valid_expiration_date": true, 
  "valid_composite": true, 
  "valid_personal_number": true, 
  "method": "rescaled(3)", 
  "walltime": 2.0293290615081787, 
  "filename": "100_pass-uto.jpg"
}
"""