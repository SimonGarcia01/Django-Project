# Troubleshooting - Pruebas de Selenium

## Problema: TimeoutException al encontrar el botón de login

### Síntomas
```
selenium.common.exceptions.TimeoutException: Message:
  File ".../bienestar360_login_page.py", line 42, in click_login_button
    self.click(self.LOGIN_BUTTON)
```

### Solución

1. **Verifica que el servidor Django esté corriendo:**
   ```bash
   # En una terminal, ejecuta:
   docker-compose up
   # O
   python manage.py runserver
   ```

2. **Verifica que la página de login sea accesible:**
   - Abre tu navegador y ve a: `http://localhost:8000/login/`
   - Deberías ver la página de login con el formulario
   - Si ves un error de conexión, el servidor no está corriendo

3. **Ejecuta las pruebas con salida detallada:**
   ```bash
   python -m behave selenium_tests/features/bienestar360_tournament_creation.feature --no-capture
   ```

4. **Revisa los logs:**
   - Los logs ahora incluyen mensajes de debug que te dirán exactamente qué está pasando
   - Busca mensajes como:
     - `✅ Login card found` - La página se cargó correctamente
     - `❌ Username field not found` - La página no se cargó correctamente
     - `Error: Could not find login button` - El botón no está presente

### Verificación rápida

1. Abre una nueva terminal
2. Ejecuta:
   ```bash
   curl http://localhost:8000/login/
   ```
   - Si obtienes HTML, el servidor está corriendo
   - Si obtienes un error de conexión, el servidor NO está corriendo

### Si el servidor está corriendo pero las pruebas aún fallan

1. **Verifica que ChromeDriver esté instalado y en el PATH:**
   ```bash
   chromedriver --version
   ```

2. **Verifica que no haya otros servicios usando el puerto 8000:**
   ```bash
   # En Windows (PowerShell):
   netstat -ano | findstr :8000
   ```

3. **Ejecuta las pruebas con más tiempo de espera:**
   - Las pruebas ahora tienen timeouts más largos (15 segundos)
   - Si tu servidor es lento, puede que necesites aumentar los timeouts

### Verificación del código

Si el servidor está corriendo y las pruebas aún fallan, verifica:

1. **Que el selector del botón sea correcto:**
   - El botón debería tener la clase `btn-submit`
   - El botón debería tener `type="submit"`
   - El texto del botón debería ser "Iniciar sesión"

2. **Que la página se esté cargando correctamente:**
   - Revisa los logs de la prueba para ver qué elementos se están encontrando
   - Los logs mostrarán qué botones están disponibles en la página

### Próximos pasos

Si después de verificar todo lo anterior las pruebas aún fallan:

1. Comparte los logs completos de la ejecución
2. Verifica que la estructura HTML de la página de login sea la esperada
3. Revisa si hay algún JavaScript que esté modificando el DOM después de la carga

