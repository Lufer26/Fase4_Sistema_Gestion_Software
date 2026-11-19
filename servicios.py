from abc import abstractmethod
from entidades import Entidad
from excepciones import ErrorValidacion, ErrorCalculoInconsistente


class Servicio(Entidad):
    """
    Clase abstracta base para todos los servicios de Software FJ.
    Aplica Open/Closed: nuevos servicios se agregan heredando sin modificar esta clase.
    """

    def __init__(self, identificador: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(identificador)
        self.__nombre = nombre
        self.__tarifa_base = tarifa_base
        self.__disponible = disponible
        self.validar()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def tarifa_base(self) -> float:
        return self.__tarifa_base

    @property
    def disponible(self) -> bool:
        return self.__disponible

    def cambiar_disponibilidad(self, estado: bool) -> None:
        if not isinstance(estado, bool):
            raise ErrorValidacion("La disponibilidad debe ser un valor booleano.")
        self.__disponible = estado

    def validar(self) -> bool:
        if not isinstance(self.__nombre, str) or len(self.__nombre.strip()) < 3:
            raise ErrorValidacion("El nombre del servicio debe tener al menos 3 caracteres.")
        if not isinstance(self.__tarifa_base, (int, float)) or isinstance(self.__tarifa_base, bool):
            raise ErrorValidacion("La tarifa base debe ser un valor numérico.")
        if self.__tarifa_base <= 0:
            raise ErrorValidacion("La tarifa base debe ser mayor a cero.")
        if not isinstance(self.__disponible, bool):
            raise ErrorValidacion("El estado de disponibilidad debe ser booleano.")
        return True

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción detallada del servicio."""
        pass

    @abstractmethod
    def _calcular_subtotal(self, duracion: float) -> float:
        """Calcula el subtotal según las reglas propias de cada servicio."""
        pass

    def calcular_costo(
        self,
        duracion: float,
        tasa_impuesto: float = 0.0,
        descuento: float = 0.0,
        recargo_adicional: float = 0.0
    ) -> float:
        """
        Método con sobrecarga mediante parámetros opcionales.
        Permite calcular costos simples o con impuestos, descuentos y recargos.
        """
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            raise ErrorValidacion("La duración debe ser un número mayor a cero.")
        if not (0 <= tasa_impuesto <= 1):
            raise ErrorCalculoInconsistente("La tasa de impuesto debe estar entre 0 y 1 (ej. 0.19).")
        if not (0 <= descuento <= 1):
            raise ErrorCalculoInconsistente("El descuento debe estar entre 0 y 1 (ej. 0.10).")
        if recargo_adicional < 0:
            raise ErrorCalculoInconsistente("El recargo adicional no puede ser negativo.")

        subtotal = self._calcular_subtotal(duracion) + recargo_adicional
        if subtotal <= 0:
            raise ErrorCalculoInconsistente("El subtotal calculado resultó inválido (<= 0).")

        monto_descuento = subtotal * descuento
        base_gravable = subtotal - monto_descuento
        total = base_gravable * (1 + tasa_impuesto)

        if total < 0:
            raise ErrorCalculoInconsistente("El costo total no puede ser negativo.")

        return round(total, 2)

    def __str__(self) -> str:
        estado = "Disponible" if self.__disponible else "No disponible"
        return f"[{self.identificador}] {self.describir()} | Tarifa base: ${self.__tarifa_base:,.2f} | {estado}"


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        capacidad: int,
        tiene_proyector: bool = False,
        disponible: bool = True
    ):
        self.__capacidad = capacidad
        self.__tiene_proyector = tiene_proyector
        super().__init__(identificador, nombre, tarifa_base, disponible)

    @property
    def capacidad(self) -> int:
        return self.__capacidad

    @property
    def tiene_proyector(self) -> bool:
        return self.__tiene_proyector

    def validar(self) -> bool:
        super().validar()
        if not isinstance(self.__capacidad, int) or isinstance(self.__capacidad, bool) or self.__capacidad <= 0:
            raise ErrorValidacion("La capacidad de la sala debe ser un entero positivo.")
        if not isinstance(self.__tiene_proyector, bool):
            raise ErrorValidacion("El indicador de proyector debe ser booleano.")
        return True

    def describir(self) -> str:
        proyector = "con proyector" if self.__tiene_proyector else "sin proyector"
        return f"Sala '{self.nombre}' (Capacidad: {self.__capacidad} personas, {proyector})"

    def _calcular_subtotal(self, duracion: float) -> float:
        recargo_proyector = 15000.0 if self.__tiene_proyector else 0.0
        return (self.tarifa_base * duracion) + recargo_proyector


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        tipo_equipo: str,
        deposito_garantia: float = 0.0,
        disponible: bool = True
    ):
        self.__tipo_equipo = tipo_equipo
        self.__deposito_garantia = deposito_garantia
        super().__init__(identificador, nombre, tarifa_base, disponible)

    @property
    def tipo_equipo(self) -> str:
        return self.__tipo_equipo

    @property
    def deposito_garantia(self) -> float:
        return self.__deposito_garantia

    def validar(self) -> bool:
        super().validar()
        if not isinstance(self.__tipo_equipo, str) or len(self.__tipo_equipo.strip()) < 3:
            raise ErrorValidacion("El tipo de equipo debe tener al menos 3 caracteres.")
        if not isinstance(self.__deposito_garantia, (int, float)) or isinstance(self.__deposito_garantia, bool):
            raise ErrorValidacion("El depósito de garantía debe ser numérico.")
        if self.__deposito_garantia < 0:
            raise ErrorValidacion("El depósito de garantía no puede ser negativo.")
        return True

    def describir(self) -> str:
        return f"Equipo '{self.nombre}' (Tipo: {self.__tipo_equipo}, Depósito: ${self.__deposito_garantia:,.2f})"

    def _calcular_subtotal(self, duracion: float) -> float:
        return (self.tarifa_base * duracion) + self.__deposito_garantia


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para asesorías técnicas o de negocio."""

    NIVELES_VALIDOS = {
        "basico": 1.0,
        "intermedio": 1.25,
        "avanzado": 1.5
    }

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        especialidad: str,
        nivel_complejidad: str = "basico",
        disponible: bool = True
    ):
        self.__especialidad = especialidad
        self.__nivel_complejidad = nivel_complejidad.strip().lower() if isinstance(nivel_complejidad, str) else nivel_complejidad
        super().__init__(identificador, nombre, tarifa_base, disponible)

    @property
    def especialidad(self) -> str:
        return self.__especialidad

    @property
    def nivel_complejidad(self) -> str:
        return self.__nivel_complejidad

    def validar(self) -> bool:
        super().validar()
        if not isinstance(self.__especialidad, str) or len(self.__especialidad.strip()) < 3:
            raise ErrorValidacion("La especialidad debe tener al menos 3 caracteres.")
        if self.__nivel_complejidad not in self.NIVELES_VALIDOS:
            niveles = ", ".join(self.NIVELES_VALIDOS.keys())
            raise ErrorValidacion(f"Nivel de complejidad inválido. Use: {niveles}.")
        return True

    def describir(self) -> str:
        return f"Asesoría '{self.nombre}' (Especialidad: {self.__especialidad}, Nivel: {self.__nivel_complejidad})"

    def _calcular_subtotal(self, duracion: float) -> float:
        multiplicador = self.NIVELES_VALIDOS[self.__nivel_complejidad]
        return self.tarifa_base * duracion * multiplicador