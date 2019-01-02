from django import forms
#Creamos un formulario enlazado con un modelo, para q se genere automaticamente
from .models import Page

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title','content','order']
        #Con widget editamos los campos para mostrarlos como queramos, con estilo
        widget = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Título'}),
            'content':forms.Textarea(attrs = {'class':'form-control'}),
            'order':forms.NumberInput(attrs ={'class':'form-control','placeholder':'Orden'}),
        }
    #Con labels indicamos que etiquetas de los campos queremos mostrar 
        labels = {
        'title':'', 'order':'','content':''
        }