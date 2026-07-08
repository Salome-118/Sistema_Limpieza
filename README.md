Sistema de Productos de Limpieza — Aplicacion Web (LimpiaStock)

Aplicacion web para gestionar el inventario de un negocio de productos de limpieza,
con autenticacion de usuarios y CRUD de productos, desarrollada como proyecto final
de la carrera de Desarrollo de Software (ISTC CENESTUR). Incluye control de versiones
con flujo de ramas, tests automaticos, integracion continua (CI) y despliegue en
Azure App Service.


1. Stack tecnologico

PreguntaRespuestaTipo de aplicacionAplicacion web completa (backend + frontend).Lenguaje y versionPython 3.12FrameworkFlask 3.0ORM y comandoSQLAlchemy (via Flask-SQLAlchemy). Crear tablas: flask --app wsgi init-db. Migraciones: flask db init, flask db migrate, flask db upgrade.Base de datosPostgreSQL 16 (Azure Database for PostgreSQL Flexible Server). En local se usa SQLite automaticamente.RepositorioGitHub con rama main protegida y trabajo mediante ramas + Pull Requests.Servidor de produccionGunicorn sobre Azure App Service.


2. Que hace la aplicacion


Registro de usuarios (contrasena cifrada, nunca en texto plano).
Formulario de login que valida credenciales e inicia sesion.
Panel de inventario protegido: solo accesible con sesion iniciada.
CRUD de productos de limpieza: agregar, listar, buscar, editar y eliminar.
Campos por producto: nombre, marca, categoria, precio y stock.
Alerta visual de "stock bajo" cuando quedan 5 unidades o menos.
Cada usuario gestiona su propio inventario.
Cierre de sesion.



3. Estructura del proyecto

sistema-limpieza/
    app/
        __init__.py        Fabrica de la app (application factory)
        config.py          Configuracion (lee DATABASE_URL del entorno)
        models.py          Modelos ORM: User, Producto
        forms.py           Formularios (login, registro, producto)
        routes/
            auth.py        Rutas: registro, login, logout
            main.py        Rutas: inicio, inventario, CRUD de productos
        templates/         Plantillas HTML (Jinja2)
        static/css/        Estilos
    tests/                 Pruebas con pytest (10 tests)
    .github/workflows/
        ci.yml             Integracion continua (corre los tests en cada PR)
    requirements.txt       Dependencias
    wsgi.py                Punto de entrada
    startup.sh             Comando de arranque en Azure
    .env.example           Plantilla de variables de entorno
    .gitignore
    README.md


4. Como ejecutar en local

bash# 1. Clonar el repositorio
git clone https://github.com/Salome-118/Sistema_Limpieza.git
cd Sistema_Limpieza

# 2. Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate        # En Windows (PowerShell)

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Copiar variables de entorno
copy .env.example .env       # En Windows

# 5. Crear las tablas de la base de datos
flask --app wsgi init-db

# 6. Arrancar la aplicacion
python wsgi.py

Abrir el navegador en http://127.0.0.1:5000


Nota: si tu Python es muy reciente y falla la instalacion de psycopg2-binary,
puedes instalar en local sin esa libreria (solo se necesita en Azure):
pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-Login Flask-WTF email-validator python-dotenv pytest




5. Ejecutar los tests

bashpytest -v

Los tests validan: pagina de inicio, apertura del formulario de login, registro,
login correcto e incorrecto, proteccion del inventario y el CRUD de productos.


6. Flujo de trabajo con Git (nada directo a main)

Regla de oro: nunca se hace push directo a main. Todo el trabajo se hace en ramas
y se integra a main mediante Pull Request, solo si los tests pasan.

6.1 Proteger la rama main en GitHub

En GitHub: Settings -> Branches -> Add classic branch protection rule, sobre main:


Activar "Require a pull request before merging".
Activar "Require status checks to pass before merging".


6.2 Trabajar una funcionalidad

bash# 1. Crear una rama para la funcionalidad
git checkout -b feature/nombre-funcionalidad

# 2. Hacer los cambios en local y probarlos...

# 3. Guardar y subir a GitHub
git add .
git commit -m "feat: descripcion del cambio"
git push -u origin feature/nombre-funcionalidad

# 4. En GitHub: abrir un Pull Request de la rama hacia main
#    -> GitHub Actions ejecuta los tests automaticamente
#    -> Si los tests pasan, se aprueba el merge
#    -> Merge del Pull Request a main

# 5. Volver a main y actualizar en local
git checkout main
git pull origin main

Este es el ciclo que pide el proyecto: cambio local -> subir a GitHub ->
aprobar los tests -> aprobar el merge -> deploy.


7. Despliegue en Azure App Service


Crear un Azure Database for PostgreSQL Flexible Server y una base de datos (ej. limpiezadb).
En Networking, permitir el acceso desde servicios de Azure.
Crear un App Service con pila de ejecucion Python 3.12 en Linux.
En Configuracion -> Configuracion de la aplicacion, agregar:

SECRET_KEY = una clave larga y aleatoria.
DATABASE_URL = postgresql://USUARIO:PASSWORD@SERVIDOR.postgres.database.azure.com:5432/limpiezadb?sslmode=require



En Configuracion -> Configuracion general -> Comando de inicio, poner: startup.sh
En el Centro de implementacion, conectar el repositorio de GitHub y la rama main.
La primera vez, crear las tablas por SSH: flask --app wsgi init-db


Flujo completo: cambio local -> push a rama -> PR -> tests aprobados -> merge a main ->
Azure despliega automaticamente.


8. Seguridad y buenas practicas


Contrasenas cifradas con hash (nunca en texto plano).
Credenciales fuera del codigo: se leen de variables de entorno.
.env excluido del repositorio mediante .gitignore.
Proteccion CSRF en los formularios (Flask-WTF).
Rama main protegida: solo se integra codigo probado.
Tests automaticos ejecutados en cada Pull Request (CI).



9. Autora

Esthelita Salome Chicaiza Yupangui — Desarrollo de Software, ISTC CENESTUR.