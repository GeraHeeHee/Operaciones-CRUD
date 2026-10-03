from django import forms

from .models import Curso


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ["codigo", "nombre", "creditos"]
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Código"}),
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre"}),
            "creditos": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 20}),
        }
