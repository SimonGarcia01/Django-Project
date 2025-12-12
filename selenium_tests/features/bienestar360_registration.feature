Feature: Creación de un usuario
  Como estudiante, profesor y egresado de la universidad Icesi
  Quiero poder registrarme dentro de la aplicación usando mi cédula y el resto de información necesaria
  Para poder acceder a los servicios de bienestar universitario

  Scenario: Se crea un usuario exitósamente
    Given Un usuario este en la página de registro
    And ha ingresado la información necesaria para crear un usuario
    And no tenía una cuenta registrada antes
    When presiona "Crear Usuario"
    Then el sistema registra el usuario
    And le muestra mensaje de éxito

  Scenario: Intento de registro con usuario existente
    Given Un usuario este en la página de registro
    And intenta registrarse con un nombre de usuario que ya existe "basicuser"
    When presiona "Crear Usuario"
    Then el sistema muestra un mensaje de error indicando que el usuario ya existe
    And el usuario permanece en la página de registro

  Scenario: Intento de registro con campos incompletos
    Given Un usuario este en la página de registro
    And ha ingresado información incompleta para crear un usuario
    When presiona "Crear Usuario"
    Then el sistema muestra mensajes de error para los campos requeridos
    And el usuario permanece en la página de registro

  Scenario: Intento de registro con contraseñas que no coinciden
    Given Un usuario este en la página de registro
    And ha ingresado información válida pero con contraseñas que no coinciden
    When presiona "Crear Usuario"
    Then el sistema muestra un mensaje de error indicando que las contraseñas no coinciden
    And el usuario permanece en la página de registro

