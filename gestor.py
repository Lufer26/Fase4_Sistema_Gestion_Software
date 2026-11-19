from typing import List, Optional
from entidades import Cliente
from servicios import Servicio
from reservas import Reserva
from logger import RegistradorEventos
from excepciones import (
    ErrorSoftwareFJ,
    ErrorValidacion,
    ErrorOperacionNoPermitida
)


class SistemaSoftwareFJ:
    """
    Orquestador principal del sistema.
    Administra colecciones en memoria y delega el registro de eventos al logger inyectado.
    """

    def __init__(self, registrador: RegistradorEventos):
        self.__registrador = registrador
        self.__clientes: List[Cliente] = []
        self.__servicios: List[Servicio] = []
        self.__reservas: List[Reserva] = []
        self.__registrador.registrar_evento("Sistema Software FJ inicializado correctamente.")

    @property
    def clientes(self) -> List[Cliente]:
        return list(self.__clientes)

    @property
    def servicios(self) -> List[Servicio]:
        return list(self.__servicios)

    @property
    def reservas(self) -> List[Reserva]:
        return list(self.__reservas)

    # --- Búsquedas internas ---

    def buscar_cliente(self, identificador: str) -> Optional[Cliente]:
        for cliente in self.__clientes:
            if cliente.identificador == identificador:
                return cliente
        return None

    def buscar_servicio(self, identificador: str) -> Optional[Servicio]:
        for servicio in self.__servicios:
            if servicio.identificador == identificador:
                return servicio
        return None

    def buscar_reserva(self, identificador: str) -> Optional[Reserva]:
        for reserva in self.__reservas:
            if reserva.identificador == identificador:
                return reserva
        return None

    # --- Gestión de Clientes ---

    def registrar_cliente(
        self,
        identificador: str,
        nombre: str,
        documento: str,
        correo: str,
        telefono: str
    ) -> Optional[Cliente]:
        """Crea y registra un cliente controlando excepciones de entidades.py."""
        try:
            if self.buscar_cliente(str(identificador).strip()) is not None:
                raise ErrorOperacionNoPermitida(
                    f"Ya existe un cliente con el identificador '{identificador}'."
                )

            try:
                cliente = Cliente(identificador, nombre, documento, correo, telefono)
            except (ValueError, TypeError) as error_nativo:
                raise ErrorValidacion(
                    f"Datos inválidos al registrar el cliente '{identificador}'."
                ) from error_nativo

        except ErrorSoftwareFJ as error:
            self.__registrador.registrar_error(error, contexto="Registro de cliente")
            print(f"[ERROR] {error}")
            return None
        else:
            self.__clientes.append(cliente)
            self.__registrador.registrar_evento(
                f"Cliente registrado: [{cliente.identificador}] {cliente.nombre}"
            )
            return cliente

    # --- Gestión de Servicios ---

    def registrar_servicio(self, servicio: Servicio) -> bool:
        """Registra una instancia válida de cualquier subclase de Servicio (Polimorfismo / OCP)."""
        try:
            if not isinstance(servicio, Servicio):
                raise ErrorValidacion("El objeto proporcionado no es una instancia válida de Servicio.")

            if self.buscar_servicio(servicio.identificador) is not None:
                raise ErrorOperacionNoPermitida(
                    f"Ya existe un servicio con el identificador '{servicio.identificador}'."
                )
        except ErrorSoftwareFJ as error:
            self.__registrador.registrar_error(error, contexto="Registro de servicio")
            print(f"[ERROR] {error}")
            return False
        else:
            self.__servicios.append(servicio)
            self.__registrador.registrar_evento(
                f"Servicio registrado: [{servicio.identificador}] {servicio.describir()}"
            )
            return True

    def registrar_error_externo(self, error: Exception, contexto: str) -> None:
        """Permite registrar en el log errores ocurridos al instanciar servicios antes de agregarlos."""
        self.__registrador.registrar_error(error, contexto=contexto)
        print(f"[ERROR] {contexto}: {error}")

    # --- Gestión de Reservas ---

    def crear_reserva(
        self,
        identificador: str,
        id_cliente: str,
        id_servicio: str,
        duracion: float
    ) -> Optional[Reserva]:
        """Crea una reserva en estado PENDIENTE validando existencia de cliente y servicio."""
        try:
            if self.buscar_reserva(str(identificador).strip()) is not None:
                raise ErrorOperacionNoPermitida(
                    f"Ya existe una reserva con el identificador '{identificador}'."
                )

            cliente = self.buscar_cliente(id_cliente)
            if cliente is None:
                raise ErrorValidacion(f"No se encontró el cliente con ID '{id_cliente}'.")

            servicio = self.buscar_servicio(id_servicio)
            if servicio is None:
                raise ErrorValidacion(f"No se encontró el servicio con ID '{id_servicio}'.")

            reserva = Reserva(identificador, cliente, servicio, duracion)
        except ErrorSoftwareFJ as error:
            self.__registrador.registrar_error(error, contexto="Creación de reserva")
            print(f"[ERROR] {error}")
            return None
        else:
            self.__reservas.append(reserva)
            self.__registrador.registrar_evento(
                f"Reserva creada: [{reserva.identificador}] Cliente={cliente.identificador}, "
                f"Servicio={servicio.identificador}, Duración={duracion}h"
            )
            return reserva

    def confirmar_reserva(
        self,
        id_reserva: str,
        tasa_impuesto: float = 0.19,
        descuento: float = 0.0,
        recargo_adicional: float = 0.0
    ) -> Optional[float]:
        """Confirma una reserva y calcula su costo total."""
        try:
            reserva = self.buscar_reserva(id_reserva)
            if reserva is None:
                raise ErrorValidacion(f"No existe la reserva con ID '{id_reserva}'.")

            total = reserva.confirmar(
                tasa_impuesto=tasa_impuesto,
                descuento=descuento,
                recargo_adicional=recargo_adicional
            )
        except ErrorSoftwareFJ as error:
            self.__registrador.registrar_error(error, contexto=f"Confirmación de reserva '{id_reserva}'")
            print(f"[ERROR] {error}")
            return None
        else:
            self.__registrador.registrar_evento(
                f"Reserva confirmada: [{reserva.identificador}] Total=${total:,.2f}"
            )
            return total

    def procesar_reserva(self, id_reserva: str) -> bool:
        """Procesa una reserva confirmada y libera el servicio."""
        try:
            reserva = self.buscar_reserva(id_reserva)
            if reserva is None:
                raise ErrorValidacion(f"No existe la reserva con ID '{id_reserva}'.")

            reserva.procesar()
        except ErrorSoftwareFJ as error:
            self.__registrador.registrar_error(error, contexto=f"Procesamiento de reserva '{id_reserva}'")
            print(f"[ERROR] {error}")
            return False
        else:
            self.__registrador.registrar_evento(f"Reserva procesada: [{reserva.identificador}]")
            return True

    def cancelar_reserva(self, id_reserva: str) -> bool:
        """Cancela una reserva si su estado lo permite."""
        try:
            reserva = self.buscar_reserva(id_reserva)
            if reserva is None:
                raise ErrorValidacion(f"No existe la reserva con ID '{id_reserva}'.")

            reserva.cancelar()
        except ErrorSoftwareFJ as error:
            self.__registrador.registrar_error(error, contexto=f"Cancelación de reserva '{id_reserva}'")
            print(f"[ERROR] {error}")
            return False
        else:
            self.__registrador.registrar_evento(f"Reserva cancelada: [{reserva.identificador}]")
            return True