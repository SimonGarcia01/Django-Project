# Pruebas Funcionales - Descarga de Tablas y Gráficos

## Objetivo
Validar que la funcionalidad de descarga de tablas y gráficos funcione correctamente en todos los formatos definidos, con manejo adecuado de errores y compatibilidad entre navegadores.

---

## 1. Pruebas de Descarga de Tablas

### 1.1 Descarga en Formato Excel (.xlsx)

#### Caso de Prueba 1.1.1: Descarga exitosa con datos
**Precondiciones:**
- El usuario está en la página de reportes filtrados
- Existen datos de participación en la base de datos
- El filtro seleccionado muestra datos en la tabla

**Pasos:**
1. Seleccionar un filtro (actividad, facultad o género) que tenga datos
2. Verificar que la tabla muestre datos
3. Hacer clic en el botón "Excel (.xlsx)"
4. Verificar que se descargue el archivo
5. Abrir el archivo descargado

**Resultado Esperado:**
- Se muestra el mensaje "Descarga completada exitosamente"
- El archivo se descarga con nombre: `reporte_participacion_{filtro}_{timestamp}.xlsx`
- El archivo contiene:
  - Encabezados: [Filtro], Participación, Actividades
  - Los mismos datos que se muestran en la tabla de la pantalla
  - Formato correcto con estilos (encabezados en azul, texto centrado)
- Los datos coinciden exactamente con los mostrados en pantalla

**Navegadores a probar:**
- [ ] Chrome (última versión)
- [ ] Firefox (última versión)
- [ ] Edge (última versión)
- [ ] Safari (si está disponible)

---

#### Caso de Prueba 1.1.2: Descarga con datos vacíos
**Precondiciones:**
- El usuario está en la página de reportes filtrados
- No existen datos para el filtro seleccionado

**Pasos:**
1. Seleccionar un filtro que no tenga datos
2. Verificar que la tabla muestre "No hay datos para mostrar con este filtro"
3. Hacer clic en el botón "Excel (.xlsx)"

**Resultado Esperado:**
- Se descarga el archivo Excel
- El archivo contiene solo los encabezados y una fila con "No hay datos disponibles", 0, 0
- No se genera error

---

#### Caso de Prueba 1.1.3: Error simulado (filtro inválido)
**Precondiciones:**
- El usuario está en la página de reportes filtrados

**Pasos:**
1. Modificar manualmente la URL para incluir un filtro inválido: `?filter=invalid`
2. Intentar descargar el archivo Excel

**Resultado Esperado:**
- Se muestra el mensaje de error: "No fue posible generar el archivo, por favor intente nuevamente"
- No se descarga ningún archivo

---

### 1.2 Descarga en Formato CSV (.csv)

#### Caso de Prueba 1.2.1: Descarga exitosa con datos
**Precondiciones:**
- El usuario está en la página de reportes filtrados
- Existen datos de participación en la base de datos

**Pasos:**
1. Seleccionar un filtro que tenga datos
2. Verificar que la tabla muestre datos
3. Hacer clic en el botón "CSV (.csv)"
4. Verificar que se descargue el archivo
5. Abrir el archivo descargado en Excel o un editor de texto

**Resultado Esperado:**
- Se muestra el mensaje "Descarga completada exitosamente"
- El archivo se descarga con nombre: `reporte_participacion_{filtro}_{timestamp}.csv`
- El archivo contiene:
  - Encabezados: [Filtro], Participación, Actividades
  - Los mismos datos que se muestran en la tabla
  - Codificación UTF-8 con BOM (se ve correctamente en Excel)
- Los datos coinciden exactamente con los mostrados en pantalla
- La estructura y encabezados se conservan correctamente

**Navegadores a probar:**
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Safari

---

#### Caso de Prueba 1.2.2: Descarga con datos vacíos
**Precondiciones:**
- No existen datos para el filtro seleccionado

**Pasos:**
1. Seleccionar un filtro sin datos
2. Hacer clic en el botón "CSV (.csv)"

**Resultado Esperado:**
- Se descarga el archivo CSV
- El archivo contiene encabezados y una fila: "No hay datos disponibles",0,0
- No se genera error

---

## 2. Pruebas de Descarga de Gráficos

### 2.1 Descarga en Formato PNG

#### Caso de Prueba 2.1.1: Descarga exitosa
**Precondiciones:**
- El usuario está en la página de reportes filtrados
- Existe un gráfico visible con datos

**Pasos:**
1. Verificar que el gráfico se muestre correctamente
2. Hacer clic en el botón "PNG"
3. Verificar que se descargue la imagen

**Resultado Esperado:**
- Se muestra el mensaje "Descarga completada exitosamente"
- Se descarga un archivo PNG con nombre: `grafico_participacion_{timestamp}.png`
- La imagen contiene:
  - El gráfico completo con todos los colores originales
  - Las etiquetas y leyendas visibles
  - La misma información que se muestra en pantalla
- La calidad de la imagen es buena (sin pixelación)

**Navegadores a probar:**
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Safari

---

#### Caso de Prueba 2.1.2: Error con gráfico sin datos
**Precondiciones:**
- No hay datos para mostrar en el gráfico

**Pasos:**
1. Intentar descargar el gráfico cuando no hay datos

**Resultado Esperado:**
- Se muestra el mensaje de error: "No hay datos para generar el gráfico"
- No se descarga ningún archivo

---

