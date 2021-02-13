from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Orden en que se despliegan las opciones en el dashboard del admin
    list_display = ('pk', 'user', 'phone_number', 'website', 'picture')

    # Elementos que se pueden hacer click para ir al detalle
    list_display_links = ('pk', 'user')

    # Elementos que se puede editar sin ir al detalle
    list_editable = ('phone_number', 'picture')

    # Elementos que se pueden relacionar con la busqueda
    search_fields = ('user__email', 'user__first_name', 'user__username')

    # Filtrar la busqueda por estos criterios
    list_filter = ('created', 'modified')

    # Orden en que se muestran los elementos en el detalle
    # Tupla con el nombre y un diccionario de tuplas
    fieldsets = (('Profile', {'fields': (('user', 'picture'), ('phone_number', 'bio'),)}),
                ('Extra info', {
                    'fields': ('website',)
                }),
                ('Metadata', {
                    'fields': ('created', 'modified')
                },)
    )

    # Elementos que solo son de lectura
    readonly_fields = ('created', 'modified')

# Esto se hace para que desde la creacion del user tambien se pueda crear el perfil 
# sin necesidad de tener que ir a otro apartado sino que aparece ahi abajo
class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInLine, )
    list_display = ('username', 'email', 'is_active', 'is_staff')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)