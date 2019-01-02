# Vamos a extender el formulario para incluir el email obligatorio al registrarse 
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserCreationFormWithEmail(UserCreationForm):

    email = forms.EmailField(required = True, help_text = "Requerido, 254 caracteres como máximo y debe ser válido")
    # Redefinimos la clase Meta
    class Meta: 
        model = User
        fields = ['username', 'email','password1','password2']

    # Se añade una validación para evitar que 2 usuarios tengan el mismo email
    def clean_email(self):
        # Recuperamos el email escrito por pantalla
        email = self.cleaned_data.get("email")
        # Filtramos en la BD si algún usuario tiene este email
        if User.objects.filter(email = email).exists():
            # Lanzamos un error si existe
            raise forms.ValidationError("El email ya esta registrado, pruebe con otra dirección de correo electrónico")
        # si no existe , devuelve el email
        return email 

#Clase para el formulario del perfil 
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'link']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
            'bio': forms.Textarea(attrs={'class':'form-control mt-3', 'rows':3, 'placeholder':'Biografía'}),
            'link': forms.URLInput(attrs={'class':'form-control mt-3', 'placeholder':'Enlace'}),
        }

# Clase para editar el email
class EmailForm(forms.ModelForm):
    email = forms.EmailField(required = True, help_text = "Requerido, 254 caracteres como máximo y debe ser válido")
    class Meta: 
        model = User
        fields = ['email']

    # Validación para ver si el email se ha modificado 
    def clean_email(self):
        email = self.cleaned_data.get("email")
        # change data es una lista que contiene lo q se ha modificado
        if 'email' in self.changed_data:
              if User.objects.filter(email = email).exists():
            # Lanzamos un error si existe
                raise forms.ValidationError("El email ya esta registrado, pruebe con otra dirección de correo electrónico")
        # si no existe , devuelve el email
        return email 