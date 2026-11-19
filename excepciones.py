class ErrorSoftwareFJ(Exception):
    """Excepción base para todos los errores del sistema Software FJ."""


class ErrorValidacion(ErrorSoftwareFJ):
    """Se lanza cuando un dato o parámetro no cumple las reglas de validación."""


class ErrorServicioNoDisponible(ErrorSoftwareFJ):
    """Se lanza al intentar reservar un servicio que no está disponible."""


class ErrorReservaInvalida(ErrorSoftwareFJ):
    """Se lanza cuando una reserva no puede crearse o confirmarse."""


class ErrorOperacionNoPermitida(ErrorSoftwareFJ):
    """Se lanza al intentar una transición de estado o acción prohibida."""


class ErrorCalculoInconsistente(ErrorSoftwareFJ):
    """Se lanza cuando el cálculo de costos produce resultados inválidos."""
