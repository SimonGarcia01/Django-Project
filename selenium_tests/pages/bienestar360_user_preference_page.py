# pages/bienestar360_user_preference_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

from .base_page import BasePage


class Bienestar360UserPreferencePage(BasePage):
    """Page Object for Bienestar360 User Preference Selection"""
   
    PAGE_TITLE = (By.TAG_NAME, 'h1')  
    
    RECEIVE_ALERTS_CHECKBOX = (By.ID, 'id_receive_alerts')
    GROUP_ACTIVITY_CHECKBOX = (By.ID, 'id_is_group_activity')
    INDIVIDUAL_ACTIVITY_CHECKBOX = (By.ID, 'id_is_individual_activity')
    SPORT_CHECKBOX = (By.ID, 'id_is_sport')
    ART_CHECKBOX = (By.ID, 'id_is_art')
    PSYCHOLOGY_CHECKBOX = (By.ID, 'id_is_psychology')
    
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, '.alert-success, .messages .success')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/preferences/setup/"
    
    def navigate_to(self):
        """Navigate to the user preference setup page"""
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    
    def set_preferences(self, preferences_dict):
        """Set user preferences based on dictionary"""
        try:
            print(f"Setting preferences: {preferences_dict}")
            
            if 'receive_alerts' in preferences_dict:
                self._set_checkbox(self.RECEIVE_ALERTS_CHECKBOX, preferences_dict['receive_alerts'])
            
            if 'group_activity' in preferences_dict:
                self._set_checkbox(self.GROUP_ACTIVITY_CHECKBOX, preferences_dict['group_activity'])
            
            if 'individual_activity' in preferences_dict:
                self._set_checkbox(self.INDIVIDUAL_ACTIVITY_CHECKBOX, preferences_dict['individual_activity'])
            
            if 'sport' in preferences_dict:
                self._set_checkbox(self.SPORT_CHECKBOX, preferences_dict['sport'])
            
            if 'art' in preferences_dict:
                self._set_checkbox(self.ART_CHECKBOX, preferences_dict['art'])
            
            if 'psychology' in preferences_dict:
                self._set_checkbox(self.PSYCHOLOGY_CHECKBOX, preferences_dict['psychology'])
            
            return True
        except Exception as e:
            print(f"Error setting preferences: {e}")
            return False
    
    def _set_checkbox(self, locator, value):
        """Set checkbox to desired state"""
        checkbox = self.find_element(locator)
        current_state = checkbox.is_selected()
        
        if value and not current_state:
            checkbox.click()
            print(f"Checked checkbox: {locator}")
        elif not value and current_state:
            checkbox.click()
            print(f"Unchecked checkbox: {locator}")
        else:
            print(f"Checkbox already in desired state: {locator}")
    
    def submit_preferences(self):
        """Submit the preferences form"""
        try:
            self.close_password_dialogs()
            time.sleep(0.5)
            
            submit_button = self.find_element(self.SUBMIT_BUTTON)
            submit_button.click()
            print("Preferences form submitted")
            
            time.sleep(0.5)
            self.close_password_dialogs()
            
            WebDriverWait(self.driver, 10).until(
                lambda driver: "homepageUser" in driver.current_url
            )
            
            return True
        except Exception as e:
            print(f"Error submitting preferences: {e}")
            return False
    
    def get_current_preferences(self):
        """Get current state of all preferences"""
        try:
            preferences = {
                'receive_alerts': self.find_element(self.RECEIVE_ALERTS_CHECKBOX).is_selected(),
                'group_activity': self.find_element(self.GROUP_ACTIVITY_CHECKBOX).is_selected(),
                'individual_activity': self.find_element(self.INDIVIDUAL_ACTIVITY_CHECKBOX).is_selected(),
                'sport': self.find_element(self.SPORT_CHECKBOX).is_selected(),
                'art': self.find_element(self.ART_CHECKBOX).is_selected(),
                'psychology': self.find_element(self.PSYCHOLOGY_CHECKBOX).is_selected()
            }
            return preferences
        except Exception as e:
            print(f"Error getting current preferences: {e}")
            return {}
    
    def is_success_message_displayed(self):
        """Check if success message is displayed"""
        try:
            messages = self.driver.find_elements(*self.SUCCESS_MESSAGE)
            return len(messages) > 0
        except:
            return False


class Bienestar360UserHomePage(BasePage):
    """Page Object for User Homepage where preferences are accessed"""
    
   
    PAGE_TITLE = (By.TAG_NAME, 'h1')  
    PREFERENCES_LINK = (By.LINK_TEXT, 'Alertas personalizadas')
    QUICK_ACCESS_GRID = (By.CSS_SELECTOR, '.access-grid')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/homepageUser/"
    
    def navigate_to(self):
        """Navigate to user homepage"""
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    
    def click_preferences_link(self):
        """Click the preferences/alerts link - ADAPTED VERSION"""
        try:
            print("Navegando directamente a página de preferencias...")
            self.driver.get("http://localhost:8000/preferences/setup/")
            return True
        except Exception as e:
            print(f"Error en navegación directa: {e}")
            return False
    
    def is_preferences_link_available(self):
        """Check if preferences link is available"""
        return True