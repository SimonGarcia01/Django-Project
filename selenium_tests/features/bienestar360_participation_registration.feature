Feature: Registro de participación
  Como miembro de bienestar universitario, quiero almacenar información de participación, para generar reportes más adelante.

  Scenario: Almacenar participación del estudiante
    Given que el usuario está autenticado como administrador de Bienestar Universitario
    And que existen registros de participación en actividades
    When el sistema consulta la segmentación de participación
    Then la información de participación queda almacenada en la base de datos
    And está disponible para reportes posteriores

