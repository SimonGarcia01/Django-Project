from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import tempfile
import platform
import time


def before_all(context):
    """
    Esta función se ejecuta una vez antes de todos los escenarios.
    Puede usarse para configuraciones globales.
    """
    pass


def before_scenario(context, scenario):
    """
    Esta función se ejecuta antes de cada escenario de prueba.
    Inicializa el WebDriver con configuración de Chrome para evitar problemas
    con el administrador de contraseñas y otros servicios.
    """
    # Configurar opciones de Chrome
    chrome_options = Options()
    
    # Deshabilitar completamente el administrador de contraseñas y servicios de credenciales
    # Esto evita problemas con contraseñas inseguras durante las pruebas
    # IMPORTANTE: Estas preferencias son clave para evitar el pop-up "Cambia tu contraseña"
    prefs = {
        # ===== ADMINISTRADOR DE CONTRASEÑAS =====
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "password_manager_enabled": False,
        "profile.password_manager_enabled.managed": False,
        "credentials_enable_autosignin": False,
        
        # ===== DETECCIÓN DE CONTRASEÑAS COMPROMETIDAS (CLAVE PARA EVITAR EL POP-UP) =====
        "profile.default_content_setting_values.password_leak_detection": 2,  # 2 = bloqueado completamente
        
        # ===== NAVEGACIÓN SEGURA Y SAFE BROWSING =====
        "safe_browsing.enabled": False,
        "safebrowsing.enabled": False,
        "safebrowsing.malware.enabled": False,
        "safebrowsing_for_trusted_sources_enabled": False,
        
        # ===== AUTOFILL Y AUTocompletado =====
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
        "profile.default_content_setting_values.automatic_downloads": 1,
        
        # ===== NOTIFICACIONES =====
        "profile.default_content_setting_values.notifications": 2,  # 2 = bloqueado
        
        # ===== SINCRONIZACIÓN Y CUENTAS DE GOOGLE =====
        "sync.disabled": True,
        "signin.allowed": False,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # IMPORTANTE: Deshabilitar explícitamente la detección de contraseñas comprometidas
    # Esto es clave para evitar el pop-up "Cambia tu contraseña"
    chrome_options.add_experimental_option("excludeSwitches", [
        "enable-automation",
        "enable-logging",
        "enable-blink-features=PasswordManager",  # Deshabilitar PasswordManager
    ])
    
    # Deshabilitar la detección de automatización
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Otras opciones útiles para testing
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-infobars")  # Deshabilitar barra de información
    chrome_options.add_argument("--disable-notifications")  # Deshabilitar notificaciones
    chrome_options.add_argument("--disable-popup-blocking")  # Deshabilitar bloqueo de pop-ups
    chrome_options.add_argument("--disable-password-manager")  # Deshabilitar administrador de contraseñas
    chrome_options.add_argument("--disable-save-password-bubble")  # Deshabilitar burbuja de guardar contraseña
    
    # Deshabilitar todas las características relacionadas con contraseñas y seguridad
    # PasswordLeakDetection es clave para evitar el pop-up de contraseñas comprometidas
    chrome_options.add_argument("--disable-features=PasswordManagerOnboarding,PasswordCheck,PasswordImport,PasswordLeakDetection,AutofillServerCommunication")
    chrome_options.add_argument("--disable-component-extensions-with-background-pages")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-sync")  # Deshabilitar sincronización de Google
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-web-security")  # Deshabilitar seguridad web (solo para testing)
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-site-isolation-trials")
    
    # Deshabilitar completamente las APIs de contraseñas de Chrome
    chrome_options.add_argument("--disable-features=RendererCodeIntegrity")
    chrome_options.add_argument("--disable-ipc-flooding-protection")
    
    # Usar un perfil temporal completamente limpio para evitar conflictos
    # Crear directorio temporal según el sistema operativo
    import uuid
    if platform.system() == "Windows":
        # En Windows, usar un directorio temporal único para cada ejecución
        temp_profile_dir = os.path.join(tempfile.gettempdir(), f"chrome_test_profile_{uuid.uuid4().hex[:8]}")
    else:
        temp_profile_dir = f"/tmp/chrome_test_profile_{uuid.uuid4().hex[:8]}"
    
    # Crear el directorio si no existe
    os.makedirs(temp_profile_dir, exist_ok=True)
    chrome_options.add_argument(f"--user-data-dir={temp_profile_dir}")
    
    # Forzar que Chrome use un perfil completamente nuevo sin conexión a Google
    chrome_options.add_argument("--disable-sync")  # Ya está, pero lo dejamos por si acaso
    chrome_options.add_argument("--disable-background-networking")  # Ya está
    chrome_options.add_argument("--disable-default-apps")  # Ya está
    
    # Función auxiliar para crear driver con opciones
    def create_driver_with_options(options):
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        
        # Ejecutar script para evitar detección de automatización
        try:
            driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    // Evitar detección de automatización
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                '''
            })
        except:
            # Si CDP no está disponible, continuar sin el script
            pass
        
        # Configurar timeouts por defecto
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        
        return driver
    
    # Función para cerrar pop-ups de contraseñas usando CDP y teclado
    def close_password_dialogs(driver):
        """Intenta cerrar diálogos de contraseñas de Chrome usando múltiples métodos"""
        try:
            # Método 1: Presionar ESC múltiples veces para cerrar cualquier diálogo nativo
            try:
                actions = ActionChains(driver)
                # Presionar ESC varias veces para asegurarse de cerrar el diálogo
                for _ in range(3):
                    actions.send_keys(Keys.ESCAPE).perform()
                    time.sleep(0.1)
            except:
                pass
            
            # Método 2: Usar CDP para simular tecla ESC a nivel del navegador
            try:
                driver.execute_cdp_cmd('Input.dispatchKeyEvent', {
                    'type': 'keyDown',
                    'windowsVirtualKeyCode': 27,  # ESC key code
                    'code': 'Escape',
                    'key': 'Escape'
                })
                time.sleep(0.1)
                driver.execute_cdp_cmd('Input.dispatchKeyEvent', {
                    'type': 'keyUp',
                    'windowsVirtualKeyCode': 27,
                    'code': 'Escape',
                    'key': 'Escape'
                })
            except:
                pass
            
            # Método 3: Buscar y hacer clic en botones de "Aceptar" mediante JavaScript
            try:
                driver.execute_script("""
                    // Buscar todos los botones visibles
                    var buttons = document.querySelectorAll('button, [role="button"], input[type="button"]');
                    for (var i = 0; i < buttons.length; i++) {
                        var btn = buttons[i];
                        if (btn.offsetParent !== null) {  // Solo botones visibles
                            var text = (btn.textContent || btn.innerText || btn.value || '').toLowerCase();
                            var ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
                            
                            if (text.includes('aceptar') || text.includes('accept') || 
                                text.includes('cerrar') || text.includes('close') ||
                                text.includes('ok') || text.includes('continuar') ||
                                ariaLabel.includes('cerrar') || ariaLabel.includes('close') ||
                                ariaLabel.includes('aceptar') || ariaLabel.includes('accept')) {
                                try {
                                    btn.click();
                                    break;
                                } catch(e) {
                                    // Continuar si no se puede hacer clic
                                }
                            }
                        }
                    }
                """)
            except:
                pass
                
        except Exception as e:
            # Si hay algún error, simplemente continuar
            print(f"Warning: No se pudo cerrar diálogo de contraseñas: {e}")
            pass
    
    # Inicializar el driver con las opciones configuradas
    try:
        context.driver = create_driver_with_options(chrome_options)
        # Agregar función para cerrar pop-ups al contexto
        context.close_password_dialogs = lambda: close_password_dialogs(context.driver)
        
        # Configurar un listener para cerrar pop-ups después de navegar a páginas
        def navigate_with_popup_handling(url):
            """Navegar a una URL y cerrar pop-ups después"""
            context.driver.get(url)
            time.sleep(0.5)
            close_password_dialogs(context.driver)
        
        # No sobrescribir driver.get directamente, pero tener la función disponible
        context.navigate_with_popup_handling = navigate_with_popup_handling
    except Exception as e:
        print(f"Error al inicializar Chrome con perfil temporal: {e}")
        print("Intentando sin perfil temporal...")
        # Si falla con el perfil temporal, crear nuevas opciones sin user-data-dir
        chrome_options_no_profile = Options()
        chrome_options_no_profile.add_experimental_option("prefs", prefs)
        chrome_options_no_profile.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options_no_profile.add_experimental_option('useAutomationExtension', False)
        
        # Agregar todos los argumentos excepto user-data-dir
        for arg in [
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-infobars",
            "--disable-notifications",
            "--disable-popup-blocking",
            "--disable-password-manager",
            "--disable-save-password-bubble",
            "--disable-features=PasswordManagerOnboarding,PasswordCheck,PasswordImport,PasswordLeakDetection,AutofillServerCommunication",
            "--disable-component-extensions-with-background-pages",
            "--disable-background-networking",
            "--disable-sync",
            "--disable-translate",
            "--disable-default-apps",
            "--disable-web-security",
            "--allow-running-insecure-content",
            "--disable-site-isolation-trials",
            "--disable-features=RendererCodeIntegrity",
            "--disable-ipc-flooding-protection",
        ]:
            chrome_options_no_profile.add_argument(arg)
        
        try:
            context.driver = create_driver_with_options(chrome_options_no_profile)
            # Agregar función para cerrar pop-ups al contexto
            context.close_password_dialogs = lambda: close_password_dialogs(context.driver)
        except Exception as e2:
            print(f"Error crítico al inicializar Chrome: {e2}")
            raise


def after_scenario(context, scenario):
    """
    Esta función se ejecuta después de cada escenario de prueba.
    Cierra el navegador para limpiar después de cada prueba.
    """
    if hasattr(context, 'driver'):
        try:
            context.driver.quit()
        except Exception as e:
            print(f"Error al cerrar el driver: {e}")


def after_all(context):
    """
    Esta función se ejecuta una vez después de todos los escenarios.
    Puede usarse para limpieza global.
    """
    pass

