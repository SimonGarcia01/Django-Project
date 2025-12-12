Feature: Actualizar actividades sin inscripción
  Como personal del equipo CADI
  Quiero actualizar las actividades artísticas y deportivas que no requieren inscripción
  Para que los estudiantes interesados puedan ver y asistir a las de su agrado

  Scenario: Modificar información de una actividad existente
    Given que el personal del equipo CADI ha accedido al panel de administración
    And ha buscado una actividad previamente registrada
    When actualiza la información de la actividad
    And guarda los cambios
    Then la información actualizada se refleja inmediatamente en el portal estudiantil y en la misma vista de administrador

  Scenario: Intentar actualizar actividad con datos inválidos
    Given que el personal del equipo CADI ha accedido al panel de administración
    And ha buscado una actividad previamente registrada
    When intenta actualizar la actividad marcando "requiere inscripción" sin definir cupo máximo
    And intenta guardar los cambios
    Then el sistema muestra un mensaje de error indicando que el cupo máximo es requerido
    And la actividad no se actualiza

