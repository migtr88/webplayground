from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .models import Page
from .forms import PageForm

#Creamos un Mixin que nos permitirá implementar una funcionalidad que permita heredar, se lo pasaremos a la clase
# que nos interese como atributo,esto nos permite evitar repetir el mismo método en múltiples clases, reimplementamos el metodo dispatch
class StaffRequiredMixin(object):
    """ 
     Este mixin requerirá q el usuario sea miembro del staff
    """
    #Con los decoradores nos ahorraremos parte de la implementacion del metodo dispatch
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args,**kwargs):
        #print(request.user)
        #if not request.user.is_staff:
            #return redirect(reverse_lazy('admin:login'))
        return super(PageCreate,self).dispatch(request, *args,**kwargs)

# Create your views here.

class PageListView(ListView):
    model = Page

class PageDetailView(DetailView):
    model = Page
#utilizamos el decorador indicandole el metodo que queremos decorar
@method_decorator(staff_member_required, name = 'dispatch')
class PageCreate(CreateView):
    model = Page
    #Creamos nuestro formulario desde el modelo q tenemos
    form_class = PageForm
    #fields = ['title', 'content', 'order']
    #def get_success_url(self):
   #    return reverse('pages:pages')
    success_url = reverse_lazy('pages:pages')
    #Dispatch nos va a servir para ver que usuario esta accediendo, si no es administrador o esta autorizado redireccionamos 
    #a la página de login 
 

class PageUpdated(StaffRequiredMixin,UpdateView):
    model = Page
    #Creamos nuestro formulario desde el modelo q tenemos
    form_class = PageForm
    template_name_suffix = '_update_form'
#debemos redefinir el get_success, para pasarle la pk de la pagina actualizada,de manera 
#q nos devuelva la página actualizada
    def get_success_url(self):
        #Concatenamos una cadena al final del reverse lazy para q en la url aparezca un ok
        #diciendole al usurio q todo ha ido bien 
        return reverse_lazy('pages:update', args=[self.object.id]) + '?ok'
    

class PageDelete(StaffRequiredMixin,DeleteView): 
    model = Page
    success_url = reverse_lazy('pages:pages')