Feature: Eliminar actividades sin inscripción
  Como personal del equipo CADI
  Quiero eliminar las actividades artísticas y deportivas que no requieren inscripción
  Para que los estudiantes ya no puedan ver la actividad eliminada

  Scenario: Eliminar una actividad existente
    Given que el personal del equipo CADI ha accedido al panel de administración
    And ha buscado una actividad previamente registrada
    When selecciona la opción de eliminar la actividad
    And confirma la eliminación
    Then la actividad deja de aparecer en el portal estudiantil y en la vista de administrador

  Scenario: Cancelar la eliminación de una actividad
    Given que el personal del equipo CADI ha accedido al panel de administración
    And ha buscado una actividad previamente registrada
    When selecciona la opción de eliminar la actividad
    And cancela la eliminación
    Then la actividad sigue apareciendo en el portal estudiantil y en la vista de administrador

