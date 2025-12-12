Feature: Visualizar actividades en calendario interactivo
  Como estudiante de ICESI
  Quiero visualizar las actividades disponibles en un calendario interactivo
  Para poder consultar las actividades de forma rápida y ver los horarios fácilmente

  Scenario: Mostrar actividades en vista de calendario
    Given que el estudiante ha accedido al portal de actividades sin inscripción
    Then las actividades publicadas se muestran en la vista /activities/view/
    When selecciona la opción "Calendario interactivo"
    Then el sistema muestra las actividades disponibles organizadas por fecha y hora dentro de una distribución de calendario
    And cada actividad incluye su nombre, categoría y ubicación

  Scenario: Intentar acceder al calendario sin autenticación
    Given que un usuario no autenticado intenta acceder al calendario interactivo
    When intenta navegar a la página del calendario
    Then el sistema redirige al usuario a la página de inicio de sesión
    And el calendario no se muestra

