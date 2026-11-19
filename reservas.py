from datetime import datetime
from enum import Enum
from entidades import Entidad, Cliente
from servicios import Servicio
from excepciones import (
    ErrorValidacion,
    ErrorServicioNoDisponible,
    ErrorReservaInvalida,
    ErrorOperacionNoPermitida,
    ErrorCalculoInconsistente
)


class EstadoReserva(Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"


class Reserva(Entidad):
    """
    Representa una reserva que vincula un Cliente y un Servicio
    con control estricto de estados y manejo avanzado de excepciones.
    """

    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio, duracion: float):
        super().__init__(identificador)
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__estado = EstadoReserva.PENDIENTE
        self.__costo_total = 0.0
        self.__fecha_creacion = datetime.now()
        self.validar()

    @property
    def cliente(self) -> Cliente:
        return self.__cliente

    @property
    def servicio(self) -> Servicio:
        return self.__servicio

    @property
    def duracion(self) -> float:
        return self.__duracion

    @property
    def estado(self) -> EstadoReserva:
        return self.__estado

    @property
    def costo_total(self) -> float:
        return self.__costo_total

    @property
    def fecha_creacion(self) -> datetime:
        return self.__fecha_creacion

    def validar(self) -> bool:
        if not isinstance(self.__cliente, Cliente):
            raise ErrorValidacion("La reserva requiere una instancia válida de Cliente.")
        if not isinstance(self.__servicio, Servicio):
            raise ErrorValidacion("La reserva requiere una instancia válida de Servicio.")
        if not isinstance(self.__duracion, (int, float)) or isinstance(self.__duracion, bool) or self.__duracion <= 0:
            raise ErrorValidacion("La duración de la reserva debe ser un número mayor a cero.")
        return True

    def confirmar(
        self,
        tasa_impuesto: float = 0.19,
        descuento: float = 0.0,
        recargo_adicional: float = 0.0
    ) -> float:
        """
        Confirma la reserva, calcula el costo total y bloquea el servicio.
        Demuestra try/except/else/finally y encadenamiento de excepciones.
        """
        if self.__estado != EstadoReserva.PENDIENTE:
            raise ErrorOperacionNoPermitida(
                f"No se puede confirmar la reserva {self.identificador} en estado {self.__estado.value}."
            )

        if not self.__servicio.disponible:
            raise ErrorServicioNoDisponible(
                f"El servicio '{self.__servicio.nombre}' no está disponible para reservar."
            )

        calculo_exitoso = False
        try:
            costo = self.__servicio.calcular_costo(
                duracion=self.__duracion,
                tasa_impuesto=tasa_impuesto,
                descuento=descuento,
                recargo_adicional=recargo_adicional
            )
        except (ErrorValidacion, ErrorCalculoInconsistente) as error_calculo:
            raise ErrorReservaInvalida(
                f"Fallo al confirmar la reserva {self.identificador}: error en el cálculo de costos."
            ) from error_calculo
        else:
            self.__costo_total = costo
            self.__estado = EstadoReserva.CONFIRMADA
            self.__servicio.cambiar_disponibilidad(False)
            calculo_exitoso = True
            return self.__costo_total
        finally:
            if not calculo_exitoso and self.__estado == EstadoReserva.PENDIENTE:
                self.__costo_total = 0.0

    def procesar(self) -> None:
        """Marca una reserva confirmada como procesada y libera el servicio."""
        if self.__estado != EstadoReserva.CONFIRMADA:
            raise ErrorOperacionNoPermitida(
                f"Solo se pueden procesar reservas CONFIRMADAS (estado actual: {self.__estado.value})."
            )

        self.__estado = EstadoReserva.PROCESADA
        self.__servicio.cambiar_disponibilidad(True)

    def cancelar(self) -> None:
        """Cancela la reserva si no ha sido procesada y libera el servicio si estaba ocupado."""
        if self.__estado == EstadoReserva.PROCESADA:
            raise ErrorOperacionNoPermitida(
                f"No se puede cancelar la reserva {self.identificador} porque ya fue procesada."
            )
        if self.__estado == EstadoReserva.CANCELADA:
            raise ErrorOperacionNoPermitida(
                f"La reserva {self.identificador} ya se encuentra cancelada."
            )

        if self.__estado == EstadoReserva.CONFIRMADA:
            self.__servicio.cambiar_disponibilidad(True)

        self.__estado = EstadoReserva.CANCELADA

    def __str__(self) -> str:
        fecha = self.__fecha_creacion.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"Reserva [{self.identificador}] | Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | Duración: {self.__duracion}h | "
            f"Estado: {self.__estado.value} | Total: ${self.__costo_total:,.2f} | Fecha: {fecha}"
        )