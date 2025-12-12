# Instrucciones para Ejecutar Pruebas Funcionales

## Pruebas Automatizadas (en entorno Docker)

### Ejecutar todas las pruebas
```bash
docker compose exec web python manage.py test reportsAndStats.tests.test_downloads
```

### Ejecutar pruebas específicas
```bash
# Solo pruebas de descarga de tablas
docker compose exec web python manage.py test reportsAndStats.tests.test_downloads.DownloadTableTests

# Solo pruebas de descarga de gráficos
docker compose exec web python manage.py test reportsAndStats.tests.test_downloads.DownloadChartTests

# Prueba específica
docker compose exec web python manage.py test reportsAndStats.tests.test_downloads.DownloadTableTests.test_download_excel_with_data
```

### Ver cobertura de pruebas
```bash
# Instalar coverage dentro del contenedor (solo si no está instalado)
docker compose exec web pip install coverage

# Ejecutar con coverage
docker compose exec web coverage run --source='reportsAndStats' manage.py test reportsAndStats.tests.test_downloads
docker compose exec web coverage report
docker compose exec web coverage html  # Genera el reporte HTML en htmlcov/
```

---

## Pruebas Manuales

### 1. Preparación del Entorno

1. **Iniciar los servicios del proyecto:**
   ```bash
   docker compose up
   ```

2. **Acceder al contenedor de la aplicación:**
   ```bash
   docker compose exec web bash
   ```

3. **Verificar que el servidor esté corriendo:**
   ```bash
   docker compose exec web python manage.py runserver 0.0.0.0:8000
   ```

4. **Acceder a la aplicación en el navegador:**
   - URL: `http://localhost:8000`
   - Iniciar sesión con un usuario CADI válido.

5. **Ir a la sección de reportes filtrados:**
   - Menú: `Reportes y Estadísticas > Reportes Filtrados`
   - URL: `http://localhost:8000/reportsAndStats/filtered/`

---

### 2. Checklist de Pruebas Rápidas

#### Descarga de Tablas

- [ ] **Excel con datos:**
  - Seleccionar un filtro con datos (por ejemplo, “Actividad”).
  - Clic en “Excel (.xlsx)”.
  - Verificar: mensaje de éxito, archivo descargado, datos coincidentes.

- [ ] **CSV con datos:**
  - Mismo filtro con datos.
  - Clic en “CSV (.csv)”.
  - Verificar: mensaje de éxito, archivo descargado, datos coincidentes.

- [ ] **Excel sin datos:**
  - Seleccionar un filtro sin datos.
  - Clic en “Excel (.xlsx)”.
  - Verificar: archivo descargado con mensaje “No hay datos disponibles”.

- [ ] **CSV sin datos:**
  - Mismo filtro sin datos.
  - Clic en “CSV (.csv)”.
  - Verificar: archivo descargado con mensaje “No hay datos disponibles”.

#### Descarga de Gráficos

- [ ] **PNG:**
  - Con datos visibles.
  - Clic en “PNG”.
  - Verificar: mensaje de éxito, imagen descargada, buena calidad.

- [ ] **JPEG:**
  - Clic en “JPEG”.
  - Verificar: mensaje de éxito, imagen descargada.

- [ ] **PDF:**
  - Clic en “PDF”.
  - Verificar: mensaje de éxito, archivo descargado con gráfico completo.

- [ ] **Gráfico sin datos:**
  - Intentar descargar sin datos disponibles.
  - Verificar: mensaje de error apropiado.

---

### 3. Pruebas de Compatibilidad entre Navegadores

#### Chrome
- Ejecutar todas las pruebas del checklist.

#### Firefox
- Ejecutar todas las pruebas del checklist.

#### Edge
- Ejecutar todas las pruebas del checklist.

#### Safari (si está disponible)
- Ejecutar todas las pruebas del checklist.

---

### 4. Pruebas de Validación de Datos

#### Comparación Tabla vs Excel
1. Anotar manualmente los datos visibles en la tabla:
   ```
   Actividad: X, Participación: Y, Actividades: Z
   ```
2. Descargar el archivo Excel.
3. Abrir el archivo.
4. Comparar fila por fila.
5. Verificar coincidencia exacta.

#### Comparación Tabla vs CSV
1. Registrar los mismos datos de la tabla.
2. Descargar el archivo CSV.
3. Abrirlo en Excel o en un editor de texto.
4. Comparar fila por fila.
5. Verificar coincidencia exacta.

#### Comparación Gráfico vs Imagen
1. Capturar pantalla del gráfico.
2. Descargar el PNG.
3. Comparar visualmente:
   - Colores.
   - Etiquetas.
   - Leyenda.
   - Valores.

---

### 5. Pruebas de Manejo de Errores

#### Filtro Inválido
1. Modificar la URL manualmente:
   ```
   http://localhost:8000/reportsAndStats/download-table-excel/?filter=invalid
   ```
2. Verificar: mensaje de error mostrado correctamente.

#### Error de Red
1. Desconectar la conexión a internet.
2. Intentar descargar un archivo.
3. Verificar: mensaje de error apropiado.

#### Datos Vacíos
1. Seleccionar un filtro sin datos.
2. Descargar tabla → Debe funcionar con mensaje informativo.
3. Descargar gráfico → Debe mostrar error.

---

## Herramientas para Verificar Archivos

- **Excel:** Microsoft Excel o LibreOffice Calc.  
- **CSV:** Excel o cualquier editor de texto.  
- **Imágenes:** Visor de imágenes del sistema.  
- **PDF:** Visor PDF estándar.
