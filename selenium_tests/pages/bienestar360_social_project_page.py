# pages/bienestar360_social_project_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time

class Bienestar360SocialProjectPage(BasePage):
    """Page Object para Proyectos Sociales"""
    
    # Locators
    PROJECT_SOCIAL_BUTTON = (By.XPATH, "//*[contains(text(), 'Proyecto Social')]")
    EVENT_CARDS = (By.CSS_SELECTOR, ".event-card, .card, .evento")
    INSCRIPTION_BUTTON = (By.XPATH, "//button[contains(text(), 'Inscribirse')]")
    CONFIRMATION_BUTTON = (By.XPATH, "//button[contains(text(), 'Confirmar')]")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "alert-success")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/proyecto-social/"
    
    def navigate_to_social_projects(self):
        """Navegar a la página de proyectos sociales"""
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    
    def click_social_project_button(self):
        """Hacer clic en el botón de Proyecto Social"""
        return self.click(self.PROJECT_SOCIAL_BUTTON)
    
    def select_first_available_event(self):
        """Seleccionar el primer evento disponible"""
        events = self.find_elements(self.EVENT_CARDS)
        if events:
            events[0].click()
            return True
        return False
    
    def click_inscription_button(self):
        """Hacer clic en el botón de inscripción"""
        return self.click(self.INSCRIPTION_BUTTON)
    
    def confirm_inscription(self):
        """Confirmar la inscripción si hay diálogo de confirmación"""
        try:
            confirm_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.CONFIRMATION_BUTTON)
            )
            confirm_btn.click()
            return True
        except:
            return False
    
    def is_inscription_successful(self):
        """Verificar si la inscripción fue exitosa"""
        return self.is_element_present(self.SUCCESS_MESSAGE)