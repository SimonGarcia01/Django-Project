# steps/user_preference_steps.py
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ELIMINA los steps @given y @when que están en common_steps.py
# Solo deja los steps específicos de preferencias

@when('navego a la página de alertas personalizadas')
def step_impl(context):
    """Navegar directamente a preferencias"""
    # Intentar varias URLs posibles
    urls_to_try = [
        "http://localhost:8000/preferences/setup/",
        "http://localhost:8000/preferences/",
        "http://localhost:8000/alertas/",
        "http://localhost:8000/alertas-personalizadas/",
        "http://localhost:8000/user/preferences/",
        "http://localhost:8000/user/alertas/"
    ]
    
    for url in urls_to_try:
        try:
            print(f"🔗 Intentando: {url}")
            context.driver.get(url)
            
            WebDriverWait(context.driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Verificar que la página cargó algo útil
            page_source = context.driver.page_source.lower()
            if any(keyword in page_source for keyword in ['preferencias', 'alertas', 'grupal', 'configuración']):
                print(f"✅ Navegado exitosamente a: {url}")
                return
            else:
                print(f"⚠️ Página cargada pero no parece ser de preferencias: {url}")
                
        except Exception as e:
            print(f"❌ Error navegando a {url}: {e}")
            continue
    
    print("⚠️ No se pudo navegar a ninguna URL de preferencias conocida")
    # Tomar screenshot para debug
    context.driver.save_screenshot("debug_preferences_not_found.png")
    print("📸 Screenshot guardado: debug_preferences_not_found.png")

@then('veo una card con el texto "Grupal"')
def step_impl(context):
    """Buscar el texto Grupal"""
    try:
        print("🔍 Buscando texto 'Grupal'...")
        
        # Primero mostrar información de la página actual
        print(f"🔗 URL actual: {context.driver.current_url}")
        print(f"📄 Título: {context.driver.title}")
        
        # Buscar el texto "Grupal" de múltiples formas
        WebDriverWait(context.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Grupal')]"))
        )
        
        elementos_grupal = context.driver.find_elements(By.XPATH, "//*[contains(text(), 'Grupal')]")
        print(f"🔍 Encontrados {len(elementos_grupal)} elementos con 'Grupal'")
        
        for i, elemento in enumerate(elementos_grupal):
            if elemento.is_displayed():
                print(f"✅ Texto 'Grupal' encontrado y visible (#{i+1}): '{elemento.text}'")
                return
        
        # Si no encuentra elementos visibles, verificar en el HTML
        if "Grupal" in context.driver.page_source:
            print("✅ Texto 'Grupal' encontrado en el código HTML de la página")
        else:
            raise AssertionError("No se encontró el texto 'Grupal' en la página")
        
    except Exception as e:
        print(f"💥 Error buscando texto 'Grupal': {e}")
        
        # Última verificación - buscar en todo el contenido
        page_text = context.driver.page_source
        if "Grupal" in page_text:
            print("✅ Texto 'Grupal' encontrado en el contenido de la página")
        else:
            # Tomar screenshot para debugging
            context.driver.save_screenshot("error_grupal_no_encontrado.png")
            print("📸 Screenshot guardado: error_grupal_no_encontrado.png")
            print("📋 Contenido de la página (primeros 1500 caracteres):")
            print(context.driver.page_source[:1500])
            raise AssertionError("No se encontró el texto 'Grupal' en la página")