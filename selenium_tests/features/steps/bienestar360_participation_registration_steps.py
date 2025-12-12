from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.bienestar360_participation_segmentation_page import Bienestar360ParticipationSegmentationPage
from pages.bienestar360_login_page import Bienestar360LoginPage
from pages.bienestar360_homepage_cadi import Bienestar360HomePageCADI
import time
import re


@given('que el usuario está autenticado como administrador de Bienestar Universitario')
def step_given_admin_authenticated(context):
    context.login_page = Bienestar360LoginPage(context.driver)
    context.login_page.navigate_to()
    context.login_page.login("adminuser", "adminpass")
    time.sleep(1)
    context.homepage_cadi = Bienestar360HomePageCADI(context.driver)
    assert "homepageCADI" in context.driver.current_url or "admin" in context.driver.current_url.lower(), \
        "No se redirigió al homepage CADI después del login"


@given('que existen registros de participación en actividades')
def step_given_participation_records_exist(context):
    print("Asumiendo que existen registros de participación en la base de datos.")
    context.segmentation_page = Bienestar360ParticipationSegmentationPage(context.driver)
    context.segmentation_page.navigate_to()
    rows = context.segmentation_page.get_table_rows()
    assert len(rows) > 0, "No se encontraron registros de participación. Asegúrate de que hay datos de prueba."
    print(f"Se encontraron {len(rows)} registros de participación.")


@when('el sistema consulta la segmentación de participación')
def step_when_consult_segmentation(context):
    context.segmentation_page = Bienestar360ParticipationSegmentationPage(context.driver)
    context.segmentation_page.navigate_to()
    print("Consultando la segmentación de participación.")


@then('la información de participación queda almacenada en la base de datos')
def step_then_info_stored_in_db(context):
    rows = context.segmentation_page.get_table_rows()
    assert len(rows) > 0, "No se encontraron datos de participación en la UI, lo que sugiere que no están almacenados."
    print("La información de participación se muestra en la UI, asumiendo que está almacenada en la DB.")


@then('está disponible para reportes posteriores')
def step_then_available_for_reports(context):
    rows = context.segmentation_page.get_table_rows()
    assert len(rows) > 0, "No hay filas en la tabla para verificar la disponibilidad de reportes."
    
    first_row_index = 0
    activity_info = context.segmentation_page.get_activity_info_from_row(first_row_index)
    students = context.segmentation_page.get_participated_students_info(first_row_index)
    
    assert activity_info is not None, "No se pudo obtener la información de la actividad."
    assert activity_info.get('name') is not None and activity_info.get('name') != "", \
        "No se pudo obtener el nombre de la actividad."
    
    if len(students) > 0:
        for student in students:
            assert student.get("id") is not None and student.get("id") != "", \
                "El ID del estudiante no está disponible."
            assert student.get("name") is not None and student.get("name") != "", \
                "El nombre del estudiante no está disponible."
    
    print(f"Información de participación disponible para reportes.")
    print(f"  Actividad: '{activity_info.get('name')}'")
    print(f"  Tipo: '{activity_info.get('type')}'")
    print(f"  Horario: '{activity_info.get('schedule')}'")
    print(f"  Participantes: {len(students)}")
    for student in students:
        print(f"    - ID: {student['id']}, Nombre: {student['name']}")
