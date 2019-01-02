from django.shortcuts import render
from django.views.generic.base import TemplateView

#Ahora vamos a utilizar CBV (Class-Base View), nos permite generar vistas que son clases
#lo cual es de ayuda a la hora de definir vistas ya que nos permitirá reutilizarlas

class HomePageView(TemplateView):
    template_name = "core/home.html"
    #Como sobreescribir el diccionario de contexto para enviar nuestra propia información al template
    #def get_context_data(self, **kwargs):
        #recupera el diccionario de context con "super()", llamando a la propia función
        #context = super().get_context_data(**kwargs)
        #le definimos el valor que queramos pasarle al diccionario
       # context['title'] = "Mi super diccionario"
      #  return context
    #El método get proporciona la respuesta de la vista, aquí ira lo q quiera devolver
    #Devolvemos argumentos y argumentos en clave y valor(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        return(render(request, self.template_name,{'title':"Super webplayground"}))

class SamplePageView(TemplateView):
    template_name = "core/sample.html"

