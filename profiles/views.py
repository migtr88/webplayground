from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from registration.models import Profile

# Create your views here.
class ProfilesListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'
    # Establecemos el número de elementos a mostrar en cada página 
    paginate_by = 3

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiles/profile_detail.html'
    # Sobreescribimis el metodo get_object para recuperar el perfil a través del username
    def get_object(self):
        return get_object_or_404(Profile, user__username=self.kwargs['username'])