# Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de la Fase 4 del curso Programación (213023), UNAD.
Sistema orientado a objetos para la empresa **Software FJ**, sin base de datos.

## Integrantes
- [LUIZA FERNANDA ROMERO ORTIZ]
- [JEINER ALEXIS BUSTOS QUIPO]
- [JEYDI PAOLA ORTEGON ABRIL ]

## Descripción
Gestiona clientes, servicios (salas, equipos y asesorías) y reservas.
Aplica abstracción, herencia, polimorfismo, encapsulación y manejo
avanzado de excepciones. Los errores se registran en un archivo de logs
y el programa continúa funcionando.

## Estructura del proyecto
- `entidades.py`: clase abstracta base y clase Cliente.
- `servicios.py`: clase abstracta Servicio y tres servicios especializados
  (ReservaSala, AlquilerEquipo, AsesoriaEspecializada).
- `reservas.py`: clase Reserva con estados (confirmar, procesar, cancelar).
- `excepciones.py`: excepciones personalizadas.
- `logger.py`: registro de eventos y errores en archivo.
- `gestor.py`: administra clientes, servicios y reservas en memoria.
- `main.py`: simulación de 12 operaciones y menú interactivo.
- `prueba_entidades.py`: pruebas de las entidades.

## Conceptos aplicados
- **Abstracción:** clases abstractas `Entidad`, `Servicio` y `RegistradorEventos`.
- **Herencia y polimorfismo:** los tres servicios sobrescriben `describir` y `_calcular_subtotal`.
- **Encapsulación:** atributos privados con propiedades de solo lectura.
- **Sobrecarga:** `calcular_costo` con impuesto, descuento y recargo opcionales.
- **Excepciones:** personalizadas, `try/except/else/finally` y encadenamiento con `raise ... from ...`.

## Cómo ejecutar
1. Instalar Python 3.
2. Descargar el proyecto.
3. En la terminal: `python main.py`
4. Al terminar las 12 operaciones se abre un menú; escribir `0` para salir.
5. Los errores y eventos quedan en `software_fj.log`.
