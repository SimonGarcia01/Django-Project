# features/social_project_inscription.feature
Feature: Inscripción a eventos de Proyecto Social
  Como usuario registrado
  Quiero poder inscribirme en eventos de proyecto social
  Para participar en actividades comunitarias

  Scenario: Inscribirse en un evento de proyecto social
    Given que he iniciado sesión en Bienestar360
    When accedo a la página principal de usuario
    And hago clic en el botón "Proyecto Social"
    And selecciono un evento disponible
    And me inscribo en el evento
    Then veo un mensaje de confirmación de inscripción
    And mi inscripción queda registrada en el sistema