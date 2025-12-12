Feature: Inicio de sesión
  Como usuario de la aplicación
  Quiero poder ingresar mi usuario y contraseña
  Para poder observar la información que me compete en la aplicación con mis privilegios asociados

  Scenario: Inicio exitoso con credenciales válidas (usuario básico)
    Given el usuario está en la pantalla de inicio de sesión
    And ha ingresado un nombre de usuario válido "basicuser"
    And ha ingresado una contraseña válida "password123"
    When presiona el botón "Iniciar sesión"
    Then accede a la aplicación
    And puede ver la información que le corresponde
    And sus privilegios están correctamente aplicados

  Scenario: Inicio exitoso con credenciales válidas (administrador)
    Given el usuario está en la pantalla de inicio de sesión
    And ha ingresado un nombre de usuario válido "adminuser"
    And ha ingresado una contraseña válida "adminpass"
    When presiona el botón "Iniciar sesión"
    Then accede a la aplicación
    And puede ver la información que le corresponde (administrador)
    And sus privilegios están correctamente aplicados (administrador)

  Scenario: Inicio de sesión fallido con credenciales inválidas
    Given el usuario está en la pantalla de inicio de sesión
    And ha ingresado un nombre de usuario inválido "usuario_inexistente"
    And ha ingresado una contraseña inválida "contraseña_incorrecta"
    When presiona el botón "Iniciar sesión"
    Then se muestra un mensaje de error
    And el usuario permanece en la pantalla de inicio de sesión

  Scenario: Inicio de sesión con campos vacíos
    Given el usuario está en la pantalla de inicio de sesión
    And no ha ingresado nombre de usuario
    And no ha ingresado contraseña
    When presiona el botón "Iniciar sesión"
    Then se muestra un mensaje de error o validación
    And el usuario permanece en la pantalla de inicio de sesión
