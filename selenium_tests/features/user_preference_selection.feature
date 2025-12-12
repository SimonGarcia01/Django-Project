# features/user_preference_selection.feature
Feature: Ver funcionalidad de alertas personalizadas
  Como usuario registrado
  Quiero acceder a las alertas personalizadas
  Para ver la opción Grupal

  Scenario: Ver card Grupal en alertas personalizadas
    Given que he iniciado sesión en Bienestar360
    When accedo a la página principal de usuario
    And navego a la página de alertas personalizadas
    Then veo una card con el texto "Grupal"