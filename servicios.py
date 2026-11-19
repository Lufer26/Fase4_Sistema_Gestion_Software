# Importamos 'abstractmethod' para declarar métodos que las clases hijas están obligadas a implementar
from abc import abstractmethod
# Importamos la clase abstracta base 'Entidad' (definida en entidades.py) de la que hereda Servicio
from entidades import Entidad
# Importamos las excepciones personalizadas que usaremos para reportar errores
from excepciones import ErrorValidacion, ErrorCalculoInconsistente


# Clase abstracta Servicio: hereda de Entidad y sirve de molde para todos los servicios
class Servicio(Entidad):
    """
    Clase abstracta base para todos los servicios de Software FJ.
    Aplica Open/Closed: nuevos servicios se agregan heredando sin modificar esta clase.
    """

    # Constructor: recibe los datos comunes a todos los servicios
    def __init__(self, identificador: str, nombre: str, tarifa_base: float, disponible: bool = True):
        # Llamamos al constructor de la clase padre (Entidad) para guardar el identificador
        super().__init__(identificador)
        # Atributo privado (doble guion bajo) para encapsular el nombre del servicio
        self.__nombre = nombre
        # Atributo privado con la tarifa base por unidad de tiempo
        self.__tarifa_base = tarifa_base
        # Atributo privado que indica si el servicio está disponible (True por defecto)
        self.__disponible = disponible
        # Validamos los datos apenas se crea el objeto; si algo está mal, lanza una excepción
        self.validar()

    # Decorador que permite leer 'nombre' como si fuera un atributo (solo lectura)
    @property
    def nombre(self) -> str:
        # Devuelve el nombre privado del servicio
        return self.__nombre

    # Propiedad de solo lectura para la tarifa base
    @property
    def tarifa_base(self) -> float:
        # Devuelve la tarifa base privada
        return self.__tarifa_base

    # Propiedad de solo lectura para la disponibilidad
    @property
    def disponible(self) -> bool:
        # Devuelve True si el servicio está disponible, False si no
        return self.__disponible

    # Método para cambiar la disponibilidad de forma controlada (no se modifica directamente)
    def cambiar_disponibilidad(self, estado: bool) -> None:
        # Verificamos que el nuevo estado sea realmente un booleano
        if not isinstance(estado, bool):
            # Si no lo es, lanzamos la excepción personalizada de validación
            raise ErrorValidacion("La disponibilidad debe ser un valor booleano.")
        # Si es válido, actualizamos la disponibilidad
        self.__disponible = estado

    # Valida los datos comunes del servicio; las clases hijas lo amplían con sus propias reglas
    def validar(self) -> bool:
        # El nombre debe ser texto y tener al menos 3 caracteres (sin contar espacios de los extremos)
        if not isinstance(self.__nombre, str) or len(self.__nombre.strip()) < 3:
            # Error si el nombre no cumple la regla
            raise ErrorValidacion("El nombre del servicio debe tener al menos 3 caracteres.")
        # La tarifa debe ser número (int o float); se excluye bool porque en Python bool es subtipo de int
        if not isinstance(self.__tarifa_base, (int, float)) or isinstance(self.__tarifa_base, bool):
            # Error si la tarifa no es numérica
            raise ErrorValidacion("La tarifa base debe ser un valor numérico.")
        # La tarifa no puede ser cero ni negativa
        if self.__tarifa_base <= 0:
            # Error si la tarifa no es positiva
            raise ErrorValidacion("La tarifa base debe ser mayor a cero.")
        # La disponibilidad debe ser un booleano
        if not isinstance(self.__disponible, bool):
            # Error si el estado de disponibilidad no es booleano
            raise ErrorValidacion("El estado de disponibilidad debe ser booleano.")
        # Si pasó todas las validaciones, devuelve True
        return True

    # Método abstracto: cada servicio hijo debe implementarlo (polimorfismo)
    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción detallada del servicio."""
        # 'pass' porque aquí no hay lógica; la definen las clases hijas
        pass

    # Método abstracto: cada servicio calcula su subtotal con sus propias reglas
    @abstractmethod
    def _calcular_subtotal(self, duracion: float) -> float:
        """Calcula el subtotal según las reglas propias de cada servicio."""
        # Sin lógica aquí; la implementan las clases hijas
        pass

    # Método de cálculo de costo con "sobrecarga" mediante parámetros opcionales
    def calcular_costo(
        self,
        duracion: float,               # Tiempo del servicio (obligatorio)
        tasa_impuesto: float = 0.0,    # Impuesto opcional, ej. 0.19 = 19 %
        descuento: float = 0.0,        # Descuento opcional, ej. 0.10 = 10 %
        recargo_adicional: float = 0.0  # Recargo fijo opcional
    ) -> float:
        """
        Método con sobrecarga mediante parámetros opcionales.
        Permite calcular costos simples o con impuestos, descuentos y recargos.
        """
        # La duración debe ser número, no booleano y mayor a cero
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool) or duracion <= 0:
            # Error de validación si la duración es inválida
            raise ErrorValidacion("La duración debe ser un número mayor a cero.")
        # El impuesto debe estar entre 0 y 1 (0 % a 100 %)
        if not (0 <= tasa_impuesto <= 1):
            # Error de cálculo si el impuesto está fuera de rango
            raise ErrorCalculoInconsistente("La tasa de impuesto debe estar entre 0 y 1 (ej. 0.19).")
        # El descuento debe estar entre 0 y 1 (0 % a 100 %)
        if not (0 <= descuento <= 1):
            # Error de cálculo si el descuento está fuera de rango
            raise ErrorCalculoInconsistente("El descuento debe estar entre 0 y 1 (ej. 0.10).")
        # El recargo adicional no puede ser negativo
        if recargo_adicional < 0:
            # Error de cálculo si el recargo es negativo
            raise ErrorCalculoInconsistente("El recargo adicional no puede ser negativo.")

        # Subtotal = cálculo propio del servicio (polimorfismo) + recargo adicional
        subtotal = self._calcular_subtotal(duracion) + recargo_adicional
        # Si el subtotal no es positivo, hay una inconsistencia en el cálculo
        if subtotal <= 0:
            # Error de cálculo por subtotal inválido
            raise ErrorCalculoInconsistente("El subtotal calculado resultó inválido (<= 0).")

        # Monto que se descuenta del subtotal
        monto_descuento = subtotal * descuento
        # Base sobre la que se aplica el impuesto (subtotal menos el descuento)
        base_gravable = subtotal - monto_descuento
        # Total final = base + impuesto
        total = base_gravable * (1 + tasa_impuesto)

        # Verificación de seguridad: el total nunca debe ser negativo
        if total < 0:
            # Error de cálculo si el total salió negativo
            raise ErrorCalculoInconsistente("El costo total no puede ser negativo.")

        # Devolvemos el total redondeado a 2 decimales
        return round(total, 2)

    # Representación en texto del servicio (se usa al hacer print(servicio))
    def __str__(self) -> str:
        # Convertimos el booleano de disponibilidad en un texto legible
        estado = "Disponible" if self.__disponible else "No disponible"
        # Armamos la cadena con identificador, descripción, tarifa formateada y estado
        return f"[{self.identificador}] {self.describir()} | Tarifa base: ${self.__tarifa_base:,.2f} | {estado}"


# Clase hija 1: servicio de reserva de salas (hereda de Servicio)
class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas."""

    # Constructor con los datos comunes más los propios de una sala
    def __init__(
        self,
        identificador: str,            # Código único de la sala
        nombre: str,                   # Nombre de la sala
        tarifa_base: float,            # Tarifa por hora
        capacidad: int,                # Cantidad máxima de personas
        tiene_proyector: bool = False,  # Indica si incluye proyector
        disponible: bool = True        # Disponibilidad inicial
    ):
        # Guardamos la capacidad (privada) ANTES de llamar al padre, porque el padre ejecuta validar()
        self.__capacidad = capacidad
        # Guardamos si tiene proyector (privado), también antes del super()
        self.__tiene_proyector = tiene_proyector
        # Llamamos al constructor de Servicio con los datos comunes
        super().__init__(identificador, nombre, tarifa_base, disponible)

    # Propiedad de solo lectura para la capacidad
    @property
    def capacidad(self) -> int:
        # Devuelve la capacidad de la sala
        return self.__capacidad

    # Propiedad de solo lectura para el proyector
    @property
    def tiene_proyector(self) -> bool:
        # Devuelve True si la sala tiene proyector
        return self.__tiene_proyector

    # Sobrescribe validar() para agregar reglas propias de la sala
    def validar(self) -> bool:
        # Primero ejecuta las validaciones comunes de la clase padre
        super().validar()
        # La capacidad debe ser entero (no bool) y mayor a cero
        if not isinstance(self.__capacidad, int) or isinstance(self.__capacidad, bool) or self.__capacidad <= 0:
            # Error si la capacidad es inválida
            raise ErrorValidacion("La capacidad de la sala debe ser un entero positivo.")
        # El indicador de proyector debe ser booleano
        if not isinstance(self.__tiene_proyector, bool):
            # Error si no es booleano
            raise ErrorValidacion("El indicador de proyector debe ser booleano.")
        # Todo correcto: devuelve True
        return True

    # Implementa el método abstracto describir() para una sala
    def describir(self) -> str:
        # Texto según si la sala tiene o no proyector
        proyector = "con proyector" if self.__tiene_proyector else "sin proyector"
        # Devuelve la descripción con nombre, capacidad y proyector
        return f"Sala '{self.nombre}' (Capacidad: {self.__capacidad} personas, {proyector})"

    # Implementa el cálculo de subtotal propio de una sala
    def _calcular_subtotal(self, duracion: float) -> float:
        # Si tiene proyector se suma un recargo fijo de 15.000; si no, 0
        recargo_proyector = 15000.0 if self.__tiene_proyector else 0.0
        # Subtotal = tarifa por duración + recargo del proyector
        return (self.tarifa_base * duracion) + recargo_proyector


