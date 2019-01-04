from django.test import TestCase
from .models import Profile
from django.contrib.auth.models import User

# Create your tests here.
# Vamos a crear una prueba unitaria que se encargue automatizar la creación de un usuario y que luego creé
# un perfil y compruebe que se ha creado
class ProfileTestCase(TestCase):
    # Se crea el usuario de prueba
    def setUp(self):
        User.objects.create_user('test', 'test@test.es', 'test1234')
    # Se define el test en si 
    def test_profile_exists(self):
        # Comprobamos si existe un perfil con usuario test
        exists = Profile.objects.filter(user__username = 'test').exists()
        # Ejecutamos el test case, comparamos q exists sea true
        self.assertEqual(exists, True)
        