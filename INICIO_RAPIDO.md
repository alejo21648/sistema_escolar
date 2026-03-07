# 🚀 Guía Rápida de Inicio - Sistema de Acudientes y Estudiantes

## Requisitos Previos

✅ Base de datos MySQL configurada  
✅ Entorno virtual de Python activado  
✅ Dependencias instaladas (`pip install -r requirements.txt`)

---

## Paso 1: Configurar la Base de Datos

### 1.1 Crear base de datos MySQL
```sql
CREATE DATABASE sistema_escolar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'django'@'localhost' IDENTIFIED BY 'tu_contraseña';
GRANT ALL PRIVILEGES ON sistema_escolar.* TO 'django'@'localhost';
FLUSH PRIVILEGES;
```

### 1.2 Configurar archivo `.env` (si existe)
```env
DB_ENGINE=mysql
DB_NAME=sistema_escolar
DB_USER=django
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=3306
```

### 1.3 Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Paso 2: Crear Superusuario (Admin)

```bash
python manage.py createsuperuser
```

Cuando solicite:
- Username: `admin` (o tu preferencia)
- Email: `admin@example.com`
- Password: Tu contraseña segura

---

## Paso 3: Iniciar el Servidor

```bash
python manage.py runserver
```

Acceder a:
- **Aplicación**: http://localhost:8000
- **Admin**: http://localhost:8000/admin/

---

## Paso 4: Crear Estudiantes

### Opción A: Registro Público (Recomendado para estudiantes)

1. Ir a http://localhost:8000/usuarios/registro/
2. Completar formulario:
   - Nombre, Apellido, Email
   - Usuario, Contraseña
   - **Código de Estudiante** (ej: `EST001`, `EST002`)
3. Se inicia sesión automáticamente
4. Acceso directo a Dashboard de Estudiante

### Opción B: Admin crea estudiante

1. Acceder a http://localhost:8000/admin/
2. **Usuarios → Usuarios → Añadir Usuario**
3. Llenar formulario:
   - Nombre de usuario
   - Contraseña
   - Información personal
4. En **"Rol"**: Seleccionar **"Estudiante"**
5. En **"Código de Estudiante"**: `EST001` (o similar, ÚNICO)
6. Guardar

---

## Paso 5: Crear Acudientes

### En el Admin de Django (Recomendado)

1. Acceder a http://localhost:8000/admin/
2. **Usuarios → Usuarios → Añadir Usuario**
3. Llenar datos básicos
4. En **"Rol"**: Seleccionar **"Acudiente"**
5. En **"Código del Hijo"**: Ingresa el código del estudiante
   - Ej: Si el estudiante es `EST001`, ingresa `EST001`
6. Si el código es válido, se guarda la relación
7. Guardar

### Otros lugares para crear acudientes

- http://localhost:8000/usuarios/crear/ (si eres admin)
- List: http://localhost:8000/usuarios/lista/

---

## Paso 6: Verificar Relaciones

### Admin de Django
1. Ir a http://localhost:8000/admin/usuarios/usuario/
2. Buscar o filtrar acudiente
3. Verificar que en **"Información de Relación"** dice:
   - ✓ Relacionado con: [Nombre del Estudiante]

### Aplicación
1. Ir a http://localhost:8000/usuarios/lista/
2. Ver tabla con columna **"Código/Relación"**
3. Para acudientes debe mostrar: "Relacionado con: [Nombre]"

---

## Paso 7: Probar como Acudiente

1. Ir a http://localhost:8000/usuarios/login/
2. Ingresar credenciales del acudiente
3. Se abre Dashboard del Acudiente con:
   - ℹ️ Información del hijo
   - 📊 Desempeño académico
   - 📅 Asistencia
   - 📝 Tareas pendientes
   - 💰 Cotizaciones

---

## Códigos de Ejemplo

### Crear estos estudiantes primero:

```
EST001  - Juan Pérez
EST002  - María García
EST003  - Carlos López
```

### Luego crear acudientes:

```
Usuario: padre_juan    / Código del Hijo: EST001
Usuario: madre_juan    / Código del Hijo: EST001
Usuario: padre_maria   / Código del Hijo: EST002
Usuario: padre_carlos  / Código del Hijo: EST003
```

---

## Validaciones Automáticas

✅ **Código de estudiante único**: No puede haber dos estudiantes con el mismo código  
✅ **Código del hijo válido**: Solo acepta códigos que existan y sean de estudiantes  
✅ **Rol obligatorio**: Es seleccionable al crear  
✅ **Contraseñas coinciden**: Valida que password1 = password2  

---

## Troubleshooting

### "Access denied for user 'django'@'localhost'"
**Solución**: Crear usuario MySQL o cambiar credenciales en settings.py

### "Este código de estudiante ya está en uso"
**Solución**: Usar otro código o editar el existente

### "El código del hijo no corresponde a ningún estudiante"
**Solución**: Verificar que el código existe en un estudiante

### Dashboard del acudiente no muestra información del hijo
**Solución**: Verificar que el acudiente tiene `codigo_hijo` establecido correctamente

---

## Estructura de URLs de Administración

```
/admin/                        - Panel admin de Django
/usuarios/                     - Sección de usuarios
/usuarios/login/               - Login
/usuarios/registro/            - Registro público de estudiantes
/usuarios/lista/               - Lista de usuarios (admin)
/usuarios/crear/               - Crear nuevo usuario (admin)
/usuarios/<id>/editar/         - Editar usuario (admin)
/usuarios/<id>/eliminar/       - Eliminar usuario (admin)
/dashboard/                    - Dashboard (automático según rol)
```

---

## Documentación Adicional

- **GUIA_ACUDIENTES.md**: Guía completa de funcionamiento
- **CAMBIOS_REALIZADOS.md**: Detalle técnico de cambios
- **MANUAL.md**: Manual general del sistema

---

## ✅ Checklist Final

- ✅ Base de datos configurada
- ✅ Migraciones ejecutadas
- ✅ Superusuario creado
- ✅ Servidor ejecutándose
- ✅ Estudiantes creados con códigos
- ✅ Acudientes creados y relacionados
- ✅ Relaciones verificadas
- ✅ Dashboard del acudiente funcional

---

¡Listo! El sistema está operativo. 🎉
