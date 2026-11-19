# Importamos datetime para guardar la fecha y hora en que se crea cada reserva
from datetime import datetime
# Importamos Enum para definir los estados posibles de una reserva como constantes
from enum import Enum
# Importamos la clase abstracta Entidad (base) y la clase Cliente desde entidades.py
from entidades import Entidad, Cliente
# Importamos la clase abstracta Servicio desde servicios.py
from servicios import Servicio
# Importamos las excepciones personalizadas que se usan en este módulo
from excepciones import (
    ErrorValidacion,              # Error por datos inválidos
    ErrorServicioNoDisponible,    # Error cuando el servicio está ocupado
    ErrorReservaInvalida,         # Error cuando la reserva no se puede crear o confirmar
    ErrorOperacionNoPermitida,    # Error por transiciones de estado prohibidas
    ErrorCalculoInconsistente     # Error en el cálculo de costos
)


# Enumeración con los cuatro estados posibles de una reserva
class EstadoReserva(Enum):
    # Reserva creada pero aún no confirmada
    PENDIENTE = "PENDIENTE"
    # Reserva confirmada con costo calculado; el servicio queda ocupado
    CONFIRMADA = "CONFIRMADA"
    # Reserva ya atendida; el servicio vuelve a quedar libre
    PROCESADA = "PROCESADA"
    # Reserva cancelada
    CANCELADA = "CANCELADA"


