from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time


class Bienestar360FormalReportPage(BasePage):
    PAGE_TITLE = (By.TAG_NAME, 'h1')
    FILTER_FORM = (By.ID, 'filter-form')
    
    ACTIVITY_TYPE_CHECKBOXES = (By.CSS_SELECTOR, 'input[type="checkbox"][name="activity_type"]')
    FACULTY_CHECKBOXES = (By.CSS_SELECTOR, 'input[type="checkbox"][name="faculty"]')
    GENDER_CHECKBOXES = (By.CSS_SELECTOR, 'input[type="checkbox"][name="gender"]')
    FREQUENCY_MIN = (By.NAME, 'frequency_min')
    FREQUENCY_MAX = (By.NAME, 'frequency_max')
    DATE_START = (By.NAME, 'date_start')
    DATE_END = (By.NAME, 'date_end')
    
    GENERATE_REPORT_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"].button')
    CLEAR_FILTERS_BUTTON = (By.LINK_TEXT, '🔄 Limpiar Filtros')
    
    STATS_GRID = (By.CSS_SELECTOR, '.stats-grid')
    STAT_CARDS = (By.CSS_SELECTOR, '.stat-card')
    CHARTS_SECTION = (By.CSS_SELECTOR, '.charts-section')
    
    EXPORT_CSV_BUTTON = (By.CSS_SELECTOR, 'a.download-btn-csv, .download-btn-csv')
    
    MESSAGE_DIV = (By.ID, 'message')
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, '.message.error, .empty-message')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/reportsAndStats/participation-formal-report/"
    
    def navigate_to(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PAGE_TITLE)
        )
        time.sleep(0.5)
    
    def select_activity_type(self, activity_type):
        try:
            checkboxes = self.driver.find_elements(*self.ACTIVITY_TYPE_CHECKBOXES)
            for checkbox in checkboxes:
                if checkbox.get_attribute('value') == activity_type:
                    if not checkbox.is_selected():
                        checkbox.click()
                    return True
            return False
        except Exception as e:
            print(f"Error selecting activity type: {e}")
            return False
    
    def select_faculty(self, faculty_name):
        try:
            checkboxes = self.driver.find_elements(*self.FACULTY_CHECKBOXES)
            for checkbox in checkboxes:
                checkbox_value = checkbox.get_attribute('value')
                try:
                    label_element = checkbox.find_element(By.XPATH, './following-sibling::text()[1]')
                    checkbox_label = label_element.strip() if label_element else ''
                except:
                    try:
                        parent = checkbox.find_element(By.XPATH, './..')
                        checkbox_label = parent.text.strip()
                    except:
                        checkbox_label = ''
                
                if checkbox_value == faculty_name or faculty_name in checkbox_label or faculty_name in checkbox_value:
                    if not checkbox.is_selected():
                        checkbox.click()
                    return True
            return False
        except Exception as e:
            print(f"Error selecting faculty: {e}")
            return False
    
    def select_gender(self, gender):
        try:
            checkboxes = self.driver.find_elements(*self.GENDER_CHECKBOXES)
            for checkbox in checkboxes:
                if checkbox.get_attribute('value') == gender:
                    if not checkbox.is_selected():
                        checkbox.click()
                    return True
            return False
        except Exception as e:
            print(f"Error selecting gender: {e}")
            return False
    
    def set_frequency_range(self, min_freq=None, max_freq=None):
        try:
            if min_freq is not None:
                min_field = self.find_element(self.FREQUENCY_MIN)
                min_field.clear()
                min_field.send_keys(str(min_freq))
                time.sleep(0.2)
            
            if max_freq is not None:
                max_field = self.find_element(self.FREQUENCY_MAX)
                max_field.clear()
                max_field.send_keys(str(max_freq))
                time.sleep(0.2)
            
            return True
        except Exception as e:
            print(f"Error setting frequency range: {e}")
            return False
    
    def set_date_range(self, start_date=None, end_date=None):
        try:
            if start_date:
                start_field = self.find_element(self.DATE_START)
                start_field.clear()
                start_field.send_keys(start_date)
                time.sleep(0.2)
            
            if end_date:
                end_field = self.find_element(self.DATE_END)
                end_field.clear()
                end_field.send_keys(end_date)
                time.sleep(0.2)
            
            return True
        except Exception as e:
            print(f"Error setting date range: {e}")
            return False
    
    def apply_filters(self):
        try:
            submit_button = self.find_element(self.GENERATE_REPORT_BUTTON)
            self.close_password_dialogs()
            time.sleep(0.3)
            submit_button.click()
            print("Filters applied, waiting for report generation...")
            time.sleep(2)
            self.close_password_dialogs()
            return True
        except Exception as e:
            print(f"Error applying filters: {e}")
            return False
    
    def clear_filters(self):
        try:
            clear_button = self.find_element(self.CLEAR_FILTERS_BUTTON)
            clear_button.click()
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error clearing filters: {e}")
            return False
    
    def has_report_data(self):
        try:
            stat_cards = self.driver.find_elements(*self.STAT_CARDS)
            return len(stat_cards) > 0
        except:
            return False
    
    def get_stat_value(self, stat_index=0):
        try:
            stat_cards = self.driver.find_elements(*self.STAT_CARDS)
            if stat_index < len(stat_cards):
                stat_value = stat_cards[stat_index].find_element(By.CSS_SELECTOR, '.stat-value')
                return stat_value.text.strip()
            return None
        except Exception as e:
            print(f"Error getting stat value: {e}")
            return None
    
    def has_no_results_message(self):
        try:
            messages = self.driver.find_elements(*self.NO_RESULTS_MESSAGE)
            if len(messages) > 0:
                return True
            
            page_text = self.driver.page_source.lower()
            no_results_keywords = ['no hay resultados', 'sin datos', 'no se encontraron', 'no hay registros', 'no se encontraron registros']
            for keyword in no_results_keywords:
                if keyword in page_text:
                    return True
            
            stat_cards = self.driver.find_elements(*self.STAT_CARDS)
            if len(stat_cards) > 0:
                all_zero = True
                for card in stat_cards:
                    try:
                        stat_value_elem = card.find_element(By.CSS_SELECTOR, '.stat-value, .value')
                        stat_value = stat_value_elem.text.strip()
                        if stat_value and stat_value != '0' and stat_value != '0.0' and stat_value != '0%':
                            all_zero = False
                            break
                    except:
                        pass
                if all_zero:
                    return True
            
            return False
        except:
            return False
    
    def has_charts(self):
        try:
            charts_section = self.find_element(self.CHARTS_SECTION)
            return charts_section.is_displayed()
        except:
            return False
    
    def click_export_csv(self):
        try:
            csv_button = self.find_element(self.EXPORT_CSV_BUTTON)
            self.close_password_dialogs()
            time.sleep(0.3)
            csv_button.click()
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Error clicking export CSV: {e}")
            return False
    
    def click_export_excel(self):
        try:
            excel_button = self.driver.find_element(By.CSS_SELECTOR, 'a.download-btn-excel, .download-btn-excel, a[href*="excel"], a[href*="xlsx"]')
            self.close_password_dialogs()
            time.sleep(0.3)
            excel_button.click()
            time.sleep(1)
            return True
        except Exception as e:
            print(f"⚠️ Botón de exportar a Excel no encontrado: {e}")
            return False