# Clase hija 2: servicio de alquiler de equipos (hereda de Servicio)
class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos."""

    # Constructor con los datos comunes más los propios de un equipo
    def __init__(
        self,
        identificador: str,            # Código único del equipo
        nombre: str,                   # Nombre del equipo
        tarifa_base: float,            # Tarifa por unidad de tiempo
        tipo_equipo: str,              # Tipo de equipo (portátil, cámara, etc.)
        deposito_garantia: float = 0.0,  # Depósito de garantía opcional
        disponible: bool = True        # Disponibilidad inicial
    ):
        # Guardamos el tipo de equipo (privado) antes de llamar al padre
        self.__tipo_equipo = tipo_equipo
        # Guardamos el depósito de garantía (privado) antes de llamar al padre
        self.__deposito_garantia = deposito_garantia
        # Llamamos al constructor de Servicio con los datos comunes
        super().__init__(identificador, nombre, tarifa_base, disponible)

    # Propiedad de solo lectura para el tipo de equipo
    @property
    def tipo_equipo(self) -> str:
        # Devuelve el tipo de equipo
        return self.__tipo_equipo

    # Propiedad de solo lectura para el depósito
    @property
    def deposito_garantia(self) -> float:
        # Devuelve el depósito de garantía
        return self.__deposito_garantia

    # Sobrescribe validar() para agregar reglas propias del equipo
    def validar(self) -> bool:
        # Primero ejecuta las validaciones comunes de la clase padre
        super().validar()
        # El tipo de equipo debe ser texto de al menos 3 caracteres
        if not isinstance(self.__tipo_equipo, str) or len(self.__tipo_equipo.strip()) < 3:
            # Error si el tipo de equipo es inválido
            raise ErrorValidacion("El tipo de equipo debe tener al menos 3 caracteres.")
        # El depósito debe ser numérico (y no booleano)
        if not isinstance(self.__deposito_garantia, (int, float)) or isinstance(self.__deposito_garantia, bool):
            # Error si el depósito no es numérico
            raise ErrorValidacion("El depósito de garantía debe ser numérico.")
        # El depósito no puede ser negativo
        if self.__deposito_garantia < 0:
            # Error si el depósito es negativo
            raise ErrorValidacion("El depósito de garantía no puede ser negativo.")
        # Todo correcto: devuelve True
        return True

    # Implementa el método abstracto describir() para un equipo
    def describir(self) -> str:
        # Devuelve la descripción con nombre, tipo y depósito formateado con separador de miles
        return f"Equipo '{self.nombre}' (Tipo: {self.__tipo_equipo}, Depósito: ${self.__deposito_garantia:,.2f})"

    # Implementa el cálculo de subtotal propio de un equipo
    def _calcular_subtotal(self, duracion: float) -> float:
        # Subtotal = tarifa por duración + depósito de garantía
        return (self.tarifa_base * duracion) + self.__deposito_garantia


# Clase hija 3: servicio de asesorías especializadas (hereda de Servicio)
class AsesoriaEspecializada(Servicio):
    """Servicio especializado para asesorías técnicas o de negocio."""

    # Diccionario de clase: niveles permitidos y su multiplicador de precio
    NIVELES_VALIDOS = {
        "basico": 1.0,       # Nivel básico: sin recargo
        "intermedio": 1.25,  # Nivel intermedio: 25 % más caro
        "avanzado": 1.5      # Nivel avanzado: 50 % más caro
    }

    # Constructor con los datos comunes más los propios de una asesoría
    def __init__(
        self,
        identificador: str,            # Código único de la asesoría
        nombre: str,                   # Nombre de la asesoría
        tarifa_base: float,            # Tarifa por hora
        especialidad: str,             # Área de la asesoría
        nivel_complejidad: str = "basico",  # Nivel (basico, intermedio, avanzado)
        disponible: bool = True        # Disponibilidad inicial
    ):
        # Guardamos la especialidad (privada) antes de llamar al padre
        self.__especialidad = especialidad
        # Normalizamos el nivel: sin espacios y en minúsculas; si no es texto, se deja igual para que validar() lo rechace
        self.__nivel_complejidad = nivel_complejidad.strip().lower() if isinstance(nivel_complejidad, str) else nivel_complejidad
        # Llamamos al constructor de Servicio con los datos comunes
        super().__init__(identificador, nombre, tarifa_base, disponible)

    # Propiedad de solo lectura para la especialidad
    @property
    def especialidad(self) -> str:
        # Devuelve la especialidad
        return self.__especialidad

    # Propiedad de solo lectura para el nivel de complejidad
    @property
    def nivel_complejidad(self) -> str:
        # Devuelve el nivel de complejidad
        return self.__nivel_complejidad

    # Sobrescribe validar() para agregar reglas propias de la asesoría
    def validar(self) -> bool:
        # Primero ejecuta las validaciones comunes de la clase padre
        super().validar()
        # La especialidad debe ser texto de al menos 3 caracteres
        if not isinstance(self.__especialidad, str) or len(self.__especialidad.strip()) < 3:
            # Error si la especialidad es inválida
            raise ErrorValidacion("La especialidad debe tener al menos 3 caracteres.")
        # El nivel debe ser una de las llaves permitidas del diccionario
        if self.__nivel_complejidad not in self.NIVELES_VALIDOS:
            # Armamos un texto con los niveles válidos separados por coma
            niveles = ", ".join(self.NIVELES_VALIDOS.keys())
            # Error indicando cuáles niveles se pueden usar
            raise ErrorValidacion(f"Nivel de complejidad inválido. Use: {niveles}.")
        # Todo correcto: devuelve True
        return True

    # Implementa el método abstracto describir() para una asesoría
    def describir(self) -> str:
        # Devuelve la descripción con nombre, especialidad y nivel
        return f"Asesoría '{self.nombre}' (Especialidad: {self.__especialidad}, Nivel: {self.__nivel_complejidad})"

    # Implementa el cálculo de subtotal propio de una asesoría
    def _calcular_subtotal(self, duracion: float) -> float:
        # Obtenemos el multiplicador según el nivel de complejidad
        multiplicador = self.NIVELES_VALIDOS[self.__nivel_complejidad]
        # Subtotal = tarifa × duración × multiplicador del nivel
        return self.tarifa_base * duracion * multiplicador
      
