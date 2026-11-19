# Importamos tipos para indicar qué contienen las listas (List) y valores que pueden ser None (Optional)
from typing import List, Optional
# Importamos la clase Cliente (definida en entidades.py)
from entidades import Cliente
# Importamos la clase abstracta Servicio (definida en servicios.py)
from servicios import Servicio
# Importamos la clase Reserva (definida en reservas.py)
from reservas import Reserva
# Importamos el registrador de eventos y errores (definido en logger.py)
from logger import RegistradorEventos
# Importamos las excepciones personalizadas que se usan en este módulo
from excepciones import (
    ErrorSoftwareFJ,            # Excepción base de todos los errores del sistema
    ErrorValidacion,            # Error por datos inválidos
    ErrorOperacionNoPermitida   # Error por acciones no permitidas
)


# Clase principal que coordina clientes, servicios y reservas
class SistemaSoftwareFJ:
    """
    Orquestador principal del sistema.
    Administra colecciones en memoria y delega el registro de eventos al logger inyectado.
    """

    # Constructor: recibe el registrador de eventos desde afuera (inyección de dependencias)
    def __init__(self, registrador: RegistradorEventos):
        # Guardamos el registrador como atributo privado
        self.__registrador = registrador
        # Lista privada en memoria donde se guardan los clientes (sin base de datos)
        self.__clientes: List[Cliente] = []
        # Lista privada en memoria donde se guardan los servicios
        self.__servicios: List[Servicio] = []
        # Lista privada en memoria donde se guardan las reservas
        self.__reservas: List[Reserva] = []
        # Dejamos constancia en el log de que el sistema inició bien
        self.__registrador.registrar_evento("Sistema Software FJ inicializado correctamente.")

    # Propiedad de solo lectura para consultar los clientes
    @property
    def clientes(self) -> List[Cliente]:
        # Devolvemos una COPIA de la lista para que no la puedan modificar desde afuera (encapsulación)
        return list(self.__clientes)

    # Propiedad de solo lectura para consultar los servicios
    @property
    def servicios(self) -> List[Servicio]:
        # Devolvemos una copia de la lista de servicios
        return list(self.__servicios)

    # Propiedad de solo lectura para consultar las reservas
    @property
    def reservas(self) -> List[Reserva]:
        # Devolvemos una copia de la lista de reservas
        return list(self.__reservas)

    # --- Búsquedas internas ---

    # Busca un cliente por su identificador
    def buscar_cliente(self, identificador: str) -> Optional[Cliente]:
        # Recorremos todos los clientes registrados
        for cliente in self.__clientes:
            # Si el identificador coincide, devolvemos ese cliente
            if cliente.identificador == identificador:
                return cliente
        # Si no se encontró ninguno, devolvemos None
        return None

    # Busca un servicio por su identificador
    def buscar_servicio(self, identificador: str) -> Optional[Servicio]:
        # Recorremos todos los servicios registrados
        for servicio in self.__servicios:
            # Si el identificador coincide, devolvemos ese servicio
            if servicio.identificador == identificador:
                return servicio
        # Si no se encontró ninguno, devolvemos None
        return None

    # Busca una reserva por su identificador
    def buscar_reserva(self, identificador: str) -> Optional[Reserva]:
        # Recorremos todas las reservas registradas
        for reserva in self.__reservas:
            # Si el identificador coincide, devolvemos esa reserva
            if reserva.identificador == identificador:
                return reserva
        # Si no se encontró ninguna, devolvemos None
        return None

    # --- Gestión de Clientes ---

    # Crea y registra un cliente nuevo
    def registrar_cliente(
        self,
        identificador: str,  # Código único del cliente
        nombre: str,         # Nombre completo
        documento: str,      # Número de documento
        correo: str,         # Correo electrónico
        telefono: str        # Número de teléfono
    ) -> Optional[Cliente]:
        """Crea y registra un cliente controlando excepciones de entidades.py."""
        # Bloque try externo: captura los errores propios del sistema
        try:
            # Verificamos que no exista ya un cliente con ese identificador
            if self.buscar_cliente(str(identificador).strip()) is not None:
                # Si existe, lanzamos error de operación no permitida
                raise ErrorOperacionNoPermitida(
                    f"Ya existe un cliente con el identificador '{identificador}'."
                )

            # Bloque try interno: captura errores nativos de Python al crear el cliente
            try:
                # Intentamos crear el objeto Cliente (aquí se validan los datos)
                cliente = Cliente(identificador, nombre, documento, correo, telefono)
            # Si Cliente lanza ValueError o TypeError, los capturamos
            except (ValueError, TypeError) as error_nativo:
                # Encadenamiento de excepciones: lanzamos nuestro error y conservamos el original con "from"
                raise ErrorValidacion(
                    f"Datos inválidos al registrar el cliente '{identificador}'."
                ) from error_nativo

        # Si ocurrió cualquier error propio del sistema, lo manejamos aquí
        except ErrorSoftwareFJ as error:
            # Guardamos el error en el archivo de logs, indicando en qué operación ocurrió
            self.__registrador.registrar_error(error, contexto="Registro de cliente")
            # Mostramos el error en pantalla
            print(f"[ERROR] {error}")
            # Devolvemos None para indicar que no se pudo registrar; el programa sigue funcionando
            return None
        # El bloque else se ejecuta SOLO si no hubo ningún error
        else:
            # Agregamos el cliente a la lista en memoria
            self.__clientes.append(cliente)
            # Registramos en el log que el cliente fue creado con éxito
            self.__registrador.registrar_evento(
                f"Cliente registrado: [{cliente.identificador}] {cliente.nombre}"
            )
            # Devolvemos el cliente creado
            return cliente

    # --- Gestión de Servicios ---

    # Registra un servicio ya creado (sala, equipo o asesoría)
    def registrar_servicio(self, servicio: Servicio) -> bool:
        """Registra una instancia válida de cualquier subclase de Servicio (Polimorfismo / OCP)."""
        # Bloque try: captura los errores propios del sistema
        try:
            # Verificamos que el objeto recibido sea realmente un Servicio (o una subclase)
            if not isinstance(servicio, Servicio):
                # Si no lo es, lanzamos error de validación
                raise ErrorValidacion("El objeto proporcionado no es una instancia válida de Servicio.")

            # Verificamos que no exista ya un servicio con ese identificador
            if self.buscar_servicio(servicio.identificador) is not None:
                # Si existe, lanzamos error de operación no permitida
                raise ErrorOperacionNoPermitida(
                    f"Ya existe un servicio con el identificador '{servicio.identificador}'."
                )
        # Si ocurrió un error propio del sistema, lo manejamos aquí
        except ErrorSoftwareFJ as error:
            # Guardamos el error en el log con su contexto
            self.__registrador.registrar_error(error, contexto="Registro de servicio")
            # Mostramos el error en pantalla
            print(f"[ERROR] {error}")
            # Devolvemos False: no se pudo registrar
            return False
        # Se ejecuta solo si no hubo errores
        else:
            # Agregamos el servicio a la lista en memoria
            self.__servicios.append(servicio)
            # Registramos el evento; describir() es polimórfico: cada servicio se describe a su manera
            self.__registrador.registrar_evento(
                f"Servicio registrado: [{servicio.identificador}] {servicio.describir()}"
            )
            # Devolvemos True: registro exitoso
            return True

    # Permite registrar en el log errores ocurridos fuera del gestor (por ejemplo, al crear un servicio inválido)
    def registrar_error_externo(self, error: Exception, contexto: str) -> None:
        """Permite registrar en el log errores ocurridos al instanciar servicios antes de agregarlos."""
        # Guardamos el error en el archivo de logs
        self.__registrador.registrar_error(error, contexto=contexto)
        # Mostramos el error en pantalla con su contexto
        print(f"[ERROR] {contexto}: {error}")

    # --- Gestión de Reservas ---

    # Crea una reserva nueva en estado PENDIENTE
    def crear_reserva(
        self,
        identificador: str,  # Código único de la reserva
        id_cliente: str,     # Identificador del cliente que reserva
        id_servicio: str,    # Identificador del servicio reservado
        duracion: float      # Duración de la reserva en horas
    ) -> Optional[Reserva]:
        """Crea una reserva en estado PENDIENTE validando existencia de cliente y servicio."""
        # Bloque try: captura los errores propios del sistema
        try:
            # Verificamos que no exista ya una reserva con ese identificador
            if self.buscar_reserva(str(identificador).strip()) is not None:
                # Si existe, lanzamos error de operación no permitida
                raise ErrorOperacionNoPermitida(
                    f"Ya existe una reserva con el identificador '{identificador}'."
                )

            # Buscamos el cliente indicado
            cliente = self.buscar_cliente(id_cliente)
            # Si no existe, no se puede reservar
            if cliente is None:
                # Lanzamos error de validación
                raise ErrorValidacion(f"No se encontró el cliente con ID '{id_cliente}'.")

            # Buscamos el servicio indicado
            servicio = self.buscar_servicio(id_servicio)
            # Si no existe, no se puede reservar
            if servicio is None:
                # Lanzamos error de validación
                raise ErrorValidacion(f"No se encontró el servicio con ID '{id_servicio}'.")

            # Creamos la reserva integrando cliente, servicio y duración (aquí se validan sus reglas)
            reserva = Reserva(identificador, cliente, servicio, duracion)
        # Si ocurrió un error propio del sistema, lo manejamos aquí
        except ErrorSoftwareFJ as error:
            # Guardamos el error en el log con su contexto
            self.__registrador.registrar_error(error, contexto="Creación de reserva")
            # Mostramos el error en pantalla
            print(f"[ERROR] {error}")
            # Devolvemos None: no se pudo crear la reserva
            return None
        # Se ejecuta solo si no hubo errores
        else:
            # Agregamos la reserva a la lista en memoria
            self.__reservas.append(reserva)
            # Registramos en el log la creación con sus datos principales
            self.__registrador.registrar_evento(
                f"Reserva creada: [{reserva.identificador}] Cliente={cliente.identificador}, "
                f"Servicio={servicio.identificador}, Duración={duracion}h"
            )
            # Devolvemos la reserva creada
            return reserva

    # Confirma una reserva y calcula su costo total
    def confirmar_reserva(
        self,
        id_reserva: str,                 # Identificador de la reserva a confirmar
        tasa_impuesto: float = 0.19,     # Impuesto (19 % por defecto)
        descuento: float = 0.0,          # Descuento opcional
        recargo_adicional: float = 0.0   # Recargo opcional
    ) -> Optional[float]:
        """Confirma una reserva y calcula su costo total."""
        # Bloque try: captura los errores propios del sistema
        try:
            # Buscamos la reserva por su identificador
            reserva = self.buscar_reserva(id_reserva)
            # Si no existe, no se puede confirmar
            if reserva is None:
                # Lanzamos error de validación
                raise ErrorValidacion(f"No existe la reserva con ID '{id_reserva}'.")

            # Confirmamos la reserva; devuelve el costo total calculado
            total = reserva.confirmar(
                tasa_impuesto=tasa_impuesto,
                descuento=descuento,
                recargo_adicional=recargo_adicional
            )
        # Si ocurrió un error propio del sistema, lo manejamos aquí
        except ErrorSoftwareFJ as error:
            # Guardamos el error en el log indicando qué reserva falló
            self.__registrador.registrar_error(error, contexto=f"Confirmación de reserva '{id_reserva}'")
            # Mostramos el error en pantalla
            print(f"[ERROR] {error}")
            # Devolvemos None: no se pudo confirmar
            return None
        # Se ejecuta solo si no hubo errores
        else:
            # Registramos en el log la confirmación con el total formateado en pesos
            self.__registrador.registrar_evento(
                f"Reserva confirmada: [{reserva.identificador}] Total=${total:,.2f}"
            )
            # Devolvemos el total calculado
            return total

    # Procesa una reserva que ya fue confirmada
    def procesar_reserva(self, id_reserva: str) -> bool:
        """Procesa una reserva confirmada y libera el servicio."""
        # Bloque try: captura los errores propios del sistema
        try:
            # Buscamos la reserva por su identificador
            reserva = self.buscar_reserva(id_reserva)
            # Si no existe, no se puede procesar
            if reserva is None:
                # Lanzamos error de validación
                raise ErrorValidacion(f"No existe la reserva con ID '{id_reserva}'.")

            # Procesamos la reserva (la clase Reserva valida que su estado lo permita)
            reserva.procesar()
        # Si ocurrió un error propio del sistema, lo manejamos aquí
        except ErrorSoftwareFJ as error:
            # Guardamos el error en el log indicando qué reserva falló
            self.__registrador.registrar_error(error, contexto=f"Procesamiento de reserva '{id_reserva}'")
            # Mostramos el error en pantalla
            print(f"[ERROR] {error}")
            # Devolvemos False: no se pudo procesar
            return False
        # Se ejecuta solo si no hubo errores
        else:
            # Registramos en el log que la reserva fue procesada
            self.__registrador.registrar_evento(f"Reserva procesada: [{reserva.identificador}]")
            # Devolvemos True: procesamiento exitoso
            return True

    # Cancela una reserva si su estado lo permite
    def cancelar_reserva(self, id_reserva: str) -> bool:
        """Cancela una reserva si su estado lo permite."""
        # Bloque try: captura los errores propios del sistema
        try:
            # Buscamos la reserva por su identificador
            reserva = self.buscar_reserva(id_reserva)
            # Si no existe, no se puede cancelar
            if reserva is None:
                # Lanzamos error de validación
                raise ErrorValidacion(f"No existe la reserva con ID '{id_reserva}'.")

            # Cancelamos la reserva (la clase Reserva valida que su estado lo permita)
            reserva.cancelar()
        # Si ocurrió un error propio del sistema, lo manejamos aquí
        except ErrorSoftwareFJ as error:
            # Guardamos el error en el log indicando qué reserva falló
            self.__registrador.registrar_error(error, contexto=f"Cancelación de reserva '{id_reserva}'")
            # Mostramos el error en pantalla
            print(f"[ERROR] {error}")
            # Devolvemos False: no se pudo cancelar
            return False
        # Se ejecuta solo si no hubo errores
        else:
            # Registramos en el log que la reserva fue cancelada
            self.__registrador.registrar_evento(f"Reserva cancelada: [{reserva.identificador}]")
            # Devolvemos True: cancelación exitosa
            return True
