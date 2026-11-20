from abc import ABC, abstractmethod
from datetime import datetime


class RegistradorEventos(ABC):
    """Interfaz abstracta para el registro de eventos y errores del sistema."""

    @abstractmethod
    def registrar_evento(self, mensaje: str) -> None:
        pass

    @abstractmethod
    def registrar_error(self, error: Exception, contexto: str = "") -> None:
        pass


class LoggerArchivo(RegistradorEventos):
    """
    Implementación concreta que persiste eventos y errores en un archivo de texto plano.
    No utiliza librerías externas ni bases de datos.
    """

    def __init__(self, ruta_archivo: str = "software_fj.log"):
        self.__ruta_archivo = ruta_archivo

    @property
    def ruta_archivo(self) -> str:
        return self.__ruta_archivo

    def _escribir_linea(self, nivel: str, mensaje: str) -> None:
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        linea = f"[{marca_tiempo}] [{nivel}] {mensaje}\n"
        try:
            with open(self.__ruta_archivo, mode="a", encoding="utf-8") as archivo:
                archivo.write(linea)
        except OSError as error_io:
            # Si falla el disco, se informa en consola sin detener la aplicación
            print(f"[ADVERTENCIA LOG] No se pudo escribir en '{self.__ruta_archivo}': {error_io}")

    def registrar_evento(self, mensaje: str) -> None:
        self._escribir_linea("INFO", mensaje)

    def registrar_error(self, error: Exception, contexto: str = "") -> None:
        tipo_error = type(error).__name__
        detalle = f"{contexto} -> {tipo_error}: {error}" if contexto else f"{tipo_error}: {error}"

        # Captura la causa original si hubo encadenamiento (raise ... from ...)
        if error.__cause__ is not None:
            causa = error.__cause__
            detalle += f" | Causa original: {type(causa).__name__}: {causa}"

        self._escribir_linea("ERROR", detalle)
