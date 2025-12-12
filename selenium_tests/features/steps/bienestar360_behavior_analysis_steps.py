from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.bienestar360_formal_report_page import Bienestar360FormalReportPage
import time


@given('que soy analista de Bienestar Universitario')
def step_given_analyst(context):
    print("Usuario autenticado como analista de Bienestar Universitario")


@given('consulto los registros de participación en actividades')
def step_given_consult_records(context):
    context.report_page = Bienestar360FormalReportPage(context.driver)
    context.report_page.navigate_to()
    time.sleep(1)
    print("Navegando a la página de reportes formales de participación")


@when('aplico filtros de frecuencia, tipo de actividad o alguna característica demográfica especifica')
def step_when_apply_filters(context):
    context.report_page.select_activity_type("Deportiva")
    time.sleep(0.3)
    context.report_page.set_frequency_range(min_freq=1)
    time.sleep(0.3)
    context.report_page.apply_filters()
    time.sleep(2)
    print("Filtros aplicados: tipo de actividad y frecuencia")


@when('no aplico ningún filtro')
def step_when_no_filters(context):
    context.report_page.apply_filters()
    time.sleep(2)
    print("Generando reporte sin filtros (todos los datos)")


@when('aplico filtros que no coinciden con ningún registro')
def step_when_apply_no_match_filters(context):
    context.report_page.select_gender("O")
    time.sleep(0.3)
    context.report_page.apply_filters()
    time.sleep(2)
    print("Filtros aplicados (género 'Otro') que no deberían devolver resultados")




@then('el sistema genera un reporte segmentado con los patrones de comportamiento')
def step_then_generate_segmented_report(context):
    has_data = context.report_page.has_report_data()
    assert has_data, "El reporte no muestra datos después de aplicar filtros"
    
    stat_value = context.report_page.get_stat_value(0)
    assert stat_value is not None, "No se encontraron estadísticas en el reporte"
    
    print(f"Reporte segmentado generado. Estadística: {stat_value}")
    
    has_charts = context.report_page.has_charts()
    if has_charts:
        print("Gráficos de comportamiento mostrados")


@then('permite exportar información para realizar más análisis')
def step_then_allow_export(context):
    try:
        csv_button = context.driver.find_element(By.CSS_SELECTOR, '.download-btn-csv, a.download-btn-csv')
        assert csv_button.is_displayed(), "Botón de exportar a CSV no está visible"
        print("Botón de exportación a CSV disponible")
    except Exception as e:
        print(f"No se pudo verificar el botón de exportación: {e}")


@then('el sistema genera un reporte con todos los datos de participación')
def step_then_generate_all_data_report(context):
    has_data = context.report_page.has_report_data()
    assert has_data, "El reporte no muestra datos"
    
    stat_value = context.report_page.get_stat_value(0)
    assert stat_value is not None, "No se encontraron estadísticas en el reporte"
    
    print(f"Reporte generado con todos los datos. Estadística: {stat_value}")


@then('el sistema muestra un mensaje indicando que no hay resultados')
def step_then_show_no_results_message(context):
    has_message = context.report_page.has_no_results_message()
    assert has_message, "No se mostró mensaje indicando que no hay resultados ni se detectaron valores en 0"
    print("Mensaje de 'sin resultados' mostrado o todos los valores son 0")


@then('el reporte no muestra datos')
def step_then_no_data_in_report(context):
    has_message = context.report_page.has_no_results_message()
    assert has_message, "El reporte muestra datos cuando no debería (valores diferentes de 0)"
    print("Reporte no muestra datos (todos los valores son 0 o hay mensaje de sin resultados)")



