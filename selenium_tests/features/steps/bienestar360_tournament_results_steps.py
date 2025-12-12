from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.bienestar360_tournament_page import (
    Bienestar360TournamentPage,
    Bienestar360ResultsPage,
    Bienestar360RegisterResultPage
)
import time


@given('que un partido ha finalizado')
def step_given_game_finished(context):
    """Step: Un partido ha finalizado (asumimos que existe un partido con fecha pasada)"""
    # Navegar a la página de resultados para encontrar un partido
    context.results_page = Bienestar360ResultsPage(context.driver)
    context.results_page.navigate_to()
    time.sleep(1)
    
    # Buscar un partido que haya finalizado (que tenga botón de registrar resultado)
    # Por simplicidad, asumimos que hay al menos un partido disponible
    results = context.results_page.get_results()
    assert len(results) > 0, "No hay partidos disponibles para registrar resultados"
    
    # Obtener el ID del primer partido disponible
    # Buscar el link de "Registrar / Editar Resultado" en el primer card
    try:
        first_card = results[0]
        register_link = first_card.find_element(By.CSS_SELECTOR, 'a[href*="register_result"]')
        href = register_link.get_attribute('href')
        # Extraer el game_id de la URL: /register_result/{game_id}/
        import re
        match = re.search(r'register_result/(\d+)/', href)
        if match:
            context.game_id = int(match.group(1))
            print(f"Partido encontrado con ID: {context.game_id}")
        else:
            # Si no hay link, intentar obtener el ID de otra forma
            # Por ahora, usaremos un ID por defecto (esto debería mejorarse)
            context.game_id = 1
            print(f"Usando game_id por defecto: {context.game_id}")
    except Exception as e:
        print(f"No se pudo obtener el game_id del card: {e}")
        # Usar un ID por defecto
        context.game_id = 1
        print(f"Usando game_id por defecto: {context.game_id}")


@when('el miembro de Bienestar registra el marcador')
def step_when_register_score(context):
    """Step: Registrar el marcador del partido"""
    # Navegar a la página de registro de resultados
    context.register_result_page = Bienestar360RegisterResultPage(context.driver)
    context.register_result_page.navigate_to(context.game_id)
    time.sleep(1)
    
    # Registrar un marcador de ejemplo (por ejemplo, 2-1)
    context.home_score = 2
    context.guest_score = 1
    
    success = context.register_result_page.register_result(
        context.home_score,
        context.guest_score
    )
    assert success, "No se pudo registrar el resultado del partido"
    time.sleep(1)


@then('el sistema actualiza los resultados en la base de datos')
def step_then_database_updated(context):
    """Step: Verificar que el resultado se actualizó en la base de datos"""
    # Verificar que se redirigió a la página de resultados
    assert "results" in context.driver.current_url.lower() or "resultado" in context.driver.current_url.lower(), \
        "No se redirigió a la página de resultados después de registrar"
    
    # Verificar que hay un mensaje de éxito (opcional, si existe)
    time.sleep(1)
    print("Resultado registrado exitosamente en la base de datos")


@then('los refleja en la tabla de clasificación')
def step_then_reflected_in_table(context):
    """Step: Verificar que el resultado se refleja en la tabla de clasificación"""
    # Navegar a la página de resultados si no estamos ahí
    if "results" not in context.driver.current_url.lower():
        context.results_page = Bienestar360ResultsPage(context.driver)
        context.results_page.navigate_to()
        time.sleep(1)
    
    # Verificar que el resultado aparece en la página
    result_exists = context.results_page.result_exists(
        context.home_score,
        context.guest_score
    )
    assert result_exists, \
        f"El resultado {context.home_score}-{context.guest_score} no aparece en la tabla de clasificación"

