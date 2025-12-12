Feature: Recolección de retroalimentación de actividades
  Como miembro del centro CADI
  Quiero recolectar retroalimentación de las actividades, mediante valoraciones y comentarios
  Para conocer la opinión de los estudiantes y llevar a cabo mejoras

  Scenario: Estudiante envía valoración y comentario
    Given que la actividad ya ha finalizado
    And el estudiante participó en la actividad
    When el estudiante envía una valoración numérica del 1 a 5 y un comentario
    Then el sistema almacena la valoración y comentario
    And el miembro del centro CADI puede visualizar la retroalimentación en un reporte

  Scenario: Estudiante regular intenta acceder a la vista CADI de retroalimentación
    Given que un estudiante regular ha iniciado sesión
    When intenta acceder a la página de retroalimentaciones del CADI
    Then el sistema no le permite acceder o muestra un mensaje de acceso denegado
    And no puede visualizar las retroalimentaciones del CADI

