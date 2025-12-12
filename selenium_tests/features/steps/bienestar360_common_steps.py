from behave import given
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os

# Agregar el directorio raíz de selenium_tests al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from pages.bienestar360_login_page import Bienestar360LoginPage
from pages.bienestar360_homepage_cadi import Bienestar360HomePageCADI
from pages.bienestar360_public_activities_page import Bienestar360PublicActivitiesPage
from pages.bienestar360_activities_page import Bienestar360ActivitiesPage
import time


@given('que el personal del equipo CADI ha accedido al panel de administración')
def step_given_cadi_access_admin_panel(context):
    """CADI staff accesses the admin panel - Common step for multiple features"""
    # Login as admin
    context.login_page = Bienestar360LoginPage(context.driver)
    context.login_page.navigate_to()
    context.login_page.login("adminuser", "adminpass")
    
    # Wait for redirect to CADI homepage
    WebDriverWait(context.driver, 10).until(
        lambda driver: "homepageCADI" in driver.current_url or 
                       "homepage" in driver.current_url.lower()
    )
    
    # Verify we're logged in as admin
    context.homepage_cadi = Bienestar360HomePageCADI(context.driver)
    assert context.homepage_cadi.is_homepage_displayed() or "homepageCADI" in context.driver.current_url, \
        "CADI login failed"


@given('ha buscado una actividad previamente registrada')
def step_given_searched_activity(context):
    """Search for a previously registered activity - Common step for update and delete"""
    # Navigate to public activities page (admin view)
    context.public_activities_page = Bienestar360PublicActivitiesPage(context.driver)
    context.public_activities_page.navigate_to()
    
    # Wait for page to load
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )
    time.sleep(1)
    
    # Get the first activity
    activities = context.public_activities_page.get_activities()
    assert len(activities) > 0, "No activities found"
    
    # Store the activity's name for later verification
    try:
        name_element = activities[0].find_element(By.CSS_SELECTOR, 'h2')
        context.activity_name = name_element.text
    except:
        # If we can't get the name, use a default
        context.activity_name = "Test Activity"
    
    # Store activity for both update and delete operations
    context.activity_to_update = activities[0]
    context.activity_to_delete = activities[0]
    context.activity = activities[0]  # Generic reference
    
    # Store initial count (useful for delete test)
    context.initial_count = context.public_activities_page.get_activity_count()


@given('que el estudiante ha accedido al portal de actividades sin inscripción')
def step_given_access_activities_portal(context):
    """Access the activities portal - Common step for multiple features"""
    # Check if student needs to be logged in (for calendar access, login is required)
    # For now, we'll login the student to ensure access to all features
    # Login as student if not already logged in
    try:
        # Try to access activities page first
        context.activities_page = Bienestar360ActivitiesPage(context.driver)
        context.activities_page.navigate_to()
        
        # Check if we're redirected to login
        WebDriverWait(context.driver, 5).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        time.sleep(1)
        
        # If redirected to login, login as student
        if "login" in context.driver.current_url.lower():
            context.login_page = Bienestar360LoginPage(context.driver)
            context.login_page.login("basicuser", "password123")
            # Wait for redirect
            WebDriverWait(context.driver, 10).until(
                lambda driver: "login" not in driver.current_url.lower()
            )
            # Navigate to activities again
            context.activities_page.navigate_to()
    except:
        # If error, try to login first
        context.login_page = Bienestar360LoginPage(context.driver)
        context.login_page.navigate_to()
        context.login_page.login("basicuser", "password123")
        # Wait for redirect
        WebDriverWait(context.driver, 10).until(
            lambda driver: "login" not in driver.current_url.lower()
        )
        # Navigate to activities
        context.activities_page = Bienestar360ActivitiesPage(context.driver)
        context.activities_page.navigate_to()
    
    # Verificar que la página cargó correctamente
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'h1'))
    )