### 2.2 Descarga en Formato JPEG

#### Caso de Prueba 2.2.1: Descarga exitosa
**Pasos:**
1. Verificar que el gráfico se muestre correctamente
2. Hacer clic en el botón "JPEG"
3. Verificar que se descargue la imagen

**Resultado Esperado:**
- Se muestra el mensaje "Descarga completada exitosamente"
- Se descarga un archivo JPEG con nombre: `grafico_participacion_{timestamp}.jpeg`
- La imagen contiene el gráfico completo con colores, etiquetas y leyendas
- La calidad es aceptable

**Navegadores a probar:**
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Safari

---

### 2.3 Descarga en Formato PDF

#### Caso de Prueba 2.3.1: Descarga exitosa
**Pasos:**
1. Verificar que el gráfico se muestre correctamente
2. Hacer clic en el botón "PDF"
3. Verificar que se descargue el PDF

**Resultado Esperado:**
- Se muestra el mensaje "Descarga completada exitosamente"
- Se descarga un archivo PDF con nombre: `grafico_participacion_{timestamp}.pdf`
- El PDF contiene:
  - El gráfico completo
  - Orientación horizontal (landscape)
  - Tamaño A4
  - Colores, etiquetas y leyendas preservados
  - Diseño visual igual al mostrado en pantalla

**Navegadores a probar:**
- [ ] Chrome
- [ ] Firefox
- [ ] Edge
- [ ] Safari

---

#### Caso de Prueba 2.3.2: Error con formato no soportado
**Pasos:**
1. Intentar llamar a la función con un formato inválido (ej: 'svg')

**Resultado Esperado:**
- Se muestra el mensaje de error: "No fue posible generar el archivo, por favor intente nuevamente"
- No se descarga ningún archivo

---

## 3. Pruebas de Coincidencia de Datos

### Caso de Prueba 3.1: Validación de datos entre pantalla y archivos

**Precondiciones:**
- Existen datos en la base de datos

**Pasos:**
1. Seleccionar un filtro con datos
2. Anotar manualmente los datos mostrados en la tabla
3. Descargar el archivo Excel
4. Descargar el archivo CSV
5. Comparar los datos

**Resultado Esperado:**
- Los datos en Excel coinciden exactamente con la tabla
- Los datos en CSV coinciden exactamente con la tabla
- Los encabezados son idénticos
- Los valores numéricos son exactos
- Los nombres/categorías coinciden

---

### Caso de Prueba 3.2: Validación de gráfico entre pantalla y archivo

**Pasos:**
1. Verificar el gráfico en pantalla
2. Descargar el gráfico en PNG
3. Comparar visualmente

**Resultado Esperado:**
- El gráfico descargado muestra los mismos datos
- Los colores coinciden
- Las etiquetas son las mismas
- La leyenda es idéntica

---

## 4. Pruebas de Compatibilidad entre Navegadores

### Navegadores a Probar:
1. **Google Chrome** (última versión)
2. **Mozilla Firefox** (última versión)
3. **Microsoft Edge** (última versión)
4. **Safari** (si está disponible en macOS)

### Funcionalidades a Validar en Cada Navegador:

#### Tablas:
- [ ] Descarga Excel funciona
- [ ] Descarga CSV funciona
- [ ] Mensajes de éxito se muestran
- [ ] Mensajes de error se muestran
- [ ] Datos coinciden con pantalla

#### Gráficos:
- [ ] Descarga PNG funciona
- [ ] Descarga JPEG funciona
- [ ] Descarga PDF funciona
- [ ] Calidad de imagen es buena
- [ ] Mensajes de éxito/error funcionan

---

## 5. Pruebas de Manejo de Errores

### Caso de Prueba 5.1: Error de red
**Simulación:**
- Desconectar la conexión a internet
- Intentar descargar un archivo

**Resultado Esperado:**
- Se muestra mensaje de error apropiado
- La aplicación no se bloquea

---

### Caso de Prueba 5.2: Error del servidor
**Simulación:**
- Simular un error en el servidor (modificar código temporalmente)

**Resultado Esperado:**
- Se muestra: "No fue posible generar el archivo, por favor intente nuevamente"
- No se descarga archivo corrupto

---

### Caso de Prueba 5.3: Datos vacíos
**Pasos:**
1. Acceder con un filtro que no tenga datos
2. Intentar descargar tabla y gráfico

**Resultado Esperado:**
- Tabla: Se descarga con mensaje "No hay datos disponibles"
- Gráfico: Se muestra error "No hay datos para generar el gráfico"

---

## 6. Checklist de Validación Final

### Funcionalidades Básicas:
- [ ] Descarga Excel funciona correctamente
- [ ] Descarga CSV funciona correctamente
- [ ] Descarga PNG funciona correctamente
- [ ] Descarga JPEG funciona correctamente
- [ ] Descarga PDF funciona correctamente

### Validación de Datos:
- [ ] Datos en Excel coinciden con pantalla
- [ ] Datos en CSV coinciden con pantalla
- [ ] Gráfico descargado coincide con pantalla

### Manejo de Errores:
- [ ] Errores se muestran correctamente
- [ ] Mensajes de éxito se muestran correctamente
- [ ] Datos vacíos se manejan apropiadamente

### Compatibilidad:
- [ ] Funciona en Chrome
- [ ] Funciona en Firefox
- [ ] Funciona en Edge
- [ ] Funciona en Safari (si aplica)

