# Guía: Gestión de Acudientes y Estudiantes

## Descripción General

El sistema permite:
1. **Estudiantes**: Se registren de forma pública con un código único
2. **Acudientes**: Sean creados por el administrador y relacionados con estudiantes
3. **Relación**: Los acudientes acceden a través del código de su hijo

---

## Proceso 1: Crear un Estudiante

### Opción A: Registro Público (El estudiante se registra a sí mismo)

1. El estudiante va a la página de **Registro** (`/usuarios/registro/`)
2. Completa los siguientes campos:
   - **Datos Personales**: Nombre, Apellido, Email, Teléfono, Fecha de Nacimiento
   - **Credenciales**: Usuario, Contraseña (confirmada)
   - **Código de Acceso**: Debe ingresar el código único que le proporcionó la institución
   - **Foto de Perfil**: Opcional

3. El código de estudiante es **OBLIGATORIO** y debe ser **ÚNICO** en el sistema
4. Una vez registrado, el estudiante queda listo para que acudientes se relacionen con él

### Opción B: Creación por el Administrador

1. El administrador inicia sesión
2. Va a **Usuarios → Nuevo Usuario**
3. Selecciona **Rol: Estudiante**
4. Completa los datos y establece el **Código de Estudiante**
5. Generalmente se usa un código como: `EST001`, `EST002`, etc.

---

## Proceso 2: Crear un Acudiente y Relacionarlo con un Estudiante

### Pasos:

1. El administrador inicia sesión

2. Va a **Usuarios → Nuevo Usuario**

3. Rellena los datos básicos:
   - Nombre
   - Apellido
   - Email
   - Teléfono
   - Rol: **Selecciona "Acudiente"**

4. Establece las credenciales:
   - Usuario (ej: `padre_juan`)
   - Contraseña

5. **Fundamental**: En el campo **"Código del Hijo"**, ingresa el código del estudiante a relacionar
   - Si el código no existe o no corresponde a un estudiante, mostrará un error
   - Este código debe coincidir exactamente con el de un estudiante registrado

6. Haz clic en **"Crear"**

7. El acudiente queda relacionado con el estudiante y puede acceder al sistema

---

## Gestión de Usuarios (Lista de Usuarios)

### Acceso

Ir a **Usuarios → Lista de Usuarios**

### Información Mostrada

Para cada usuario se muestra:
- **Nombre y Foto** (si existe)
- **Username**
- **Rol** (con código de color):
  - 🔴 Administrador
  - 🔵 Profesor
  - 🟢 Estudiante
  - 🟡 Acudiente
- **Email**
- **Código/Relación**:
  - **Estudiante**: Muestra su código único
  - **Acudiente**: Muestra a qué estudiante está relacionado

### Filtrar por Rol

Usa el dropdown para ver solo usuarios de un rol específico

---

## Editando Usuarios Existentes

### Para un Estudiante

1. Haz clic en **Editar** del estudiante
2. Puedes cambiar:
   - Datos personales
   - Email
   - Fotografia
   - **Código de Estudiante** (debe seguir siendo único)

### Para un Acudiente

1. Haz clic en **Editar** del acudiente
2. Puedes cambiar:
   - Datos personales
   - Email
   - **Código del Hijo**: Usa este campo para relacionarlo con otro estudiante
   - Busca el código exacto del estudiante

---

## Validaciones Importantes

### Código de Estudiante
- ✅ **Obligatorio** para estudiantes
- ✅ **Único** en el sistema (no puede haber dos estudiantes con el mismo código)
- ✅ Usado por acudientes para relacionarse

### Código del Hijo (Acudiente)
- ✅ **Opcional** al crear (puede asignarse después)
- ✅ Debe corresponder a un estudiante existente en el sistema
- ✅ Pueden editarse en cualquier momento

---

## Ejemplos de Uso

### Ejemplo 1: Institución con códigos predeterminados

**Paso 1**: El admin genera códigos para todos los estudiantes (EST001, EST002, etc.)

**Paso 2**: Los estudiantes se registran usando su código

**Paso 3**: El admin crea a los acudientes y los relaciona con los códigos

```
Estudiante 1: Juan Pérez - Código: EST001
Acudiente: María López - Código del Hijo: EST001
```

### Ejemplo 2: Registro abierto

**Paso 1**: Los estudiantes se registran con cualquier código que elijan

**Paso 2**: El admin verifica la lista de estudiantes

**Paso 3**: El admin crea a los acudientes manualmente o los acudientes se auto-registran (si está habilitado)

---

## Troubleshooting

### "El código del hijo no corresponde a ningún estudiante"

- Verifica que el código exista exactamente igual
- Asegúrate de que el usuario con ese código sea un ESTUDIANTE
- Revisa la lista de estudiantes si es necesario

### No puedo crear un estudiante con ese código

- Ese código ya está en uso por otro estudiante
- Cambia el código o usa uno diferente

### El acudiente no ve al estudiante

- Verifica que el código del hijo coincida exactamente
- Asegúrate de que el estudiante esté activo en el sistema

---

## Dashboard para Acudientes

Una vez que el acudiente inicia sesión, podrá ver:
- Información de su hijo (estudiante)
- Calificaciones
- Asistencia
- Actividades y tareas
- Información académica

(Según lo configurado en el dashboard)

---

## Notas de Seguridad

- 🔒 Los acudientes solo ven información de su hijo
- 🔒 Los estudiantes solo ven su propia información
- 🔒 Existe un sistema de validación que previene relaciones incorrectas
- 🔒 Los códigos de estudiante son únicos para evitar duplicados
