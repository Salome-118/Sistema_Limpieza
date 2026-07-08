# Sistema de Productos de Limpieza — Aplicación Web

Aplicación web para gestionar el inventario de un negocio de productos de limpieza,
con autenticación de usuarios y CRUD de productos, desarrollada como
proyecto final de la carrera de Desarrollo de Software (ISTC CENESTUR).
Incluye control de versiones con flujo de ramas, tests automáticos, integración
continua (CI) y despliegue en Azure App Service.

---

## 1. Stack tecnológico (respuestas a lo que pide el proyecto)

| Pregunta | Respuesta |
|---|---|
| ¿Es una aplicación web? | Sí, aplicación web completa (backend + frontend). |
| Lenguaje y versión | **Python 3.12** |
| Framework | **Flask 3.0** |
| ORM y comando | **SQLAlchemy** (vía Flask-SQLAlchemy). El comando para crear las tablas es `flask --app wsgi init-db`. Para migraciones se usa Flask-Migrate: `flask db init`, `flask db migrate`, `flask db upgrade`. |
| Base de datos y versión | **PostgreSQL 16** (Azure Database for PostgreSQL Flexible Server). En local se usa SQLite automáticamente para poder probar sin configurar nada. |
| Repositorio | GitHub con rama `main` protegida y trabajo mediante ramas + Pull Requests. |
| Servidor de producción | Gunicorn sobre Azure App Service. |

> Nota: el proyecto también podría hacerse en PHP + Laravel. Aquí se eligió
> Python + Flask porque es el stack con el que ya se tiene experiencia previa
> (Flask, PostgreSQL y Azure), lo que reduce el riesgo para la entrega.

---

## 2. ¿Qué hace la aplicación?

- Registro de usuarios (con contraseña cifrada, nunca en texto plano).
- **Formulario de login** que valida credenciales e inicia sesión.
- Panel de inventario protegido: solo accesible con sesión iniciada.
- CRUD de productos de limpieza: agregar, listar, buscar, editar y eliminar.
- Campos por producto: nombre, marca, categoría, precio y stock.
- Alerta visual de "stock bajo" cuando quedan 5 unidades o menos.
- Cada usuario gestiona su propio inventario.
- Cierre de sesión.

## 3. Estructura del proyecto

```
gestor-tareas/
├── app/
│   ├── __init__.py        # Fábrica de la app (application factory)
│   ├── config.py          # Configuración (lee DATABASE_URL del entorno)
│   ├── models.py          # Modelos ORM: User, Producto
│   ├── forms.py           # Formularios (login, registro, producto)
│   ├── routes/
│   │   ├── auth.py        # Rutas: registro, login, logout
│   │   └── main.py        # Rutas: inicio, inventario, CRUD de productos
│   ├── templates/         # Plantillas HTML (Jinja2)
│   └── static/css/        # Estilos
├── tests/                 # Pruebas con pytest (10 tests)
├── .github/workflows/
│   └── ci.yml             # Integración continua (corre los tests en cada PR)
├── requirements.txt       # Dependencias
├── wsgi.py                # Punto de entrada
├── startup.sh             # Comando de arranque en Azure
├── .env.example           # Plantilla de variables de entorno
├── .gitignore
└── README.md
```

---

## 4. Cómo ejecutar en local (paso a paso)

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/sistema-limpieza.git
cd sistema-limpieza

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Copiar variables de entorno
cp .env.example .env            # En Windows: copy .env.example .env

# 5. Crear las tablas de la base de datos
flask --app wsgi init-db

