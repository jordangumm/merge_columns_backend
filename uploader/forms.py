from django import forms
from models import UploadFile


class UploadFileForm(forms.Form):
    file = UploadFile