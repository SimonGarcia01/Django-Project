Feature: Filtrar actividades con inscripción
  Como estudiante de ICESI
  Quiero filtrar las actividades por tipo, lugar y horario
  Para poder encontrar mis intereses más rápido y que se ajusten a mi horario de clases

  Background:
    Given que el estudiante ha accedido al portal de actividades sin inscripción

  Scenario: Filtrar actividades por tipo - Artística
    When selecciona el filtro "Tipo de actividad"
    And elige la categoría "Artística"
    And hace clic en el botón "Filtrar"
    Then el sistema muestra únicamente las actividades de tipo "Artística"
    And cada actividad mostrada tiene el tipo "Artística"

  Scenario: Filtrar actividades por tipo - Deportiva
    When selecciona el filtro "Tipo de actividad"
    And elige la categoría "Deportiva"
    And hace clic en el botón "Filtrar"
    Then el sistema muestra únicamente las actividades de tipo "Deportiva"
    And cada actividad mostrada tiene el tipo "Deportiva"

  Scenario: Filtrar actividades por horario
    When ingresa el horario "10:00" en el filtro de tiempo
    And hace clic en el botón "Filtrar"
    Then el sistema muestra únicamente las actividades que tienen horarios que incluyen "10:00"
    And cada actividad mostrada tiene un horario que coincide con "10:00"

  Scenario: Filtrar actividades por tipo y lugar combinados
    When selecciona el filtro "Tipo de actividad"
    And elige la categoría "Deportiva"
    And ingresa el lugar "Coliseo 1" en el filtro de ubicación
    And hace clic en el botón "Filtrar"
    Then el sistema muestra únicamente las actividades de tipo "Deportiva" y ubicación "Coliseo 1"
    And cada actividad mostrada tiene el tipo "Deportiva"
    And cada actividad mostrada tiene "Coliseo 1" en su ubicación

  Scenario: Verificar que los filtros se muestran correctamente
    Then el usuario puede ver el selector de tipo de actividad
    And el usuario puede ver el campo de filtro por ubicación
    And el usuario puede ver el campo de filtro por horario
    And el usuario puede ver el botón "Filtrar"
    And el usuario puede ver el botón "Limpiar"