# 6. Arrancar la aplicación
python wsgi.py
```

Abrir el navegador en **http://127.0.0.1:5000**.

---

## 5. Ejecutar los tests

```bash
pytest -v
```

Los tests validan: página de inicio, apertura del formulario de login, registro,
login correcto e incorrecto, protección del inventario y el CRUD de productos.

---

## 6. Flujo de trabajo con Git (ramas, nada directo a main)

**Regla de oro: nunca se hace push directo a `main`.** Todo el trabajo se hace en
ramas y se integra a `main` mediante Pull Request, solo si los tests pasan.

### 6.1 Configuración inicial del repositorio

```bash
git init
git add .
git commit -m "Commit inicial: estructura del proyecto"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/sistema-limpieza.git
git push -u origin main
```

### 6.2 Proteger la rama main en GitHub

En GitHub: **Settings → Branches → Add branch ruleset (o Add rule)** y sobre `main`:
- Activar *Require a pull request before merging*.
- Activar *Require status checks to pass before merging* y seleccionar el check `test`.
- (Opcional) *Require approvals*.

Así GitHub bloquea cualquier push directo a `main` y exige PR + tests en verde.

### 6.3 Trabajar una funcionalidad (ejemplo con el login)

```bash
# 1. Crear una rama para la funcionalidad
git checkout -b feature/login

# 2. Hacer los cambios en la computadora (local)...
#    editar archivos, probar con python wsgi.py

# 3. Guardar y subir a GitHub
git add .
git commit -m "feat: formulario de login funcionando"
git push -u origin feature/login

# 4. En GitHub: abrir un Pull Request de feature/login hacia main
#    -> GitHub Actions ejecuta los tests automáticamente
#    -> Si los tests pasan (check en verde), se aprueba el merge
#    -> Merge del Pull Request a main

# 5. Volver a main y actualizar en local
git checkout main
git pull origin main
```

Este es exactamente el ciclo que pide el proyecto:
abrir el formulario del login → cambio local → subir a GitHub → aprobar los tests →
aprobar el merge → deploy.

---

## 7. Despliegue en Azure App Service (deploy)

### 7.1 Crear la base de datos PostgreSQL

1. En el portal de Azure, crear un **Azure Database for PostgreSQL Flexible Server**.
2. Crear una base de datos (por ejemplo `limpiezadb`).
3. En *Networking*, permitir el acceso desde servicios de Azure.
4. Anotar la cadena de conexión.

### 7.2 Crear el App Service

1. Crear un **App Service** con pila de ejecución **Python 3.12** en Linux.
2. En **Configuración → Configuración de la aplicación**, agregar:
   - `SECRET_KEY` = una clave larga y aleatoria.
   - `DATABASE_URL` = `postgresql://USUARIO:PASSWORD@SERVIDOR.postgres.database.azure.com:5432/limpiezadb?sslmode=require`
3. En **Configuración → Configuración general → Comando de inicio**, poner:
   ```
   startup.sh
   ```

### 7.3 Conectar el despliegue con GitHub

1. En el App Service ir a **Centro de implementación (Deployment Center)**.
2. Elegir **GitHub** como origen y seleccionar el repositorio y la rama `main`.
3. Azure genera un workflow que despliega automáticamente cada vez que se
   mergea a `main`.

Resultado del flujo completo:
cambio local → push a rama → PR → tests aprobados → merge a main →
Azure despliega automáticamente la nueva versión.

### 7.4 Crear las tablas en producción

La primera vez, ejecutar la creación de tablas contra la base de Azure (por SSH
desde el portal del App Service, o localmente apuntando `DATABASE_URL` a Azure):

```bash
flask --app wsgi init-db
```

---

## 8. Seguridad y buenas prácticas aplicadas

- Contraseñas cifradas con hash (nunca en texto plano).
- Credenciales fuera del código: se leen de variables de entorno.
- `.env` excluido del repositorio mediante `.gitignore`.
- Protección CSRF en los formularios (Flask-WTF).
- Rama `main` protegida: solo se integra código probado.
- Tests automáticos ejecutados en cada Pull Request (CI).

---

## 9. Autora

Esthelita Salomé Chicaiza Yupangui — Desarrollo de Software, ISTC CENESTUR.

## Estado del proyecto
Aplicaci�n funcional con login, CRUD de productos, tests y despliegue en Azure.
