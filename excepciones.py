# Clase base de todas las excepciones del proyecto; hereda de Exception (la clase de errores de Python)
class ErrorSoftwareFJ(Exception):
    """Excepción base para todos los errores del sistema Software FJ."""
    # No necesita código adicional: su función es agrupar todos los errores propios del sistema.
    # Gracias a ella se puede capturar cualquier error del sistema con un solo "except ErrorSoftwareFJ".


# Excepción para datos inválidos; hereda de ErrorSoftwareFJ
class ErrorValidacion(ErrorSoftwareFJ):
    """Se lanza cuando un dato o parámetro no cumple las reglas de validación."""
    # Ejemplo: un nombre muy corto, un correo mal escrito o una tarifa negativa.


# Excepción para servicios que no se pueden reservar; hereda de ErrorSoftwareFJ
class ErrorServicioNoDisponible(ErrorSoftwareFJ):
    """Se lanza al intentar reservar un servicio que no está disponible."""
    # Ejemplo: reservar una sala que está marcada como no disponible.


# Excepción para reservas incorrectas; hereda de ErrorSoftwareFJ
class ErrorReservaInvalida(ErrorSoftwareFJ):
    """Se lanza cuando una reserva no puede crearse o confirmarse."""
    # Ejemplo: crear una reserva sin cliente o con una duración inválida.


# Excepción para acciones no permitidas; hereda de ErrorSoftwareFJ
class ErrorOperacionNoPermitida(ErrorSoftwareFJ):
    """Se lanza al intentar una transición de estado o acción prohibida."""
    # Ejemplo: confirmar una reserva que ya fue cancelada.


# Excepción para cálculos de costos erróneos; hereda de ErrorSoftwareFJ
class ErrorCalculoInconsistente(ErrorSoftwareFJ):
    """Se lanza cuando el cálculo de costos produce resultados inválidos."""
    # Ejemplo: un descuento mayor al 100 % o un total negativo.
