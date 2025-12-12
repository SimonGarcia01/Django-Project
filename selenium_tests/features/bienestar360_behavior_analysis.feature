Feature: Análisis de comportamiento estudiantil
  Como analista de Bienestar Universitario
  Necesito registrar y segmentar la participación de los estudiantes según su frecuencia, tipo de actividad y variables demográficas
  Para poder identificar patrones de uso y segmentos de interés

  Background:
    Given que el usuario está autenticado como administrador de Bienestar Universitario

  Scenario: Generar reporte segmentado con filtros
    Given que soy analista de Bienestar Universitario
    And consulto los registros de participación en actividades
    When aplico filtros de frecuencia, tipo de actividad o alguna característica demográfica especifica
    Then el sistema genera un reporte segmentado con los patrones de comportamiento
    And permite exportar información para realizar más análisis

  Scenario: Generar reporte sin filtros
    Given que soy analista de Bienestar Universitario
    And consulto los registros de participación en actividades
    When no aplico ningún filtro
    Then el sistema genera un reporte con todos los datos de participación

