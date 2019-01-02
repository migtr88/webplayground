#from django.shortcuts import render
#from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreationFormWithEmail,ProfileForm,EmailForm
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django import forms 
from .models import Profile

# Create your views here.
 #Creamos CVB de registro 
class SignUpView(CreateView):
    form_class = UserCreationFormWithEmail
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    #Vamos a modificar el método get_succes_url para poder modificar en enlace en tiempo real de ejecución 
    # y así devolver un parámetro OK
    def get_success_url(self):
        return reverse_lazy('login')+ '?register'
    
    #Vamos a definir un método para recuperar los campos del formulario y modificar su aspecto en tiempo real de ejecución
    #de esta manera evitamos redefinirlos en el forms.py, si se redefinieran en el forms se sobreescribirían y 
    # se perderían las validaciones que incorporan
    def get_form(self, form_class = None):
        form = super(SignUpView,self).get_form()
        # Modificamos en tiempo real
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2','placeholder':'Nombre de usuario'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2','placeholder':'Email del usuario'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2','placeholder':'Introduzca una contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2','placeholder':'Repita la contraseña'}) 
        # Devolvemos el formulario
        return form
# Nueva vista para servir los perfiles 
# Solo debe ser accesible a usuarios logeados por lo que utilizamos un decorador para q si no esta logeado rediriga a la 
# pagina de login 
@method_decorator(login_required, name = 'dispatch')
class ProfileUpdate(UpdateView):
    form_class = ProfileForm
    #fields = ['avatar','bio','link']
    template_name = 'registration/profile_form.html'
    # Recuperamos el id del usuario que se almacena en request
    # para ello sobrescribimos el metodo get_object
    # Recuperamos el objeto q se va a editar, usamos el método get_or_create q busca un objeto y 
    #si no lo encuenta lo crea
    def get_object(self):
        profile, created =  Profile.objects.get_or_create(user = self.request.user)
        return profile 

    def get_success_url(self):
        return reverse_lazy('profile')+'?profile_updated'

# Nueva vista para modificar el email 
@method_decorator(login_required, name = 'dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    template_name = 'registration/profile_email_form.html'
    
    def get_object(self):
        
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')+ '?email_updated'

    # sobreescribimos el widget en tiempo de ejecución
    def get_form(self, form_class = None):
        form = super(EmailUpdate, self).get_form()
        # Modficamos en tiempo real 
        form.fields['email'].widget = forms.EmailInput(
            attrs = {'class':'form-control mb-2', 'placeholder':'Email'})
        return form
