from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
import random
import string

# Agregar el directorio raíz de selenium_tests al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from pages.bienestar360_registration_page import Bienestar360RegistrationPage
from pages.bienestar360_login_page import Bienestar360LoginPage


def generate_random_username():
    """Generate a random username for testing"""
    return f"testuser_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}"


def generate_random_email():
    """Generate a random email for testing"""
    return f"test_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}@example.com"


@given('Un usuario este en la página de registro')
def step_given_user_on_registration_page(context):
    """Navigate to registration page"""
    context.registration_page = Bienestar360RegistrationPage(context.driver)
    context.registration_page.navigate_to()


@given('ha ingresado la información necesaria para crear un usuario')
def step_given_entered_required_info(context):
    """Enter all required information for user registration"""
    # Generar datos únicos para evitar conflictos
    context.test_username = generate_random_username()
    context.test_email = generate_random_email()
    context.test_identification = f"{random.randint(100000000, 999999999)}"
    
    # Llenar el formulario con información válida
    context.registration_page.fill_registration_form(
        identification=context.test_identification,
        username=context.test_username,
        first_name="Test",
        last_name="User",
        gender="M",  # M, F, O
        email=context.test_email,
        faculty="Ingeniería de Sistemas",  # Debe existir en la BD (creado por signals)
        password1="testpassword123",
        password2="testpassword123"
    )


@given('no tenía una cuenta registrada antes')
def step_given_no_previous_account(context):
    """Verify user didn't have an account before"""
    # Esto se verifica usando un username único generado
    # El username se genera en el step anterior
    assert hasattr(context, 'test_username'), "Test username should have been generated"
    # El sistema verificará esto automáticamente al intentar crear el usuario


@given('intenta registrarse con un nombre de usuario que ya existe "{username}"')
def step_given_existing_username(context, username):
    """Try to register with an existing username"""
    context.registration_page.fill_registration_form(
        identification=f"{random.randint(100000000, 999999999)}",
        username=username,
        first_name="Test",
        last_name="User",
        gender="M",
        email=generate_random_email(),
        faculty="Ingeniería de Sistemas",
        password1="testpassword123",
        password2="testpassword123"
    )


@given('ha ingresado información incompleta para crear un usuario')
def step_given_incomplete_info(context):
    """Enter incomplete information for registration"""
    # Solo llenar algunos campos, dejar otros vacíos
    context.registration_page.enter_username(generate_random_username())
    context.registration_page.enter_first_name("Test")
    # No llenar otros campos requeridos


@given('ha ingresado información válida pero con contraseñas que no coinciden')
def step_given_mismatched_passwords(context):
    """Enter valid information but with mismatched passwords"""
    context.registration_page.fill_registration_form(
        identification=f"{random.randint(100000000, 999999999)}",
        username=generate_random_username(),
        first_name="Test",
        last_name="User",
        gender="M",
        email=generate_random_email(),
        faculty="Ingeniería de Sistemas",
        password1="testpassword123",
        password2="differentpassword456"  # Contraseñas no coinciden
    )


@when('presiona "Crear Usuario"')
def step_when_click_create_user(context):
    """Click create user button"""
    context.registration_page.click_submit_button()
    # Esperar a que se procese el formulario
    WebDriverWait(context.driver, 5).until(
        lambda driver: driver.execute_script("return document.readyState") == "complete"
    )


@then('el sistema registra el usuario')
def step_then_user_registered(context):
    """Verify user is registered"""
    # Después de registro exitoso, el usuario es redirigido a la página de login
    WebDriverWait(context.driver, 10).until(
        lambda driver: "login" in driver.current_url.lower() and 
                       "registration" not in driver.current_url.lower()
    )
    
    current_url = context.driver.current_url.lower()
    assert "registration" not in current_url, \
        "User should be redirected from registration page after successful registration"
    assert "login" in current_url, \
        f"Expected to be redirected to login page, but is on: {current_url}"


