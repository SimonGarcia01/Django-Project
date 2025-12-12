from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class Bienestar360HomePageCADI(BasePage):
    """Page Object for Bienestar360 CADI Homepage (Admin)"""
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/homepageCADI/"
    
    def navigate_to(self):
        """Navigate to the CADI homepage"""
        self.driver.get(self.url)
    
    def is_homepage_displayed(self):
        """Check if CADI homepage is displayed"""
        try:
            # Esperar a que la página cargue
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            return self.driver.current_url == self.url or "homepageCADI" in self.driver.current_url
        except:
            return False

