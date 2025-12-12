# Pruebas de Selenium para Bienestar360

## 📋 Estructura Creada

### Features (Gherkin)
- `features/bienestar360_login.feature` - Pruebas de inicio de sesión
- `features/bienestar360_registration.feature` - Pruebas de registro de usuario
- `features/bienestar360_activities_filter.feature` - Pruebas de filtrado de actividades
- `features/bienestar360_tournament_creation.feature` - Pruebas de creación de torneos
- `features/bienestar360_tournament_results.feature` - Pruebas de registro de resultados de torneos
- `features/bienestar360_participation_registration.feature` - Pruebas de registro de participación
- `features/bienestar360_behavior_analysis.feature` - Pruebas de análisis de comportamiento estudiantil

### Page Objects
- `pages/bienestar360_login_page.py` - Página de inicio de sesión
- `pages/bienestar360_registration_page.py` - Página de registro de usuario
- `pages/bienestar360_homepage.py` - Página de inicio del usuario
- `pages/bienestar360_homepage_cadi.py` - Página de inicio del administrador (CADI)
- `pages/bienestar360_activities_page.py` - Página de actividades con filtros
- `pages/bienestar360_tournament_page.py` - Páginas de gestión de torneos (menú, creación, calendario)
- `pages/bienestar360_participation_segmentation_page.py` - Segmentación de participación (vista CADI)
- `pages/bienestar360_formal_report_page.py` - Reportes formales de participación (análisis de comportamiento)

### Steps
- `features/steps/bienestar360_login_steps.py` - Implementación de pasos de inicio de sesión
- `features/steps/bienestar360_registration_steps.py` - Implementación de pasos de registro
- `features/steps/bienestar360_activities_filter_steps.py` - Implementación de pasos de filtrado de actividades
- `features/steps/bienestar360_tournament_creation_steps.py` - Implementación de pasos de creación de torneos
- `features/steps/bienestar360_tournament_results_steps.py` - Implementación de pasos de registro de resultados de torneos
- `features/steps/bienestar360_participation_registration_steps.py` - Implementación de pasos de registro de participación
- `features/steps/bienestar360_behavior_analysis_steps.py` - Implementación de pasos de análisis de comportamiento estudiantil

## 🚀 Cómo Ejecutar

1. **Instala las dependencias necesarias (si no las tienes):**
   ```bash
   pip install -r requirements.txt
   # O instala manualmente:
   pip install selenium behave pyautogui
   ```
   
   **Nota:** `pyautogui` se usa para cerrar automáticamente los pop-ups de Chrome relacionados con contraseñas. Si no lo tienes instalado, las pruebas intentarán usar métodos alternativos, pero `pyautogui` es más efectivo para diálogos nativos del sistema.

2. **Asegúrate de que la aplicación Django esté corriendo:**
   ```bash
   docker-compose up
   # O
   python manage.py runserver
   ```

3. **Navega al directorio de pruebas:**
   ```bash
   cd selenium_tests
   ```

4. **Ejecutar las pruebas:**
   ```bash
   # Pruebas de inicio de sesión
   python -m behave features/bienestar360_login.feature
   
   # Pruebas de registro de usuario
   python -m behave features/bienestar360_registration.feature
   
   # Pruebas de filtrado de actividades
   python -m behave features/bienestar360_activities_filter.feature
   
   # Pruebas de creación de torneos
   python -m behave features/bienestar360_tournament_creation.feature
   
   # Pruebas de registro de resultados de torneos
   python -m behave features/bienestar360_tournament_results.feature
   
   # Pruebas de registro de participación
   python -m behave features/bienestar360_participation_registration.feature
   
   # Pruebas de análisis de comportamiento estudiantil
   python -m behave features/bienestar360_behavior_analysis.feature
   
   # Todas las pruebas de Bienestar360
   python -m behave features/bienestar360_*.feature
   
   # Todas las pruebas
   python -m behave
   ```
   
   **Nota:** En Windows PowerShell, usa `python -m behave` en lugar de solo `behave`. Si `behave` está en tu PATH, también puedes usar `behave` directamente.

## ⚙️ Configuración Necesaria

### 1. Credenciales de Prueba
Las credenciales de prueba están definidas en `bienestar360/login/signals.py` y se crean automáticamente:
- **Usuario básico (estudiante)**: `basicuser` / `password123`
- **Usuario admin**: `adminuser` / `adminpass`

Estas credenciales ya están configuradas en los archivos de steps. No necesitas cambiarlas a menos que modifiques las credenciales en `signals.py`.

### 2. URL Base
Si tu aplicación corre en un puerto diferente, edita las URLs en los Page Objects:
- `pages/bienestar360_login_page.py` - línea 20
- `pages/bienestar360_homepage.py` - línea 17
- `pages/bienestar360_social_projects_page.py` - línea 21
- `pages/bienestar360_activities_page.py` - línea 24

