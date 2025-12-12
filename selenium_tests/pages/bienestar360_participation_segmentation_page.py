from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time


class Bienestar360ParticipationSegmentationPage(BasePage):
    """Page Object for Bienestar360 Participation Segmentation (CADI view)"""
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, 'h2')  # Título de la página
    FILTERS_FORM = (By.CSS_SELECTOR, '.filters-form')
    RESULTS_TABLE = (By.CSS_SELECTOR, 'table.table')
    TABLE_ROWS = (By.CSS_SELECTOR, 'table.table tbody tr')
    DETAILS_SUMMARY = (By.CSS_SELECTOR, 'details summary')  # Para expandir lista de estudiantes
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/activities/cadi/participation/"
    
    def navigate_to(self):
        """Navigate to the participation segmentation page"""
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.FILTERS_FORM)
        )
        time.sleep(0.5)
    
    def get_table_rows(self):
        """Get all rows from the results table"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.RESULTS_TABLE)
            )
            rows = self.driver.find_elements(*self.TABLE_ROWS)
            return rows
        except:
            return []
    
    def expand_students_list(self, row_index=0):
        """Expand the students list (details) for a specific row"""
        try:
            rows = self.get_table_rows()
            if row_index >= len(rows):
                return False
            
            row = rows[row_index]
            # Buscar el elemento details dentro de la fila
            try:
                details = row.find_element(By.CSS_SELECTOR, 'details')
                summary = details.find_element(By.CSS_SELECTOR, 'summary')
                
                # Si no está abierto, hacer clic para abrirlo
                if not details.get_attribute('open'):
                    summary.click()
                    time.sleep(0.5)
                
                return True
            except:
                return False
        except Exception as e:
            print(f"Error expanding students list: {e}")
            return False
    
    def get_participated_students_info(self, row_index=0):
        """Get list of participated students with their information (ID, Name) from a specific row"""
        try:
            if not self.expand_students_list(row_index):
                return []
            
            rows = self.get_table_rows()
            if row_index >= len(rows):
                return []
            
            row = rows[row_index]
            students = []
            
            # Buscar la sección de participantes/asistentes
            try:
                # Buscar todos los elementos li dentro de details que contengan información de estudiantes
                participated_section = row.find_element(By.XPATH, 
                    ".//h4[contains(text(), 'Asistieron') or contains(text(), 'Participantes')]/following-sibling::ul")
                student_items = participated_section.find_elements(By.TAG_NAME, 'li')
                
                for item in student_items:
                    student_text = item.text
                    # Extraer ID y nombre del estudiante
                    # Formato esperado: "ID: 123456789 | Nombre: Juan Pérez"
                    if 'ID:' in student_text:
                        parts = student_text.split('ID:')
                        if len(parts) > 1:
                            id_part = parts[1].split('|')[0].strip() if '|' in parts[1] else parts[1].strip()
                            name_part = parts[1].split('|')[1] if '|' in parts[1] else ''
                            if 'Nombre:' in name_part:
                                name_part = name_part.replace('Nombre:', '').strip()
                            
                            students.append({
                                'id': id_part,
                                'name': name_part if name_part else ''
                            })
            except Exception as e:
                print(f"Error extracting student info: {e}")
            
            return students
        except Exception as e:
            print(f"Error getting participated students info: {e}")
            return []
    
    def get_activity_info_from_row(self, row_index=0):
        """Get activity information from a specific table row (name, type, schedule)"""
        try:
            rows = self.get_table_rows()
            if row_index >= len(rows):
                return None
            
            row = rows[row_index]
            cells = row.find_elements(By.TAG_NAME, 'td')
            
            if len(cells) >= 4:
                activity_info = {
                    'date': cells[0].text.strip() if len(cells) > 0 else '',
                    'name': cells[1].text.strip() if len(cells) > 1 else '',
                    'type': cells[2].text.strip() if len(cells) > 2 else '',
                    'schedule': cells[3].text.strip() if len(cells) > 3 else '',
                }
                return activity_info
            
            return None
        except Exception as e:
            print(f"Error getting activity info from row: {e}")
            return None
    
    def has_participation_data(self):
        """Check if there is any participation data in the table"""
        rows = self.get_table_rows()
        return len(rows) > 0

