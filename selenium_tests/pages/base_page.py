from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    """
    Clase base para todas las Page Objects.
    Proporciona métodos comunes para interactuar con elementos de la página.
    """
    
    def __init__(self, driver):
        """
        Inicializa la página base con el driver.
        
        Args:
            driver: Instancia del WebDriver (Chrome, Firefox, etc.)
        """
        self.driver = driver
        self.timeout = 20

    def find_element(self, locator):
        """
        Encuentra un elemento en la página esperando a que esté presente.
        
        Args:
            locator: Tupla (By, value) que identifica el elemento
            
        Returns:
            WebElement: El elemento encontrado
        """
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def find_elements(self, locator):
        """
        Encuentra múltiples elementos en la página.
        
        Args:
            locator: Tupla (By, value) que identifica los elementos
            
        Returns:
            List[WebElement]: Lista de elementos encontrados
        """
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_all_elements_located(locator)
        )

    def click(self, locator):
        """
        Hace clic en un elemento.
        
        Args:
            locator: Tupla (By, value) que identifica el elemento
        """
        element = self.find_element(locator)
        element.click()
        # Esperar un momento y cerrar cualquier diálogo de contraseñas
        import time
        time.sleep(0.3)
        self.close_password_dialogs()

    def enter_text(self, locator, text):
        """
        Escribe texto en un campo de entrada.
        
        Args:
            locator: Tupla (By, value) que identifica el elemento
            text: Texto a escribir
        """
        element = self.find_element(locator)
        element.clear()
        if text:
            element.send_keys(text)
            # Si es un campo de contraseña, cerrar diálogos después de escribir
            # (los pop-ups de contraseñas aparecen después de ingresar contraseñas)
            if 'password' in str(locator).lower():
                import time
                time.sleep(0.5)  # Esperar a que aparezca el diálogo si va a aparecer
                self.close_password_dialogs()

    def get_text(self, locator):
        """
        Obtiene el texto de un elemento.
        
        Args:
            locator: Tupla (By, value) que identifica el elemento
            
        Returns:
            str: Texto del elemento
        """
        return self.find_element(locator).text

    def is_element_present(self, locator):
        """
        Verifica si un elemento está presente en la página.
        
        Args:
            locator: Tupla (By, value) que identifica el elemento
            
        Returns:
            bool: True si el elemento está presente, False en caso contrario
        """
        try:
            self.find_element(locator)
            return True
        except:
            return False

    def is_element_displayed(self, locator):
        """
        Verifica si un elemento está visible en la página.
        
        Args:
            locator: Tupla (By, value) que identifica el elemento
            
        Returns:
            bool: True si el elemento está visible, False en caso contrario
        """
        try:
            element = self.find_element(locator)
            return element.is_displayed()
        except:
            return False

    def wait_for_element(self, locator, timeout=None):
        """
        Espera a que un elemento esté presente.
        
        Args:
            locator: Tupla (By, value) que identifica el elemento
            timeout: Tiempo de espera en segundos (opcional)
            
        Returns:
            WebElement: El elemento encontrado
        """
        if timeout is None:
            timeout = self.timeout
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
    
    def close_password_dialogs(self):
        """
        Cierra cualquier diálogo de contraseñas de Chrome que pueda aparecer.
        Usa múltiples métodos para intentar cerrar diálogos nativos del navegador,
        incluyendo presionar teclas a nivel del sistema en Windows.
        """
        try:
            import time
            import platform
            from selenium.webdriver.common.keys import Keys
            from selenium.webdriver.common.action_chains import ActionChains
            
            # Esperar un momento para que aparezca el diálogo si va a aparecer
            time.sleep(0.5)
            
            # Método 1: Presionar ESC múltiples veces usando ActionChains
            try:
                actions = ActionChains(self.driver)
                for _ in range(5):  # Aumentado a 5 intentos
                    actions.send_keys(Keys.ESCAPE).perform()
                    time.sleep(0.15)
            except:
                pass
            
            # Método 2: Usar CDP para simular tecla ESC y ENTER (por si el diálogo necesita ENTER para aceptar)
            try:
                # Presionar ESC
                for _ in range(3):
                    self.driver.execute_cdp_cmd('Input.dispatchKeyEvent', {
                        'type': 'keyDown',
                        'windowsVirtualKeyCode': 27,  # ESC
                        'code': 'Escape',
                        'key': 'Escape'
                    })
                    time.sleep(0.1)
                    self.driver.execute_cdp_cmd('Input.dispatchKeyEvent', {
                        'type': 'keyUp',
                        'windowsVirtualKeyCode': 27,
                        'code': 'Escape',
                        'key': 'Escape'
                    })
                    time.sleep(0.1)
                
                # También intentar ENTER por si el diálogo tiene un botón "Aceptar" seleccionado
                self.driver.execute_cdp_cmd('Input.dispatchKeyEvent', {
                    'type': 'keyDown',
                    'windowsVirtualKeyCode': 13,  # ENTER
                    'code': 'Enter',
                    'key': 'Enter'
                })
                time.sleep(0.1)
                self.driver.execute_cdp_cmd('Input.dispatchKeyEvent', {
                    'type': 'keyUp',
                    'windowsVirtualKeyCode': 13,
                    'code': 'Enter',
                    'key': 'Enter'
                })
            except:
                pass
            
            # Método 3: En Windows, usar pyautogui para presionar teclas a nivel del sistema
            # Este es el método más efectivo para cerrar diálogos nativos del sistema
            if platform.system() == "Windows":
                try:
                    import pyautogui
                    # Configurar pyautogui para ser más rápido (reducir delay entre acciones)
                    pyautogui.PAUSE = 0.1
                    pyautogui.FAILSAFE = False  # Deshabilitar failsafe para testing
                    
                    # Estrategia: Presionar ENTER primero (el diálogo puede tener "Aceptar" seleccionado)
                    # Luego presionar ESC como respaldo
                    pyautogui.press('enter')
                    time.sleep(0.3)
                    pyautogui.press('enter')  # Presionar dos veces por si acaso
                    time.sleep(0.2)
                    pyautogui.press('escape')  # Presionar ESC como respaldo
                    time.sleep(0.2)
                    pyautogui.press('escape')
                    time.sleep(0.2)
                    pyautogui.press('enter')  # Último intento con ENTER
                except ImportError:
                    # Si pyautogui no está disponible, intentar con keyboard
                    try:
                        import keyboard
                        keyboard.press_and_release('enter')
                        time.sleep(0.3)
                        keyboard.press_and_release('enter')
                        time.sleep(0.2)
                        keyboard.press_and_release('escape')
                        time.sleep(0.2)
                        keyboard.press_and_release('escape')
                        time.sleep(0.2)
                        keyboard.press_and_release('enter')
                    except (ImportError, Exception):
                        pass
                except Exception as e:
                    # Si hay error, continuar sin pyautogui
                    pass
            
            # Método 4: Buscar y hacer clic en botones mediante JavaScript
            try:
                self.driver.execute_script("""
                    // Buscar todos los botones visibles en la página
                    var buttons = document.querySelectorAll('button, [role="button"], input[type="button"], a[role="button"]');
                    for (var i = 0; i < buttons.length; i++) {
                        var btn = buttons[i];
                        // Verificar que el botón esté visible
                        var rect = btn.getBoundingClientRect();
                        if (rect.width > 0 && rect.height > 0) {
                            var text = (btn.textContent || btn.innerText || btn.value || '').toLowerCase().trim();
                            var ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
                            
                            // Buscar botones relacionados con aceptar/cerrar
                            if (text.includes('aceptar') || text.includes('accept') || 
                                text.includes('cerrar') || text.includes('close') ||
                                text.includes('ok') || text.includes('continuar') ||
                                text.includes('sí') || text.includes('yes') ||
                                ariaLabel.includes('cerrar') || ariaLabel.includes('close') ||
                                ariaLabel.includes('aceptar') || ariaLabel.includes('accept')) {
                                try {
                                    btn.focus();
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
                
            # Esperar un poco más para que el diálogo se cierre
            time.sleep(0.3)
        except:
            # Si hay algún error, simplemente continuar
            pass