### 3. Datos de Prueba para Actividades
Las pruebas de filtrado de actividades requieren que existan actividades en la base de datos:
- Actividades de tipo "Artística"
- Actividades de tipo "Deportiva"
- Actividades con ubicaciones específicas (ej: "Coliseo", "203I")
- Actividades con horarios específicos

Puedes usar el seed de actividades:
```bash
cd bienestar360
python manage.py seed_data  # Desde el directorio bienestar360
```

### 4. Datos de Prueba para Torneos
Las pruebas de calendarios de torneos pueden crear torneos automáticamente, pero para crear partidos/juegos necesitan:
- Torneos creados (se crean automáticamente en las pruebas)
- Equipos o participantes (dependiendo de la modalidad del torneo)
- Los partidos/juegos se crean en las pruebas, pero pueden fallar si no hay equipos/participantes

**Nota:** Para crear partidos, primero se necesitan equipos (para torneos por equipos) o participantes (para torneos individuales). Las pruebas intentan crear partidos, pero si no hay equipos/participantes, este paso puede fallar. En un entorno de producción, deberías tener datos de prueba con equipos/participantes.

### 5. ChromeDriver
Asegúrate de tener ChromeDriver instalado y disponible en el PATH, o coloca `chromedriver.exe` en la raíz del proyecto `selenium_tests`.

## 🔧 Ajustar Selectores (Si es Necesario)

### Si un selector no funciona:

1. **Inspecciona el elemento en el navegador:**
   - Abre DevTools (F12)
   - Usa la herramienta de inspección
   - Identifica el selector único (ID, clase, XPath, etc.)

2. **Actualiza el Page Object correspondiente:**
   
   Por ejemplo, si el campo username no se encuentra:
   ```python
   # En pages/bienestar360_login_page.py
   # Cambiar de:
   USERNAME_FIELD = (By.ID, 'id_username')
   
   # A (ejemplo):
   USERNAME_FIELD = (By.NAME, 'username')  # Si usa name
   # O
   USERNAME_FIELD = (By.CSS_SELECTOR, 'input[type="text"]')  # Si usa CSS
   # O
   USERNAME_FIELD = (By.XPATH, '//input[@placeholder="Usuario"]')  # Si usa XPath
   ```

3. **Selectores comunes a verificar:**
   - **IDs**: `id="campo_id"` → `(By.ID, 'campo_id')`
   - **Clases**: `class="mi-clase"` → `(By.CLASS_NAME, 'mi-clase')` o `(By.CSS_SELECTOR, '.mi-clase')`
   - **Nombres**: `name="campo"` → `(By.NAME, 'campo')`
   - **Texto**: `Texto del enlace` → `(By.LINK_TEXT, 'Texto del enlace')`
   - **XPath**: Útil para elementos complejos

### Selectores que pueden necesitar ajuste:

1. **Login Page:**
   - `USERNAME_FIELD` - Campo de usuario
   - `PASSWORD_FIELD` - Campo de contraseña
   - `LOGIN_BUTTON` - Botón de login
   - `ERROR_MESSAGE` - Mensajes de error

2. **Homepage:**
   - `SOCIAL_PROJECTS_LINK` - Enlace a proyectos sociales

3. **Activities Page:**
   - `TYPE_FILTER` - Selector de tipo de actividad
   - `LOCATION_FILTER` - Campo de filtro por ubicación
   - `TIME_FILTER` - Campo de filtro por horario
   - `FILTER_BUTTON` - Botón de filtrar
   - `CLEAR_BUTTON` - Botón de limpiar
   - `ACTIVITY_CARDS` - Cards de actividades
   - `EMPTY_MESSAGE` - Mensaje cuando no hay actividades

4. **Tournament Pages:**
   - `CREATE_TOURNAMENT_BUTTON` - Botón para crear torneo
   - `CALENDAR_LINK` - Enlace al calendario
   - `TOURNAMENT_CARDS` - Cards de torneos
   - `CREATE_GAME_BUTTON` - Botón para crear partido
   - `CALENDAR_GRID` - Grid del calendario
   - `GAME_CARDS` - Cards de partidos en el calendario

## 📝 Notas

- Los selectores están basados en los templates HTML revisados
- Django genera IDs automáticamente para campos de formulario: `id_nombrecampo`
- Si los selectores no funcionan, inspecciona la página y actualiza los Page Objects
- Las pruebas asumen que hay datos de prueba en la base de datos

## 🐛 Troubleshooting

### Error: "Element not found"
- Verifica que el selector sea correcto
- Verifica que la página haya cargado completamente
- Aumenta el timeout en `BasePage` si es necesario

