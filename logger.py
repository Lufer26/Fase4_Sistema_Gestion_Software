# Importamos ABC (clase base abstracta) y abstractmethod (para declarar métodos obligatorios en las hijas)
from abc import ABC, abstractmethod
# Importamos datetime para obtener la fecha y hora actual y ponerla en cada registro del log
from datetime import datetime


# Clase abstracta que define QUÉ debe poder hacer un registrador (sin decir cómo)
class RegistradorEventos(ABC):
    """Interfaz abstracta para el registro de eventos y errores del sistema."""

    # Método abstracto: toda clase hija debe saber registrar un evento informativo
    @abstractmethod
    def registrar_evento(self, mensaje: str) -> None:
        # 'pass' porque aquí no hay lógica; la implementan las clases hijas
        pass

    # Método abstracto: toda clase hija debe saber registrar un error (con un contexto opcional)
    @abstractmethod
    def registrar_error(self, error: Exception, contexto: str = "") -> None:
        # Sin lógica aquí; la implementan las clases hijas
        pass


# Clase concreta que implementa el registrador guardando todo en un archivo de texto
class LoggerArchivo(RegistradorEventos):
    """
    Implementación concreta que persiste eventos y errores en un archivo de texto plano.
    No utiliza librerías externas ni bases de datos.
    """

    # Constructor: recibe la ruta del archivo de logs (por defecto "software_fj.log")
    def __init__(self, ruta_archivo: str = "software_fj.log"):
        # Guardamos la ruta en un atributo privado (encapsulación)
        self.__ruta_archivo = ruta_archivo

    # Propiedad de solo lectura para consultar la ruta del archivo
    @property
    def ruta_archivo(self) -> str:
        # Devuelve la ruta privada del archivo de logs
        return self.__ruta_archivo

    # Método interno (el guion bajo indica uso interno) que escribe una línea en el archivo
    def _escribir_linea(self, nivel: str, mensaje: str) -> None:
        # Obtenemos la fecha y hora actual con formato año-mes-día hora:minuto:segundo
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Armamos la línea final: [fecha] [nivel] mensaje, terminada con salto de línea
        linea = f"[{marca_tiempo}] [{nivel}] {mensaje}\n"
        # Bloque try: el acceso al archivo puede fallar (sin permisos, disco lleno, etc.)
        try:
            # Abrimos el archivo en modo "a" (append): agrega al final sin borrar lo anterior
            with open(self.__ruta_archivo, mode="a", encoding="utf-8") as archivo:
                # Escribimos la línea en el archivo; 'with' lo cierra automáticamente al terminar
                archivo.write(linea)
        # Si ocurre un error de entrada/salida (OSError), lo capturamos
        except OSError as error_io:
            # Si falla el disco, se informa en consola sin detener la aplicación
            print(f"[ADVERTENCIA LOG] No se pudo escribir en '{self.__ruta_archivo}': {error_io}")

    # Implementa el método abstracto: registra un evento informativo
    def registrar_evento(self, mensaje: str) -> None:
        # Escribe la línea con el nivel "INFO"
        self._escribir_linea("INFO", mensaje)

    # Implementa el método abstracto: registra un error con su contexto
    def registrar_error(self, error: Exception, contexto: str = "") -> None:
        # Obtenemos el nombre de la clase del error (por ejemplo, ErrorValidacion)
        tipo_error = type(error).__name__
        # Si hay contexto, lo incluimos antes del error; si no, solo el tipo y el mensaje
        detalle = f"{contexto} -> {tipo_error}: {error}" if contexto else f"{tipo_error}: {error}"

        # Captura la causa original si hubo encadenamiento (raise ... from ...)
        # __cause__ guarda el error original cuando se usó "raise ... from ..."
        if error.__cause__ is not None:
            # Guardamos la causa original en una variable
            causa = error.__cause__
            # La agregamos al detalle para que el log muestre ambos errores
            detalle += f" | Causa original: {type(causa).__name__}: {causa}"

        # Escribimos la línea en el archivo con el nivel "ERROR"
        self._escribir_linea("ERROR", detalle)
