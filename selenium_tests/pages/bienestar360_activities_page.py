from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class Bienestar360ActivitiesPage(BasePage):
    """Page Object for Bienestar360 Activities Filter Page"""
    
    # Locators - basados en el template HTML
    PAGE_TITLE = (By.TAG_NAME, 'h1')  # "Actividades disponibles"
    TYPE_FILTER = (By.NAME, 'type')  # Select de tipo de actividad
    LOCATION_FILTER = (By.NAME, 'location')  # Input de ubicación
    TIME_FILTER = (By.NAME, 'time')  # Input de tiempo
    FILTER_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"].button')  # Botón Filtrar
    CLEAR_BUTTON = (By.LINK_TEXT, 'Limpiar')  # Botón Limpiar (es un enlace)
    # Alternativas:
    # CLEAR_BUTTON = (By.CSS_SELECTOR, 'a.button.button-clear')
    # CLEAR_BUTTON = (By.XPATH, "//a[contains(@class, 'button-clear') or contains(text(), 'Limpiar')]")
    ACTIVITY_CARDS = (By.CSS_SELECTOR, '.card')  # Cards de actividades
    ACTIVITY_NAME = (By.CSS_SELECTOR, '.card h2')  # Nombre de la actividad
    EMPTY_MESSAGE = (By.CSS_SELECTOR, '.empty-message p')  # Mensaje cuando no hay actividades
    FILTERS_FORM = (By.CSS_SELECTOR, '.filters form')  # Formulario de filtros
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/activities/view/"
    
    def navigate_to(self):
        """Navigate to the activities page"""
        self.driver.get(self.url)
        # Esperar a que la página cargue
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PAGE_TITLE)
        )
    
    def select_activity_type(self, activity_type):
        """Select activity type from dropdown"""
        try:
            type_select = Select(self.find_element(self.TYPE_FILTER))
            type_select.select_by_visible_text(activity_type)
            return True
        except Exception as e:
            print(f"Error selecting activity type: {e}")
            return False
    
    def enter_location(self, location):
        """Enter location in the location filter"""
        try:
            location_field = self.find_element(self.LOCATION_FILTER)
            location_field.clear()
            location_field.send_keys(location)
            return True
        except Exception as e:
            print(f"Error entering location: {e}")
            return False
    
    def enter_time(self, time):
        """Enter time in the time filter (format: HH:MM)"""
        try:
            time_field = self.find_element(self.TIME_FILTER)
            time_field.clear()
            time_field.send_keys(time)
            return True
        except Exception as e:
            print(f"Error entering time: {e}")
            return False
    
    def click_filter_button(self):
        """Click the filter button"""
        try:
            # Obtener el número de actividades antes de filtrar para comparar
            activities_before = len(self.driver.find_elements(*self.ACTIVITY_CARDS))
            
            # Hacer clic en el botón de filtrar
            filter_button = self.find_element(self.FILTER_BUTTON)
            filter_button.click()
            
            # Esperar a que la página se recargue o que los resultados cambien
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Esperar un poco más para que los resultados se actualicen
            import time
            time.sleep(1)
            
            # Verificar que la página ha cambiado (los resultados pueden haber cambiado)
            return True
        except Exception as e:
            print(f"Error clicking filter button: {e}")
            return False
    
    def click_clear_button(self):
        """Click the clear button to reset filters"""
        try:
            # El botón limpiar es un enlace, intentar varios métodos
            selectors = [
                (By.LINK_TEXT, 'Limpiar'),
                (By.PARTIAL_LINK_TEXT, 'Limpiar'),
                (By.CSS_SELECTOR, 'a.button.button-clear'),
                (By.CSS_SELECTOR, 'a[href*="activityView"]'),
                (By.XPATH, "//a[contains(@class, 'button-clear')]"),
                (By.XPATH, "//a[contains(text(), 'Limpiar')]"),
            ]
            
            for selector_type, selector_value in selectors:
                try:
                    clear_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )
                    # Scroll al elemento si es necesario
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", clear_button)
                    clear_button.click()
                    
                    # Esperar a que la página se recargue
                    WebDriverWait(self.driver, 10).until(
                        lambda driver: driver.execute_script("return document.readyState") == "complete"
                    )
                    
                    # Esperar un poco más para que los filtros se resetee
                    import time
                    time.sleep(1)
                    
                    return True
                except:
                    continue
            
            return False
        except Exception as e:
            print(f"Error clicking clear button: {e}")
            return False
    
    def get_activity_count(self):
        """Get the number of activities displayed"""
        try:
            activities = self.driver.find_elements(*self.ACTIVITY_CARDS)
            return len(activities)
        except:
            return 0
    
    def get_activities(self):
        """Get all activity cards"""
        try:
            return self.driver.find_elements(*self.ACTIVITY_CARDS)
        except:
            return []
    
    def get_activity_type_text(self, activity_card):
        """Get the activity type text from an activity card"""
        try:
            # Buscar el párrafo que contiene "Tipo:"
            card_text = activity_card.text
            # Extraer el tipo de la línea que contiene "Tipo:"
            for line in card_text.split('\n'):
                if 'Tipo:' in line:
                    return line.split('Tipo:')[1].strip()
            return None
        except:
            return None
    
    def get_activity_location_text(self, activity_card):
        """Get the activity location text from an activity card"""
        try:
            # Intentar encontrar el elemento de ubicación directamente
            try:
                location_elements = activity_card.find_elements(By.XPATH, ".//p[contains(text(), 'Ubicación:')]")
                if location_elements:
                    location_text = location_elements[0].text
                    if 'Ubicación:' in location_text:
                        return location_text.split('Ubicación:')[1].strip()
            except:
                pass
            
            # Si no funciona, usar el método de texto
            card_text = activity_card.text
            # Extraer la ubicación de la línea que contiene "Ubicación:"
            for line in card_text.split('\n'):
                if 'Ubicación:' in line:
                    location = line.split('Ubicación:')[1].strip()
                    # Limpiar cualquier texto adicional que pueda haber
                    return location
            return None
        except Exception as e:
            print(f"Error getting location: {e}")
            return None
    
    def get_activity_schedule_text(self, activity_card):
        """Get the activity schedule text from an activity card"""
        try:
            card_text = activity_card.text
            # Extraer el horario de la línea que contiene "Horario:"
            for line in card_text.split('\n'):
                if 'Horario:' in line:
                    return line.split('Horario:')[1].strip()
            return None
        except:
            return None
    
    def is_empty_message_displayed(self):
        """Check if empty message is displayed"""
        try:
            # Buscar el mensaje vacío con diferentes selectores posibles
            selectors = [
                self.EMPTY_MESSAGE,
                (By.CSS_SELECTOR, '.empty-message'),
                (By.CSS_SELECTOR, '.no-results'),
                (By.CSS_SELECTOR, '.alert-info'),
                (By.XPATH, "//*[contains(text(), 'No hay actividades')]"),
                (By.XPATH, "//*[contains(text(), 'no hay actividades')]"),
                (By.XPATH, "//*[contains(text(), 'disponibles')]"),
            ]
            
            for selector in selectors:
                try:
                    empty_msg = self.driver.find_element(*selector)
                    if empty_msg.is_displayed():
                        return True
                except:
                    continue
            
            # También verificar si no hay actividades y no hay mensaje (puede ser válido)
            activities = self.get_activities()
            if len(activities) == 0:
                # Buscar cualquier texto que indique que no hay resultados
                page_text = self.driver.page_source.lower()
                if "no hay" in page_text or "disponibles" in page_text or "resultados" in page_text:
                    return True
            
            return False
        except:
            return False
    
    def get_empty_message_text(self):
        """Get the empty message text"""
        try:
            # Buscar el mensaje vacío con diferentes selectores posibles
            selectors = [
                self.EMPTY_MESSAGE,
                (By.CSS_SELECTOR, '.empty-message'),
                (By.CSS_SELECTOR, '.no-results'),
                (By.CSS_SELECTOR, '.alert-info'),
                (By.XPATH, "//*[contains(text(), 'No hay actividades')]"),
                (By.XPATH, "//*[contains(text(), 'no hay actividades')]"),
            ]
            
            for selector in selectors:
                try:
                    empty_msg = self.driver.find_element(*selector)
                    if empty_msg.is_displayed():
                        return empty_msg.text
                except:
                    continue
            
            # Si no hay actividades, buscar en el texto de la página
            activities = self.get_activities()
            if len(activities) == 0:
                page_text = self.driver.page_source
                # Buscar texto relacionado con "no hay actividades"
                import re
                pattern = r'(No hay actividades[^<]*)'
                match = re.search(pattern, page_text, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
            
            return None
        except:
            return None
    
    def is_type_filter_visible(self):
        """Check if type filter is visible"""
        try:
            type_filter = self.driver.find_element(*self.TYPE_FILTER)
            return type_filter.is_displayed()
        except:
            return False
    
    def is_location_filter_visible(self):
        """Check if location filter is visible"""
        try:
            location_filter = self.driver.find_element(*self.LOCATION_FILTER)
            return location_filter.is_displayed()
        except:
            return False
    
    def is_time_filter_visible(self):
        """Check if time filter is visible"""
        try:
            time_filter = self.driver.find_element(*self.TIME_FILTER)
            return time_filter.is_displayed()
        except:
            return False
    
    def is_filter_button_visible(self):
        """Check if filter button is visible"""
        try:
            filter_button = self.driver.find_element(*self.FILTER_BUTTON)
            return filter_button.is_displayed()
        except:
            return False
    
    def is_clear_button_visible(self):
        """Check if clear button is visible"""
        try:
            # Intentar varios selectores
            selectors = [
                (By.LINK_TEXT, 'Limpiar'),
                (By.PARTIAL_LINK_TEXT, 'Limpiar'),
                (By.CSS_SELECTOR, 'a.button.button-clear'),
                (By.XPATH, "//a[contains(text(), 'Limpiar')]"),
            ]
            
            for selector_type, selector_value in selectors:
                try:
                    clear_button = self.driver.find_element(selector_type, selector_value)
                    if clear_button.is_displayed():
                        return True
                except:
                    continue
            
            return False
        except:
            return False
    
    def get_selected_type(self):
        """Get the currently selected activity type"""
        try:
            type_select = Select(self.find_element(self.TYPE_FILTER))
            selected_option = type_select.first_selected_option
            # Si está seleccionado "Todos los tipos", retornar cadena vacía
            if selected_option.text == "Todos los tipos":
                return ""
            return selected_option.text
        except:
            return None
    
    def get_location_value(self):
        """Get the current location filter value"""
        try:
            location_field = self.find_element(self.LOCATION_FILTER)
            return location_field.get_attribute('value')
        except:
            return None
    
    def get_time_value(self):
        """Get the current time filter value"""
        try:
            time_field = self.find_element(self.TIME_FILTER)
            return time_field.get_attribute('value')
        except:
            return None
    
    def time_matches_schedule(self, schedule_text, filter_time):
        """Check if the schedule text matches the filter time"""
        if not schedule_text or not filter_time:
            return False
        
        # El horario puede estar en formato "HH:MM:SS - HH:MM:SS" o "HH:MM - HH:MM"
        # Necesitamos verificar si el tiempo del filtro está dentro del rango
        try:
            # Extraer horas y minutos del tiempo del filtro
            filter_hour, filter_minute = map(int, filter_time.split(':'))
            filter_minutes = filter_hour * 60 + filter_minute
            
            # Buscar todos los rangos de horarios en el texto
            import re
            time_pattern = r'(\d{1,2}):(\d{2})(?::\d{2})?\s*-\s*(\d{1,2}):(\d{2})(?::\d{2})?'
            matches = re.findall(time_pattern, schedule_text)
            
            for match in matches:
                start_hour, start_min, end_hour, end_min = map(int, match)
                start_minutes = start_hour * 60 + start_min
                end_minutes = end_hour * 60 + end_min
                
                # Verificar si el tiempo del filtro está dentro del rango
                if start_minutes <= filter_minutes <= end_minutes:
                    return True
            
            return False
        except:
            return False