### Error: "Timeout waiting for element"
- Verifica que la URL sea correcta
- Verifica que la aplicación esté corriendo
- Verifica que los datos de prueba existan

### Error: "Invalid credentials"
- Actualiza las credenciales en los steps
- Verifica que el usuario de prueba exista en la base de datos

### Error: "ModuleNotFoundError: No module named 'pages'"
- Asegúrate de ejecutar `behave` desde el directorio `selenium_tests`
- Verifica que los archivos `__init__.py` estén presentes en las carpetas `pages` y `features/steps`

## 📌 Próximos Pasos

1. Ejecutar las pruebas y verificar qué selectores fallan
2. Inspeccionar los elementos que fallan y actualizar los selectores
3. Agregar más pruebas según necesidades
4. Configurar datos de prueba en la base de datos

## 🎯 Pruebas de Inicio de Sesión

### Escenarios Incluidos:

1. **Inicio exitoso con credenciales válidas (usuario básico)** - Verifica login exitoso y acceso a información
2. **Inicio exitoso con credenciales válidas (administrador)** - Verifica login de admin y acceso a CADI
3. **Inicio de sesión fallido con credenciales inválidas** - Verifica manejo de errores
4. **Inicio de sesión con campos vacíos** - Verifica validación de campos requeridos

### Verificaciones:

- ✅ Usuario puede ingresar credenciales
- ✅ Usuario accede a la aplicación después de login exitoso
- ✅ Usuario puede ver información que le corresponde
- ✅ Privilegios están correctamente aplicados (usuario básico vs administrador)
- ✅ Mensajes de error se muestran correctamente
- ✅ Usuario permanece en login cuando hay errores

## 🎯 Pruebas de Registro de Usuario

### Escenarios Incluidos:

1. **Se crea un usuario exitosamente** - Verifica registro completo y redirección
2. **Intento de registro con usuario existente** - Verifica manejo de usuarios duplicados
3. **Intento de registro con campos incompletos** - Verifica validación de campos requeridos
4. **Intento de registro con contraseñas que no coinciden** - Verifica validación de contraseñas

### Verificaciones:

- ✅ Usuario puede llenar formulario de registro
- ✅ Usuario es registrado exitosamente
- ✅ Mensaje de éxito se muestra (redirección a login)
- ✅ Errores se muestran para usuarios existentes
- ✅ Errores se muestran para campos incompletos
- ✅ Errores se muestran para contraseñas que no coinciden

### Notas Importantes:

- Las pruebas generan usuarios únicos automáticamente para evitar conflictos
- Después de registro exitoso, el usuario es redirigido a la página de login
- El sistema verifica que el usuario pueda hacer login después del registro

## 🎯 Pruebas de Filtrado de Actividades

### Escenarios Incluidos:

1. **Filtrar por tipo (Artística)** - Verifica que solo se muestren actividades artísticas
2. **Filtrar por tipo (Deportiva)** - Verifica que solo se muestren actividades deportivas
3. **Filtrar por horario** - Verifica filtrado por tiempo
4. **Filtros combinados (tipo + lugar)** - Verifica múltiples filtros
5. **Verificar elementos de filtro** - Verifica que todos los controles estén visibles

### Notas Importantes:

- Las pruebas NO requieren login (la vista es pública)
- Los filtros se aplican inmediatamente al hacer clic en "Filtrar"
- El botón "Limpiar" resetea todos los filtros
- Los horarios se comparan dentro de rangos (inicio-fin)

## 🎯 Pruebas de Creación de Torneos

### Escenarios Incluidos:

1. **Creación de torneo exitosa** - Verifica que se puede crear un torneo con toda la información necesaria y que aparece en la lista de torneos
2. **Registro de partidos en un torneo** - Verifica que se pueden registrar partidos con fechas y horarios, y que el calendario se genera automáticamente

### Flujo de Pruebas:

1. **Login como administrador** - Se autentica como admin de Bienestar Universitario
2. **Crear torneo** - Crea un torneo con nombre, deporte, género, modalidad, fecha de inicio y participantes máximos
3. **Verificar creación** - Verifica que el torneo se creó exitosamente y aparece en la lista de torneos disponibles
4. **Registrar partidos** - Intenta crear partidos/juegos con fechas y horarios (puede fallar si no hay equipos/participantes)
5. **Verificar calendario** - Verifica que el calendario se genera automáticamente después de registrar partidos

### Notas Importantes:

- Las pruebas **requieren login como administrador** para crear torneos
- Los torneos se crean con nombres únicos para evitar conflictos
- Para crear partidos, se necesitan equipos (torneos por equipos) o participantes (torneos individuales)
- Si no hay equipos/participantes, la creación de partidos puede fallar, pero el calendario aún se genera
- El calendario se genera automáticamente cuando se crean partidos con fechas y horarios
- Las pruebas verifican que el torneo aparece en la lista después de crearlo

