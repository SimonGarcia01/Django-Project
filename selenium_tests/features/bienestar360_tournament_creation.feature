Feature: Creación de torneos
  Como miembro de Bienestar Universitario
  Quiero crear torneos y partidos
  Para organizar los eventos deportivos

  Background:
    Given que el usuario está autenticado como administrador de Bienestar Universitario

  Scenario: Creación de torneo exitosa
    Given que el miembro de Bienestar planifica un torneo
    When registra la información del torneo en el sistema
    Then el torneo se crea exitosamente
    And el torneo aparece en la lista de torneos disponibles

  Scenario: Registro de partidos en un torneo
    Given que existe un torneo creado
    When el administrador registra las fechas y partidos del torneo
    Then los partidos se registran correctamente

