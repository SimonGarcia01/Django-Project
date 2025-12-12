Feature: Registrar resultados de torneos
  Como miembro de bienestar universitario
  Quiero registrar resultados de los torneos
  Para mantener la información actualizada

  Background:
    Given que el usuario está autenticado como administrador de Bienestar Universitario

  Scenario: Ingreso de resultados de torneo
    Given que un partido ha finalizado
    When el miembro de Bienestar registra el marcador
    Then el sistema actualiza los resultados en la base de datos
    And los refleja en la tabla de clasificación

