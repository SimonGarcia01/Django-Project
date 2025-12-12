from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class Bienestar360HomePage(BasePage):
    """Page Object for Bienestar360 User Homepage"""
    
    # Locators - estos pueden necesitar ajuste después de inspeccionar
    SOCIAL_PROJECTS_LINK = (By.LINK_TEXT, 'Proyectos Sociales')  # Asumiendo que hay un enlace
    # O alternativamente por CSS/XPath si el texto es diferente
    # SOCIAL_PROJECTS_LINK = (By.CSS_SELECTOR, 'a[href*="social_projects"]')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/homepageUser/"
    
    def navigate_to(self):
        """Navigate to the homepage"""
        self.driver.get(self.url)
    
    def is_homepage_displayed(self):
        """Check if homepage is displayed"""
        # Verificar que estamos en la página correcta
        # Esto puede necesitar ajuste basado en elementos únicos de la página
        try:
            # Esperar a que la página cargue
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            return self.driver.current_url == self.url or "homepageUser" in self.driver.current_url
        except:
            return False
    
    def click_social_projects_link(self):
        """Click on social projects link"""
        # Intentar varios selectores posibles
        selectors = [
            (By.LINK_TEXT, 'Proyectos Sociales'),
            (By.PARTIAL_LINK_TEXT, 'Social'),
            (By.CSS_SELECTOR, 'a[href*="social_projects"]'),
        ]
        
        for selector in selectors:
            try:
                element = self.driver.find_element(*selector)
                element.click()
                return
            except:
                continue
        
        raise Exception("Social projects link not found")

