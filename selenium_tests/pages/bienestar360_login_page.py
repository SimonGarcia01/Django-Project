from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time


class Bienestar360LoginPage(BasePage):
    """Page Object for Bienestar360 Login Page"""
    
    # Locators - usando selectores inferidos de Django
    USERNAME_FIELD = (By.ID, 'id_username')  # Django genera id_username
    PASSWORD_FIELD = (By.ID, 'id_password')  # Django genera id_password
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button.btn-submit, button[type="submit"], button:contains("Iniciar sesión")')  # Botón con clase btn-submit
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.form-errors p')  # Mensajes de error
    REGISTRATION_LINK = (By.LINK_TEXT, 'Regístrate aquí')  # Enlace de registro
    PAGE_TITLE = (By.CSS_SELECTOR, '.card-title, h1.card-title')  # Título "Bienvenido"
    LOGIN_CARD = (By.CSS_SELECTOR, '.login-card')  # Card contenedor
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/login/"
    
    def navigate_to(self):
        """Navigate to the login page and wait for it to load"""
        print(f"Navigating to: {self.url}")
        try:
            self.driver.get(self.url)
        except Exception as e:
            print(f"Error navigating to login page: {e}")
            print("Make sure Django server is running on http://localhost:8000")
            raise
        
        # Verificar que la página se cargó (no es un error de conexión)
        current_url = self.driver.current_url
        print(f"Current URL after navigation: {current_url}")
        
        if "localhost:8000" not in current_url or "error" in current_url.lower():
            print(f"Warning: Page may not have loaded correctly. URL: {current_url}")
        
        # Esperar a que la página se cargue completamente
        try:
            # Esperar a que el login card esté presente
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.LOGIN_CARD)
            )
            print("✅ Login card found")
            time.sleep(0.5)
        except Exception as e:
            print(f"⚠️ Warning: Login card not found immediately: {e}")
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body'))
                )
                print("✅ Body element found")
                time.sleep(1)
                
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located(self.USERNAME_FIELD)
                    )
                    print("✅ Username field found")
                except:
                    print("❌ Username field not found - page may not be loaded correctly")
                    # Imprimir información de debug
                    try:
                        page_title = self.driver.title
                        print(f"Page title: {page_title}")
                    except:
                        pass
            except Exception as e2:
                print(f"❌ Error: Could not load login page. Make sure Django server is running.")
                print(f"Error details: {e2}")
                raise
    
    def enter_username(self, username):
        """Enter username in the username field"""
        try:
            # Esperar a que el campo esté presente
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.USERNAME_FIELD)
            )
            username_field.clear()
            if username:  # Solo enviar texto si no está vacío
                username_field.send_keys(username)
        except Exception as e:
            print(f"Error entering username: {e}")
            # Intentar obtener información de debug
            try:
                page_source_preview = self.driver.page_source[:500]
                print(f"Page source preview: {page_source_preview}")
            except:
                pass
            raise
    
    def enter_password(self, password):
        """Enter password in the password field"""
        try:
            # Esperar a que el campo esté presente
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.PASSWORD_FIELD)
            )
            password_field.clear()
            if password:  # Solo enviar texto si no está vacío
                password_field.send_keys(password)
        except Exception as e:
            print(f"Error entering password: {e}")
            raise
    
    def click_login_button(self):
        """Click the login button with multiple selector attempts"""
        try:
            # Intentar con el selector principal
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn-submit'))
            )
            button.click()
        except:
            try:
                # Intentar con selector alternativo
                button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
                )
                button.click()
            except:
                try:
                    # Intentar con XPath
                    button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Iniciar sesión') or contains(text(), 'Iniciar')]"))
                    )
                    button.click()
                except Exception as e:
                    print(f"Error: Could not find login button. Available buttons on page:")
                    # Debug: imprimir todos los botones disponibles
                    try:
                        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
                        for i, btn in enumerate(buttons):
                            print(f"  Button {i+1}: text='{btn.text}', type='{btn.get_attribute('type')}', class='{btn.get_attribute('class')}'")
                    except:
                        pass
                    raise Exception(f"Login button not found: {e}")
    
    def login(self, username, password):
        """Complete login process"""
        self.enter_username(username)
        self.enter_password(password)
        
        # Cerrar cualquier diálogo de contraseñas antes de hacer clic en login
        import time
        time.sleep(0.5)
        self.close_password_dialogs()
        time.sleep(0.2)
        
        self.click_login_button()
        
        # Cerrar cualquier diálogo de contraseñas después del login
        time.sleep(0.8)  # Esperar más tiempo después del login
        self.close_password_dialogs()
        time.sleep(0.2)
        self.close_password_dialogs()  # Intentar dos veces por si acaso
    
    def get_error_message(self):
        """Get error message text if present"""
        try:
            error_element = self.find_element(self.ERROR_MESSAGE)
            return error_element.text
        except:
            return None
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        try:
            error_element = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_element.is_displayed()
        except:
            return False
    
    def get_page_title(self):
        """Get the page title text"""
        try:
            title_element = self.find_element(self.PAGE_TITLE)
            return title_element.text
        except:
            return None