# Clase Reserva: integra cliente, servicio, duración y estado; hereda de Entidad
class Reserva(Entidad):
    """
    Representa una reserva que vincula un Cliente y un Servicio
    con control estricto de estados y manejo avanzado de excepciones.
    """

    # Constructor: recibe el identificador, el cliente, el servicio y la duración en horas
    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio, duracion: float):
        # Llamamos al constructor de la clase padre (Entidad) para guardar el identificador
        super().__init__(identificador)
        # Atributo privado: cliente que hace la reserva
        self.__cliente = cliente
        # Atributo privado: servicio reservado
        self.__servicio = servicio
        # Atributo privado: duración de la reserva en horas
        self.__duracion = duracion
        # Toda reserva nace en estado PENDIENTE
        self.__estado = EstadoReserva.PENDIENTE
        # El costo total empieza en 0 y se calcula al confirmar
        self.__costo_total = 0.0
        # Guardamos la fecha y hora exactas de creación
        self.__fecha_creacion = datetime.now()
        # Validamos los datos apenas se crea la reserva; si algo está mal, lanza una excepción
        self.validar()

    # Propiedad de solo lectura para el cliente
    @property
    def cliente(self) -> Cliente:
        # Devuelve el cliente de la reserva
        return self.__cliente

    # Propiedad de solo lectura para el servicio
    @property
    def servicio(self) -> Servicio:
        # Devuelve el servicio de la reserva
        return self.__servicio

    # Propiedad de solo lectura para la duración
    @property
    def duracion(self) -> float:
        # Devuelve la duración en horas
        return self.__duracion

    # Propiedad de solo lectura para el estado
    @property
    def estado(self) -> EstadoReserva:
        # Devuelve el estado actual de la reserva
        return self.__estado

    # Propiedad de solo lectura para el costo total
    @property
    def costo_total(self) -> float:
        # Devuelve el costo calculado (0 si aún no se confirma)
        return self.__costo_total

    # Propiedad de solo lectura para la fecha de creación
    @property
    def fecha_creacion(self) -> datetime:
        # Devuelve la fecha y hora de creación
        return self.__fecha_creacion

    # Valida los datos de la reserva
    def validar(self) -> bool:
        # El cliente debe ser un objeto de la clase Cliente
        if not isinstance(self.__cliente, Cliente):
            # Error si no lo es
            raise ErrorValidacion("La reserva requiere una instancia válida de Cliente.")
        # El servicio debe ser un objeto de la clase Servicio (o de sus hijas)
        if not isinstance(self.__servicio, Servicio):
            # Error si no lo es
            raise ErrorValidacion("La reserva requiere una instancia válida de Servicio.")
        # La duración debe ser número (no booleano) y mayor a cero
        if not isinstance(self.__duracion, (int, float)) or isinstance(self.__duracion, bool) or self.__duracion <= 0:
            # Error si la duración es inválida
            raise ErrorValidacion("La duración de la reserva debe ser un número mayor a cero.")
        # Si pasó todas las validaciones, devuelve True
        return True

    # Confirma la reserva: calcula el costo y ocupa el servicio
    def confirmar(
        self,
        tasa_impuesto: float = 0.19,     # Impuesto (19 % por defecto)
        descuento: float = 0.0,          # Descuento opcional
        recargo_adicional: float = 0.0   # Recargo opcional
    ) -> float:
        """
        Confirma la reserva, calcula el costo total y bloquea el servicio.
        Demuestra try/except/else/finally y encadenamiento de excepciones.
        """
        # Solo se puede confirmar una reserva que esté PENDIENTE
        if self.__estado != EstadoReserva.PENDIENTE:
            # Si está en otro estado, la operación no está permitida
            raise ErrorOperacionNoPermitida(
                f"No se puede confirmar la reserva {self.identificador} en estado {self.__estado.value}."
            )

        # El servicio debe estar disponible para poder reservarlo
        if not self.__servicio.disponible:
            # Si está ocupado, lanzamos el error correspondiente
            raise ErrorServicioNoDisponible(
                f"El servicio '{self.__servicio.nombre}' no está disponible para reservar."
            )

        # Bandera que indica si el cálculo terminó bien; se usa en el bloque finally
        calculo_exitoso = False
        # Bloque try: el cálculo del costo puede lanzar errores
        try:
            # Calculamos el costo con el método del servicio (polimorfismo + parámetros opcionales)
            costo = self.__servicio.calcular_costo(
                duracion=self.__duracion,
                tasa_impuesto=tasa_impuesto,
                descuento=descuento,
                recargo_adicional=recargo_adicional
            )
        # Capturamos los errores de validación o de cálculo inconsistente
        except (ErrorValidacion, ErrorCalculoInconsistente) as error_calculo:
            # Encadenamiento de excepciones: lanzamos un error nuevo y conservamos el original con "from"
            raise ErrorReservaInvalida(
                f"Fallo al confirmar la reserva {self.identificador}: error en el cálculo de costos."
            ) from error_calculo
        # El bloque else se ejecuta SOLO si el try terminó sin errores
        else:
            # Guardamos el costo calculado
            self.__costo_total = costo
            # La reserva pasa a estado CONFIRMADA
            self.__estado = EstadoReserva.CONFIRMADA
            # Bloqueamos el servicio (queda no disponible mientras esté reservado)
            self.__servicio.cambiar_disponibilidad(False)
            # Marcamos que el cálculo fue exitoso
            calculo_exitoso = True
            # Devolvemos el costo total
            return self.__costo_total
        # El bloque finally se ejecuta SIEMPRE, haya habido error o no
        finally:
            # Si el cálculo falló y la reserva sigue PENDIENTE, dejamos el costo en 0 para evitar datos inconsistentes
            if not calculo_exitoso and self.__estado == EstadoReserva.PENDIENTE:
                self.__costo_total = 0.0

    # Marca una reserva confirmada como procesada
    def procesar(self) -> None:
        """Marca una reserva confirmada como procesada y libera el servicio."""
        # Solo se pueden procesar reservas CONFIRMADAS
        if self.__estado != EstadoReserva.CONFIRMADA:
            # Si está en otro estado, la operación no está permitida
            raise ErrorOperacionNoPermitida(
                f"Solo se pueden procesar reservas CONFIRMADAS (estado actual: {self.__estado.value})."
            )

        # La reserva pasa a estado PROCESADA
        self.__estado = EstadoReserva.PROCESADA
        # Liberamos el servicio para que pueda reservarse de nuevo
        self.__servicio.cambiar_disponibilidad(True)

    # Cancela la reserva si todavía es posible
    def cancelar(self) -> None:
        """Cancela la reserva si no ha sido procesada y libera el servicio si estaba ocupado."""
        # Una reserva ya procesada no se puede cancelar
        if self.__estado == EstadoReserva.PROCESADA:
            # Lanzamos el error de operación no permitida
            raise ErrorOperacionNoPermitida(
                f"No se puede cancelar la reserva {self.identificador} porque ya fue procesada."
            )
        # Una reserva ya cancelada no se puede cancelar otra vez
        if self.__estado == EstadoReserva.CANCELADA:
            # Lanzamos el error de operación no permitida
            raise ErrorOperacionNoPermitida(
                f"La reserva {self.identificador} ya se encuentra cancelada."
            )

        # Si estaba CONFIRMADA, el servicio estaba ocupado, así que lo liberamos
        if self.__estado == EstadoReserva.CONFIRMADA:
            self.__servicio.cambiar_disponibilidad(True)

        # La reserva pasa a estado CANCELADA
        self.__estado = EstadoReserva.CANCELADA

    # Representación en texto de la reserva (se usa al hacer print(reserva))
    def __str__(self) -> str:
        # Damos formato legible a la fecha de creación
        fecha = self.__fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        # Armamos la cadena con todos los datos principales de la reserva
        return (
            f"Reserva [{self.identificador}] | Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | Duración: {self.__duracion}h | "
            f"Estado: {self.__estado.value} | Total: ${self.__costo_total:,.2f} | Fecha: {fecha}"
        )
