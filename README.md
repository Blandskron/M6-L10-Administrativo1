# Proyecto de Autenticación y Gestión de Usuarios

Este proyecto es una aplicación Django que integra Django REST Framework (DRF) y `drf-spectacular` para la documentación automática de la API. Permite registrar, listar, actualizar y eliminar usuarios, así como gestionar sus perfiles con foto. Además, incluye una capa de front-end interno (`front_user`) que interactúa con la API (`user_api`) y una sección de documentación (`docs`).

## Características Principales

- **API REST con DRF**:  
  Ofrece endpoints protegidos que requieren autenticación para acceder a datos sensibles de usuarios.
  
- **Autenticación por Sesión**:  
  El proyecto implementa un endpoint de login en `user_api` que permite autenticar usuarios y generar una sesión válida para acceder a los endpoints protegidos.

- **Perfiles de Usuario con Foto**:  
  Mediante señales, al crear un usuario se genera automáticamente su perfil. La API admite subir una foto y redimensionarla si excede cierto tamaño.

- **Front-end Interno**:  
  La app `front_user` permite crear cuentas de usuario localmente, iniciar sesión internamente en el proyecto, guardar credenciales y usarlas para autenticarse contra la API. El front-end muestra vistas HTML para listar, actualizar y ver el detalle de usuarios aprovechando la funcionalidad de `user_api`.

- **Documentación con drf-spectacular**:  
  Incluye endpoints para acceder a la documentación Swagger y Redoc generadas automáticamente. Esto facilita la comprensión y consumo de la API por parte de otros desarrolladores.

## Tecnologías Utilizadas

- **Django 5.1.4**: Framework principal para el desarrollo del proyecto.
- **Django REST Framework 3.15.2**: Para crear la API REST y gestionar permisos, serialización y vistas.
- **drf-spectacular 0.28.0**: Para generar documentación OpenAPI y proveer vistas Swagger y Redoc.
- **Pillow 11.0.0**: Para manejar la carga y manipulación de imágenes (fotos de perfil).
- **Requests 2.32.3**: Utilizado en `front_user` para consumir la API de `user_api`.
- **PyYAML 6.0.2**, **jsonschema 4.23.0**, **idna 3.10**, **urllib3 2.2.3**, entre otras librerías, utilizadas por drf-spectacular, requests y otros componentes de la stack.

## Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/tu-repo.git
   cd tu-repo
   ```

2. **Crear y activar un entorno virtual (opcional)**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
   
   El archivo `requirements.txt` debe contener las librerías mencionadas, por ejemplo:
   ```  
   asgiref==3.8.1
   attrs==24.2.0
   certifi==2024.8.30
   charset-normalizer==3.4.0
   Django==5.1.4
   djangorestframework==3.15.2
   drf-spectacular==0.28.0
   idna==3.10
   inflection==0.5.1
   jsonschema==4.23.0
   jsonschema-specifications==2024.10.1
   pillow==11.0.0
   PyYAML==6.0.2
   referencing==0.35.1
   requests==2.32.3
   rpds-py==0.22.3
   sqlparse==0.5.2
   tzdata==2024.2
   uritemplate==4.1.1
   urllib3==2.2.3
   ```

4. **Ejecutar migraciones y levantar el servidor**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

5. **Acceder a la aplicación**:
   - Front-end interno: `http://127.0.0.1:8000/users/` (lista de usuarios)
   - Registro: `http://127.0.0.1:8000/register/`
   - Login interno: `http://127.0.0.1:8000/login/`
   - API Endpoints (protegidos): `http://127.0.0.1:8000/user_api/users/`
   - Documentación:
     - Swagger UI: `http://127.0.0.1:8000/docs/swagger/`
     - Redoc: `http://127.0.0.1:8000/docs/redoc/`
     - Esquema OpenAPI: `http://127.0.0.1:8000/docs/schema/`

## Flujo de Trabajo

1. **Registro de Usuarios (Interno)**:  
   Desde `front_user`, un usuario puede registrarse sin autenticación en `http://127.0.0.1:8000/register/`. Esto crea un usuario y su perfil en la base de datos.

2. **Login Interno**:  
   El usuario se loguea con `http://127.0.0.1:8000/login/`. Esto almacena las credenciales en la sesión del front, permitiendo que `front_user` use dichas credenciales para autenticarse ante `user_api`.

3. **Autenticación ante `user_api`**:  
   `front_user` usa las credenciales guardadas para llamar a `http://127.0.0.1:8000/user_api/login/` y crear una sesión en `user_api`. Una vez autenticado, se pueden listar usuarios, obtener detalles, actualizar o eliminar desde `front_user` utilizando la API.

4. **Gestión de Usuarios vía API**:  
   Con la sesión establecida, `front_user` puede hacer `GET` / `POST` / `PUT` / `PATCH` / `DELETE` a la API de usuarios, según los permisos y la lógica definida en `UserViewSet`.

## Estructura del Proyecto

```
Autenticacion/
├─ Autenticacion/
│  ├─ settings.py
│  ├─ urls.py
│  └─ ...
│
├─ user_api/
│  ├─ models.py         # UserProfile y lógica para fotos
│  ├─ serializers.py    # UserSerializer, UserProfileSerializer
│  ├─ views.py          # UserViewSet, user_api_login
│  ├─ urls.py           # rutas de la API
│  ├─ signals.py        # creación automática de perfil de usuario
│  └─ apps.py
│
├─ docs/
│  ├─ urls.py           # rutas de documentación (schema, swagger, redoc)
│  └─ ...
│
├─ front_user/
│  ├─ views.py          # lógicas de frontend interno, login, registro, list_users, etc.
│  ├─ urls.py           # rutas del front interno
│  └─ templates/
│     └─ front_user/
│        ├─ login.html, register.html, list_users.html, etc.
│
└─ requirements.txt
```

## Estado del Proyecto

- Esta versión es funcional y coherente, pero puede mejorarse:
  - Enfocar la autenticación en métodos más seguros (ej. tokens, JWT).
  - Añadir tests automatizados.
  - Mejorar manejo de errores y validaciones más complejas.

## Nivel de Complejidad

El proyecto presenta una complejidad intermedia. Integra múltiples apps, documentación automática, autenticación y un front interno. Es un buen punto de partida para construir soluciones más avanzadas.

## Licencia

Este proyecto se distribuye bajo la licencia [MIT](LICENSE).
