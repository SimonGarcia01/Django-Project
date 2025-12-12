Feature: Enviar retroalimentación sobre actividades
  Como estudiante universitario
  Quiero poder enviar retroalimentación sobre las actividades del CADI
  Para compartir mi opinión y ayudar a mejorar las futuras actividades según las necesidades de los estudiantes

  Scenario: Estudiante envía comentario y valoración sobre una actividad
    Given que el estudiante ha asistido a una actividad del CADI
    When accede a la opción "Enviar retroalimentación" en el sistema
    Then el sistema le permite registrar un comentario y una valoración sobre la actividad
    And la retroalimentación queda asociada a la actividad correspondiente para que el equipo CADI pueda revisarla

  Scenario: Intentar enviar retroalimentación sin completar campos requeridos
    Given que el estudiante ha asistido a una actividad del CADI
    When accede a la opción "Enviar retroalimentación" en el sistema
    And intenta enviar la retroalimentación sin completar los campos requeridos
    Then el sistema muestra un mensaje de error indicando que los campos son requeridos
    And la retroalimentación no se envía

