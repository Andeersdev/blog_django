from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['full_names', 'email', 'password', 'image']
        widgets = {
            'password': forms.PasswordInput(),
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # commit=True es para indicar si los datos del form se deben alamcenar en la base de datos
    def save(self, commit=True):
        # Heredando save de forms.ModelForm, aqui el commit es False debido a que solo queremos hacer una instancia
        user = super().save(commit=False)
        # Usa set_password para hashear la contraseña, esto se puede ya que instanciamos con el commit en False
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
