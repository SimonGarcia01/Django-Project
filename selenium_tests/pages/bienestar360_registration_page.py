from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class Bienestar360RegistrationPage(BasePage):
    """Page Object for Bienestar360 Registration Page"""
    
    # Locators - usando selectores inferidos de Django
    IDENTIFICATION_FIELD = (By.ID, 'id_identification')
    USERNAME_FIELD = (By.ID, 'id_username')
    FIRST_NAME_FIELD = (By.ID, 'id_first_name')
    LAST_NAME_FIELD = (By.ID, 'id_last_name')
    GENDER_FIELD = (By.ID, 'id_gender')
    EMAIL_FIELD = (By.ID, 'id_email')
    FACULTY_FIELD = (By.ID, 'id_faculty')
    PASSWORD1_FIELD = (By.ID, 'id_password1')
    PASSWORD2_FIELD = (By.ID, 'id_password2')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button.btn-submit')  # Botón "Crear cuenta"
    ERROR_MESSAGE = (By.CSS_SELECTOR, '.form-errors p')  # Mensajes de error generales
    FIELD_ERRORS = (By.CSS_SELECTOR, '.error-message')  # Mensajes de error de campos
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, '.success-message, .alert-success')  # Mensaje de éxito
    PAGE_TITLE = (By.CSS_SELECTOR, '.card-title')  # Título "Crear Cuenta"
    LOGIN_LINK = (By.LINK_TEXT, 'Inicia sesión')  # Enlace a login
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/registration/"
    
    def navigate_to(self):
        """Navigate to the registration page"""
        self.driver.get(self.url)
    
    def enter_identification(self, identification):
        """Enter identification number"""
        field = self.find_element(self.IDENTIFICATION_FIELD)
        field.clear()
        if identification:
            field.send_keys(identification)
    
    def enter_username(self, username):
        """Enter username"""
        field = self.find_element(self.USERNAME_FIELD)
        field.clear()
        if username:
            field.send_keys(username)
    
    def enter_first_name(self, first_name):
        """Enter first name"""
        field = self.find_element(self.FIRST_NAME_FIELD)
        field.clear()
        if first_name:
            field.send_keys(first_name)
    
    def enter_last_name(self, last_name):
        """Enter last name"""
        field = self.find_element(self.LAST_NAME_FIELD)
        field.clear()
        if last_name:
            field.send_keys(last_name)
    
    def select_gender(self, gender):
        """Select gender from dropdown"""
        try:
            gender_select = Select(self.find_element(self.GENDER_FIELD))
            gender_select.select_by_value(gender)
            return True
        except:
            return False
    
    def enter_email(self, email):
        """Enter email"""
        field = self.find_element(self.EMAIL_FIELD)
        field.clear()
        if email:
            field.send_keys(email)
    
    def select_faculty(self, faculty_name):
        """Select faculty from dropdown by visible text"""
        try:
            faculty_select = Select(self.find_element(self.FACULTY_FIELD))
            faculty_select.select_by_visible_text(faculty_name)
            return True
        except:
            return False
    
    def enter_password1(self, password):
        """Enter password"""
        field = self.find_element(self.PASSWORD1_FIELD)
        field.clear()
        if password:
            field.send_keys(password)
    
    def enter_password2(self, password):
        """Enter password confirmation"""
        field = self.find_element(self.PASSWORD2_FIELD)
        field.clear()
        if password:
            field.send_keys(password)
    
    def fill_registration_form(self, identification, username, first_name, last_name, 
                              gender, email, faculty, password1, password2):
        """Fill complete registration form"""
        self.enter_identification(identification)
        self.enter_username(username)
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.select_gender(gender)
        self.enter_email(email)
        self.select_faculty(faculty)
        self.enter_password1(password1)
        self.enter_password2(password2)
    
    def click_submit_button(self):
        """Click the submit button"""
        self.click(self.SUBMIT_BUTTON)
    
    def is_error_displayed(self):
        """Check if error message is displayed"""
        try:
            error_elements = self.driver.find_elements(*self.ERROR_MESSAGE)
            field_errors = self.driver.find_elements(*self.FIELD_ERRORS)
            return len(error_elements) > 0 or len(field_errors) > 0
        except:
            return False
    
    def get_error_messages(self):
        """Get all error messages"""
        errors = []
        try:
            error_elements = self.driver.find_elements(*self.ERROR_MESSAGE)
            for elem in error_elements:
                if elem.text:
                    errors.append(elem.text)
            
            field_errors = self.driver.find_elements(*self.FIELD_ERRORS)
            for elem in field_errors:
                if elem.text:
                    errors.append(elem.text)
        except:
            pass
        return errors
    
    def is_success_displayed(self):
        """Check if success message is displayed"""
        try:
            # After successful registration, user is redirected to login page
            # Check if we're on login page (which indicates success)
            WebDriverWait(self.driver, 5).until(
                lambda driver: "login" in driver.current_url.lower()
            )
            # Check if we're on login page (not registration)
            return "registration" not in self.driver.current_url.lower()
        except:
            return False
    
    def get_page_title(self):
        """Get the page title text"""
        try:
            title_element = self.find_element(self.PAGE_TITLE)
            return title_element.text
        except:
            return None

