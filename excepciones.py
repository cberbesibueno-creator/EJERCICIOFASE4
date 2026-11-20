"""
Módulo de excepciones personalizadas de Software FJ.

Todas las excepciones del sistema heredan de SoftwareFJError, de modo que
con un solo "except SoftwareFJError" se puede capturar cualquier error propio
de la aplicación, sin atrapar errores ajenos (por ejemplo, de Python).
"""


class SoftwareFJError(Exception):
    """Excepción base de todo el sistema Software FJ."""


class DatosInvalidosError(SoftwareFJError, ValueError):
    """Datos inválidos, vacíos, de tipo incorrecto o parámetros faltantes.

    También hereda de ValueError para que el código que ya capturaba
    ValueError (por ejemplo, los archivos de pruebas) siga funcionando.
    """


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible en este momento."""


class OperacionNoPermitidaError(SoftwareFJError, ValueError):
    """Operación no permitida para el estado actual (ej.: procesar sin confirmar)."""


class CalculoInconsistenteError(SoftwareFJError):
    """El cálculo de costos produjo un resultado inconsistente (cero, negativo, infinito)."""


class ReservaError(SoftwareFJError):
    """Una reserva no pudo completarse.

    Se usa para ENCADENAR excepciones: envuelve el error original
    mediante 'raise ReservaError(...) from error_original'.
    """
