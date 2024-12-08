import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

BASE_API_URL = settings.BASE_API_URL

def authenticate_with_user_api(username, password):
    """
    Intenta autenticar con user_api usando el endpoint /user_api/login/.
    Devuelve una sesión autenticada o None si falla.
    """
    s = requests.Session()
    login_data = {'username': username, 'password': password}
    res = s.post(f"{BASE_API_URL}user_api/login/", data=login_data)
    if res.status_code == 200:
        return s
    return None

def list_users(request):
    """
    Lista usuarios desde user_api usando las credenciales guardadas en la sesión.
    Si no existen credenciales en la sesión, es que el usuario no se ha logueado o no
    tenemos credenciales para user_api.
    """
    api_username = request.session.get('api_username')
    api_password = request.session.get('api_password')
    
    if not api_username or not api_password:
        return HttpResponse("No se tienen credenciales para user_api. Por favor inicie sesión.", status=401)

    session = authenticate_with_user_api(api_username, api_password)
    if session is None:
        return HttpResponse("No se pudo autenticar con user_api con las credenciales proporcionadas.", status=401)

    response = session.get(f"{BASE_API_URL}user_api/users/")
    if response.status_code == 200:
        users = response.json()
        return render(request, 'front_user/list_users.html', {'users': users})
    else:
        return HttpResponse("Error al obtener la lista de usuarios", status=response.status_code)

def create_user(request):
    # Crear usuario internamente, sin depender de user_api
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        photo = request.FILES.get('photo')

        if not username or not password:
            return HttpResponse("Faltan campos obligatorios (username y password)", status=400)

        if User.objects.filter(username=username).exists():
            return HttpResponse("El nombre de usuario ya existe", status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        if photo and hasattr(user, 'profile'):
            user.profile.photo = photo
            user.profile.save()

        return redirect('front_user:login')
    return render(request, 'front_user/create_user.html')

def detail_user(request, user_id):
    # Si user_api requiere auth, debes usar la sesión como en list_users
    api_username = request.session.get('api_username')
    api_password = request.session.get('api_password')

    if api_username and api_password:
        session = authenticate_with_user_api(api_username, api_password)
        if session:
            response = session.get(f"{BASE_API_URL}user_api/users/{user_id}/")
        else:
            return HttpResponse("No se pudo autenticar con user_api con las credenciales almacenadas.", status=401)
    else:
        # Intento sin autenticar, puede resultar en 403
        response = requests.get(f"{BASE_API_URL}user_api/users/{user_id}/")

    if response.status_code == 200:
        user_data = response.json()
        return render(request, 'front_user/detail_user.html', {'user': user_data})
    else:
        return HttpResponse("Usuario no encontrado o acceso denegado", status=response.status_code)

def update_user(request, user_id):
    # Requiere auth en user_api
    api_username = request.session.get('api_username')
    api_password = request.session.get('api_password')
    if not api_username or not api_password:
        return HttpResponse("No se tienen credenciales para user_api. Por favor inicie sesión.", status=401)

    session = authenticate_with_user_api(api_username, api_password)
    if not session:
        return HttpResponse("No se pudo autenticar con user_api.", status=401)

    url = f"{BASE_API_URL}user_api/users/{user_id}/"
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        photo = request.FILES.get('photo')

        data = {'username': username, 'email': email}
        if password:
            data['password'] = password

        files = {}
        if photo:
            files['profile.photo'] = (photo.name, photo.read(), photo.content_type)

        response = session.put(url, data=data, files=files)
        if response.status_code == 200:
            return redirect('front_user:detail_user', user_id=user_id)
        else:
            return HttpResponse(f"Error al actualizar usuario: {response.text}", status=response.status_code)
    else:
        response = session.get(url)
        if response.status_code == 200:
            user_data = response.json()
            return render(request, 'front_user/update_user.html', {'user': user_data})
        else:
            return HttpResponse("Usuario no encontrado o acceso denegado", status=response.status_code)

# Repite la lógica de obtener `api_username` y `api_password` de la sesión y autenticar antes de hacer PATCH, DELETE, etc.
# igual que en update_user.

def login_view(request):
    """
    Vista de login interno.
    Además de autenticar al usuario en el sistema local de Django, guardaremos las credenciales
    ingresadas en la sesión para usarlas con user_api.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Autenticar localmente
            login(request, user)
            # Guardar credenciales para user_api (en texto plano, porque user_api las necesita así)
            request.session['api_username'] = username
            request.session['api_password'] = password
            return redirect('front_user:list_users')
        else:
            return HttpResponse("Credenciales inválidas", status=401)

    return render(request, 'front_user/login.html')


def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        photo = request.FILES.get('photo')

        if not username or not password:
            return HttpResponse("Username y password son obligatorios.", status=400)

        if User.objects.filter(username=username).exists():
            return HttpResponse("El nombre de usuario ya existe.", status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        if photo and hasattr(user, 'profile'):
            user.profile.photo = photo
            user.profile.save()

        return redirect('front_user:login')
    
    return render(request, 'front_user/register.html')