### Verificaciones:

- ✅ Administrador puede crear torneos con toda la información requerida
- ✅ Torneo se crea exitosamente y aparece en la lista de torneos disponibles
- ✅ Administrador puede registrar partidos con fechas y horarios
- ✅ Calendario se genera automáticamente después de crear partidos
- ✅ Calendario muestra la estructura correcta (días, meses, navegación)

## 🎯 Pruebas de Registro de Resultados de Torneos

### Escenarios Incluidos:

1. **Ingreso de resultados de torneo** - Verifica que un miembro de Bienestar puede registrar el marcador de un partido finalizado

### Flujo de Pruebas:

1. **Autenticación** - El usuario se autentica como administrador de Bienestar Universitario
2. **Buscar partido finalizado** - Navega a la página de resultados y encuentra un partido que haya finalizado
3. **Registrar marcador** - Ingresa el marcador (home score y guest score) en el formulario
4. **Verificar actualización** - Verifica que el resultado se actualizó en la base de datos
5. **Verificar tabla** - Verifica que el resultado se refleja en la tabla de clasificación

### Notas Importantes:

- Las pruebas **requieren login como administrador** para registrar resultados
- Se asume que existe al menos un partido con fecha pasada (finalizado) en la base de datos
- El marcador se registra con valores de ejemplo (2-1)
- La prueba verifica que el resultado aparece en la página de resultados después de registrarlo

### Verificaciones:

- ✅ Administrador puede acceder a la página de registro de resultados
- ✅ Formulario permite ingresar marcador local y visitante
- ✅ Resultado se guarda exitosamente en la base de datos
- ✅ Resultado se refleja correctamente en la tabla de clasificación

## 🎯 Pruebas de Registro de Participación

### Escenarios Incluidos:

1. **Almacenar participación del estudiante** - Verifica que la información de participación se almacena y está disponible para reportes

### Flujo de Pruebas:

1. **Autenticación como administrador** - El usuario se autentica como administrador de Bienestar Universitario
2. **Verificar almacenamiento** - Navega a la segmentación de participación y verifica que hay datos almacenados
3. **Verificar disponibilidad** - Verifica que la información de participantes (ID, Nombre) y actividades se muestra correctamente

### Notas Importantes:

- Las pruebas **requieren login como administrador** para acceder a la segmentación de participación
- Se asume que **ya existen datos de participación** en la base de datos (creados por seed data o uso previo del sistema)
- La prueba verifica que la información se muestra correctamente en la tabla de segmentación
- Se valida que los estudiantes tienen ID y nombre, y que la información de la actividad está disponible

### Verificaciones:

- ✅ Administrador puede acceder a la página de segmentación de participación
- ✅ Hay datos de participación almacenados en la base de datos
- ✅ La información de participantes se muestra correctamente (ID y Nombre)
- ✅ La información de actividades se muestra correctamente (nombre, tipo, horario)
- ✅ La información está disponible para generar reportes posteriores

## 🎯 Pruebas de Análisis de Comportamiento Estudiantil

### Escenarios Incluidos:

1. **Generar reporte segmentado con filtros** - Verifica que se puede generar un reporte con filtros de frecuencia, tipo de actividad y características demográficas
2. **Generar reporte sin filtros** - Verifica que se puede generar un reporte con todos los datos

### Flujo de Pruebas:

1. **Autenticación como administrador** - El usuario se autentica como analista de Bienestar Universitario
2. **Navegar a reportes formales** - Accede a la página de reportes formales de participación
3. **Aplicar filtros** - Selecciona filtros de tipo de actividad, frecuencia, facultad, género, o fechas
4. **Generar reporte** - Hace clic en "Generar Reporte" y verifica que se muestran los datos segmentados
5. **Verificar exportación** - Verifica que los botones de exportación están disponibles (sin hacer descargas)

### Notas Importantes:

- Las pruebas **requieren login como administrador** para acceder a los reportes formales
- Se asume que **ya existen datos de participación** en la base de datos (creados por seed data o uso previo)
- Los filtros incluyen: tipo de actividad, facultad/programa, género, frecuencia (mín/máx), y rango de fechas
- Las pruebas solo verifican que los botones de exportación están disponibles, no realizan descargas reales

### Verificaciones:

- ✅ Analista puede acceder a la página de reportes formales
- ✅ Los filtros se pueden seleccionar correctamente (tipo de actividad, facultad, género, frecuencia, fechas)
- ✅ El reporte se genera correctamente después de aplicar filtros
- ✅ El reporte muestra estadísticas y datos segmentados
- ✅ El reporte se genera correctamente sin filtros (todos los datos)
- ✅ Los botones de exportación están disponibles (CSV)
- ✅ Los gráficos de comportamiento se muestran (si están disponibles)

