from django.shortcuts import render, redirect
from .models import Empleado
from . import forms
# Create your views here.
def index(request):
    form=forms.EmpleadoForm()
    if request.method=='POST':
        form=forms.EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return listar_empleados(request)
    data={'form':form}
    return render(request, 'empleadoApp/index.html', data)

def listar_empleados(request):
    empleados=Empleado.objects.all()
    data={'empleados':empleados}
    return render(request,'empleadoApp/empleados.html', data)

def editar_empleado(request, id):
    empleado = Empleado.objects.get(id=id)  # Buscar el registro a editar
    form = forms.EmpleadoForm(instance=empleado)
    if request.method == 'POST':
        form = forms.EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()  # Aquí actualiza el registro en lugar de crear uno nuevo
        return listar_empleados(request)#redirect('employee_list')
    data = {'form':form}
    return render(request, 'empleadoApp/index.html', data)
    
def eliminar_empleado(request,id):
    empleado=Empleado.objects.get(id=id)
    empleado.delete()
    return redirect( 'trabajadores:empleados')

from .serializers import EmpleadoSerializer
from .models import Empleado
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def listar_empleados_api(request):
    if request.method == 'GET':
        empleados = Empleado.objects.all()
        serializer = EmpleadoSerializer(empleados, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EmpleadoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def detalle_empleado(request, id):
    try:
        empleado = Empleado.objects.get(id=id)
    except Empleado.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmpleadoSerializer(empleado)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = EmpleadoSerializer(empleado, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        empleado.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    