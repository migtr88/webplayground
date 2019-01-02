from django.contrib import admin
from .models import Page

# Register your models here.
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    #Para q ckeditor se adapte al tamaño de pantalla en el administrador de django
    #Inyectamos nuestro fichero css 
    class Media: 
        css = {
            'all': ('pages/css/custom_ckeditor.css',)
        }
admin.site.register(Page, PageAdmin)
