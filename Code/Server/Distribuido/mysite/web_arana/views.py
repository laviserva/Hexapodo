import platform
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required

import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
server_dir = current_dir.parent.parent
print(server_dir)
sys.path.append(str(server_dir))

from sockets_connection import run_client, run_server
from load_configuration import ConfigManager

def index(request):
    if request.method == 'GET':
        return render(request, 'hexa/index.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'hexa/index.html', {'form': AuthenticationForm, 'bandera': True})
        else:
            login(request, user)
            return redirect('inicio1')
def inicio(request,room_name):
    if request.method == 'GET':
        return render(request, 'hexa/inicio.html',{"room_name": room_name})
    else:
        data = json.loads(request.body)  # Carga los datos JSON de la solicitud
        message = data.get('message')  
        print("mensaje")
        print(message)

        data = {}
        for i, m in enumerate(message):
            data[i] = m
        
        print('data: ', data)
        data = {
            1: ["ctrl-avanzar", "15"],
             }
        
        system_os = platform.system()
        config = ConfigManager.get_config()
        port = int(config['CONNECTION']['PORT'])

        if system_os == 'Windows':
            print("[Servidor]: Configurando este dispositivo como servidor...")
            ip = '0.0.0.0'
            _, connection = run_server(ip = ip, port = port)

            try:
                json_data = json.dumps(data).encode('utf-8')
                connection.sendall(len(json_data).to_bytes(4, 'big'))
                connection.sendall(json_data)
                print("[Servidor]: Datos enviados.")

            finally:
                connection.close()

        return HttpResponse("hola")
def singout(request):
    logout(request)
    return redirect('index')
@csrf_exempt
def incio1(request):
    return render(request,'hexa/inicio1.html')


@require_http_methods(["POST"])
@csrf_exempt
def enviar_comando(request):
    try:
        data = json.loads(request.body)
        message = data.get('message')
        print(message)
        return JsonResponse({'Status': 'TODO BIEN','message':'mensaje entrgado'})
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error','message':'INVALIDO'}, status=400)