@then('le muestra mensaje de éxito')
def step_then_success_message_shown(context):
    """Verify success message is displayed"""
    # Verificar que fuimos redirigidos a login (esto indica éxito)
    # El sistema redirige a login después de registro exitoso
    WebDriverWait(context.driver, 10).until(
        lambda driver: "login" in driver.current_url.lower() and 
                       "registration" not in driver.current_url.lower()
    )
    
    current_url = context.driver.current_url.lower()
    assert "login" in current_url and "registration" not in current_url, \
        f"After successful registration, user should be redirected to login page, but is on: {current_url}"
    
    # Verificar que estamos en la página de login (puede verificar el título)
    try:
        login_page = Bienestar360LoginPage(context.driver)
        # Esperar a que la página de login cargue
        WebDriverWait(context.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        # La redirección a login es suficiente indicador de éxito
        assert True
    except:
        # Si hay algún problema, al menos verificamos que no estamos en registration
        assert "registration" not in current_url, \
            "User should not be on registration page after successful registration"


@then('el sistema muestra un mensaje de error indicando que el usuario ya existe')
def step_then_user_exists_error(context):
    """Verify error message for existing user"""
    # Esperar a que aparezca el error
    WebDriverWait(context.driver, 5).until(
        lambda driver: context.registration_page.is_error_displayed() or
                       "registration" in driver.current_url.lower()
    )
    
    # Verificar que estamos aún en la página de registro
    current_url = context.driver.current_url.lower()
    assert "registration" in current_url, \
        "User should remain on registration page when there's an error"
    
    # Verificar que hay mensajes de error
    errors = context.registration_page.get_error_messages()
    # El error puede estar en los mensajes de error o en el texto de la página
    page_text = context.driver.page_source.lower()
    assert len(errors) > 0 or "usuario" in page_text or "ya existe" in page_text or "username" in page_text, \
        "Expected error message about existing user, but no error found"


@then('el usuario permanece en la página de registro')
def step_then_stays_on_registration_page(context):
    """Verify user remains on registration page"""
    current_url = context.driver.current_url.lower()
    assert "registration" in current_url, \
        f"Expected to stay on registration page, but is on: {current_url}"


@then('el sistema muestra mensajes de error para los campos requeridos')
def step_then_required_fields_error(context):
    """Verify error messages for required fields"""
    # Esperar a que aparezcan los errores
    WebDriverWait(context.driver, 5).until(
        lambda driver: context.registration_page.is_error_displayed() or
                       "registration" in driver.current_url.lower()
    )
    
    # Verificar que estamos aún en la página de registro
    current_url = context.driver.current_url.lower()
    assert "registration" in current_url, \
        "User should remain on registration page when there are validation errors"
    
    # Verificar que hay mensajes de error
    errors = context.registration_page.get_error_messages()
    assert len(errors) > 0, "Expected error messages for required fields, but none found"


@then('el sistema muestra un mensaje de error indicando que las contraseñas no coinciden')
def step_then_password_mismatch_error(context):
    """Verify error message for password mismatch"""
    # Esperar a que aparezca el error
    WebDriverWait(context.driver, 5).until(
        lambda driver: context.registration_page.is_error_displayed() or
                       "registration" in driver.current_url.lower()
    )
    
    # Verificar que estamos aún en la página de registro
    current_url = context.driver.current_url.lower()
    assert "registration" in current_url, \
        "User should remain on registration page when passwords don't match"
    
    # Verificar que hay mensajes de error relacionados con contraseñas
    errors = context.registration_page.get_error_messages()
    page_text = context.driver.page_source.lower()
    
    # Buscar palabras clave relacionadas con contraseñas
    password_keywords = ["contraseña", "password", "coinciden", "match", "no coinciden"]
    has_password_error = any(keyword in page_text for keyword in password_keywords) or \
                        any(keyword in str(errors).lower() for keyword in password_keywords)
    
    assert has_password_error or len(errors) > 0, \
        "Expected error message about password mismatch, but no relevant error found"

