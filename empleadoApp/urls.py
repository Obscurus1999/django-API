from django.urls import path
from . import views

app_name ='trabajadores'
urlpatterns = [
    path('', views.index, name='agregar'),
    path('empleados/', views.listar_empleados, name='empleados'),
    path('actualizar_empleado/<int:id>/', views.editar_empleado, name='editar'),
    path('eliminar_empleado/<int:id>/', views.eliminar_empleado, name='eliminar'),

    # API endpoints
    path('api/trabajadores/', views.listar_empleados_api, name='api_listar'),
    path('api/trabajadores/<int:id>/', views.detalle_empleado, name='api_detalle'),

]