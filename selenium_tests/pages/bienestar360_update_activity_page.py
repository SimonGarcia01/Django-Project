from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class Bienestar360UpdateActivityPage(BasePage):
    """Page Object for Bienestar360 Update Activity Page"""
    
    # Locators - basados en el formulario de actualización
    NAME_FIELD = (By.ID, 'id_name')
    TYPE_FIELD = (By.ID, 'id_type')
    CATEGORY_FIELD = (By.ID, 'id_category')
    LOCATION_FIELD = (By.ID, 'id_location')
    DESCRIPTION_FIELD = (By.ID, 'id_description')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    PAGE_TITLE = (By.TAG_NAME, 'h1')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_page_loaded(self):
        """Check if the update page is loaded"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.PAGE_TITLE)
            )
            return "update" in self.driver.current_url.lower()
        except:
            return False
    
    def update_activity_name(self, new_name):
        """Update the activity name"""
        try:
            name_field = self.find_element(self.NAME_FIELD)
            name_field.clear()
            name_field.send_keys(new_name)
            return True
        except Exception as e:
            print(f"Error updating name: {e}")
            return False
    
    def update_activity_location(self, new_location):
        """Update the activity location"""
        try:
            location_field = self.find_element(self.LOCATION_FIELD)
            location_field.clear()
            location_field.send_keys(new_location)
            return True
        except Exception as e:
            print(f"Error updating location: {e}")
            return False
    
    def update_activity_description(self, new_description):
        """Update the activity description"""
        try:
            description_field = self.find_element(self.DESCRIPTION_FIELD)
            description_field.clear()
            description_field.send_keys(new_description)
            return True
        except Exception as e:
            print(f"Error updating description: {e}")
            return False
    
    def update_activity_type(self, activity_type):
        """Update the activity type"""
        try:
            type_select = Select(self.find_element(self.TYPE_FIELD))
            type_select.select_by_visible_text(activity_type)
            return True
        except Exception as e:
            print(f"Error updating type: {e}")
            return False
    
    def click_save_button(self):
        """Click the save/submit button"""
        try:
            submit_button = self.find_element(self.SUBMIT_BUTTON)
            # Scroll to button to ensure it's visible
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            import time
            time.sleep(0.3)
            
            # Click the button
            submit_button.click()
            
            # Don't wait here - let the step handle waiting
            # Just return success after clicking
            return True
        except Exception as e:
            print(f"Error clicking save button: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_current_name(self):
        """Get the current activity name"""
        try:
            name_field = self.find_element(self.NAME_FIELD)
            return name_field.get_attribute('value')
        except:
            return None
    
    def set_requires_registration(self, value):
        """Set the requires_registration checkbox"""
        try:
            checkbox = self.find_element((By.ID, 'id_requires_registration'))
            current_value = checkbox.is_selected()
            if current_value != value:
                checkbox.click()
            return True
        except Exception as e:
            print(f"Error setting requires_registration: {e}")
            return False
    
    def clear_max_capacity(self):
        """Clear the max_capacity field"""
        try:
            capacity_field = self.find_element((By.ID, 'id_max_capacity'))
            capacity_field.clear()
            return True
        except Exception as e:
            print(f"Error clearing max_capacity: {e}")
            return False
    
    def has_validation_error(self):
        """Check if there are validation errors on the page"""
        try:
            # Check for error messages in the form
            error_elements = self.driver.find_elements(By.CSS_SELECTOR, '.errorlist, .error, ul.errorlist li')
            if error_elements:
                for error in error_elements:
                    if error.is_displayed() and error.text.strip():
                        return True, error.text.strip()
            
            # Check for error messages in page source
            page_source = self.driver.page_source.lower()
            if 'error' in page_source or 'requerido' in page_source or 'cupo máximo' in page_source:
                # Try to find the specific error message
                error_text = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'cupo máximo') or contains(text(), 'Cupo máximo')]")
                if error_text:
                    return True, error_text[0].text.strip()
                return True, "Validation error found"
            
            return False, None
        except Exception as e:
            print(f"Error checking validation error: {e}")
            return False, None
    
    def is_still_on_update_page(self):
        """Check if still on update page (form was not submitted due to validation error)"""
        try:
            current_url = self.driver.current_url.lower()
            return "update" in current_url
        except:
            return False

