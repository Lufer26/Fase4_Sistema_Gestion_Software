# Importamos el registrador que guarda eventos y errores en un archivo de texto
from logger import LoggerArchivo
# Importamos la clase principal que coordina clientes, servicios y reservas
from gestor import SistemaSoftwareFJ
# Importamos los tres tipos de servicio especializados (herencia de Servicio)
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
# Importamos la excepción base para capturar cualquier error propio del sistema
from excepciones import ErrorSoftwareFJ


# Función que ejecuta de forma automática las 12 operaciones de prueba que pide la guía
def ejecutar_simulacion_automatica(sistema: SistemaSoftwareFJ) -> None:
    """
    Ejecuta 12 operaciones completas (válidas e inválidas) demostrando
    polimorfismo, sobrecarga de costos, control de estados y manejo de excepciones.
    """
    # Imprimimos una línea de 65 signos "=" como separador visual
    print("=" * 65)
    # Título de inicio de la simulación
    print(" INICIO DE SIMULACIÓN AUTOMÁTICA - SOFTWARE FJ (12 OPERACIONES)")
    # Otra línea separadora
    print("=" * 65)

    # 1. Registro válido de cliente
    print("\n[Op 1] Registro de cliente válido (C001):")
    # Registramos al cliente C001 con datos correctos; devuelve el cliente o None si falla
    c1 = sistema.registrar_cliente("C001", "Laura Martínez", "1020304050", "laura@softwarefj.com", "3001234567")
    # Si el registro funcionó (c1 no es None), mostramos el cliente
    if c1:
        print(f"  OK -> {c1}")

    # 2. Registro inválido de cliente (correo y teléfono mal formados)
    print("\n[Op 2] Registro de cliente inválido (C002 - correo incorrecto):")
    # El correo "correo_invalido" no cumple el formato: el gestor captura el error, lo registra en el log y el programa sigue
    sistema.registrar_cliente("C002", "Carlos Ruiz", "98765432", "correo_invalido", "3109876543")

    # 3. Registro de segundo cliente válido
    print("\n[Op 3] Registro de cliente válido (C003):")
    # Registramos al cliente C003 con datos correctos
    c3 = sistema.registrar_cliente("C003", "Andrés Gómez", "80112233", "andres.gomez@empresa.co", "+573152223344")
    # Si el registro funcionó, mostramos el cliente
    if c3:
        print(f"  OK -> {c3}")

    # 4. Creación válida de 3 servicios especializados (Polimorfismo)
    print("\n[Op 4] Creación y registro de 3 servicios válidos:")
    # Lista con tres objetos de clases distintas; todos son de tipo Servicio (polimorfismo)
    servicios_validos = [
        # Sala con capacidad para 12 personas y proyector
        ReservaSala("S001", "Sala Innovación", 80000.0, capacidad=12, tiene_proyector=True),
        # Equipo tipo portátil con depósito de garantía de 50.000
        AlquilerEquipo("S002", "Workstation Dell Precision", 35000.0, tipo_equipo="Portátil CAD", deposito_garantia=50000.0),
        # Asesoría de nivel avanzado (tiene multiplicador de precio 1.5)
        AsesoriaEspecializada("S003", "Arquitectura Cloud", 120000.0, especialidad="DevOps", nivel_complejidad="avanzado")
    ]
    # Recorremos la lista y registramos cada servicio en el sistema
    for srv in servicios_validos:
        # registrar_servicio devuelve True si se registró bien
        if sistema.registrar_servicio(srv):
            # Al imprimir, se usa el __str__ de cada servicio (cada uno se describe a su manera)
            print(f"  OK -> {srv}")

    # 5. Creación inválida de servicio (tarifa negativa y nivel inválido)
    print("\n[Op 5] Intento de creación de servicio inválido (tarifa negativa):")
    # Bloque try: crear este servicio lanzará un error porque la tarifa es negativa
    try:
        # La tarifa -50000.0 hace que validar() lance ErrorValidacion al construir el objeto
        srv_invalido = ReservaSala("S004", "Sala Error", -50000.0, capacidad=5)
        # Esta línea no llega a ejecutarse porque el error ocurre en la línea anterior
        sistema.registrar_servicio(srv_invalido)
    # Capturamos cualquier error propio del sistema
    except ErrorSoftwareFJ as error:
        # Guardamos el error en el log; el programa continúa sin detenerse
        sistema.registrar_error_externo(error, contexto="Creación de servicio S004")

    # 6. Creación inválida de asesoría (nivel de complejidad inexistente)
    print("\n[Op 6] Intento de creación de asesoría con nivel inválido:")
    # Bloque try: el nivel "experto" no existe, así que se lanzará un error
    try:
        # Los niveles válidos son basico, intermedio y avanzado; "experto" provoca ErrorValidacion
        asesoria_err = AsesoriaEspecializada("S005", "Asesoría IA", 100000.0, especialidad="ML", nivel_complejidad="experto")
        # Esta línea no se ejecuta porque falla la creación
        sistema.registrar_servicio(asesoria_err)
    # Capturamos el error propio del sistema
    except ErrorSoftwareFJ as error:
        # Lo registramos en el log y seguimos
        sistema.registrar_error_externo(error, contexto="Creación de servicio S005")

    # 7. Reserva exitosa + Confirmación con impuesto y descuento (Sobrecarga de calcular_costo)
    print("\n[Op 7] Reserva válida R001 (Sala S001) y confirmación con IVA 19% y descuento 10%:")
    # Creamos la reserva R001: cliente C001, servicio S001, 3 horas
    r1 = sistema.crear_reserva("R001", "C001", "S001", duracion=3)
    # Si la reserva se creó correctamente
    if r1:
        # La confirmamos aplicando 19 % de impuesto y 10 % de descuento; devuelve el total
        total = sistema.confirmar_reserva("R001", tasa_impuesto=0.19, descuento=0.10)
        # Si la confirmación funcionó (total no es None), mostramos la reserva
        if total is not None:
            print(f"  OK -> {r1}")

    # 8. Intento de reservar un servicio que ya no está disponible
    print("\n[Op 8] Intento de confirmar reserva R002 sobre sala S001 ya ocupada:")
    # Creamos R002 sobre la misma sala S001, que quedó ocupada tras confirmar R001
    r2 = sistema.crear_reserva("R002", "C003", "S001", duracion=2)
    # Si la reserva se creó, intentamos confirmarla (fallará porque el servicio no está disponible)
    if r2:
        sistema.confirmar_reserva("R002")

    # 9. Intento de confirmación con parámetro de cálculo inconsistente (descuento > 100%)
    print("\n[Op 9] Intento de confirmar reserva R003 con descuento inválido (1.5 -> 150%):")
    # Creamos R003: cliente C003, equipo S002, 4 horas
    r3 = sistema.crear_reserva("R003", "C003", "S002", duracion=4)
    # Si se creó, intentamos confirmarla con un descuento de 150 %, lo cual es inválido
    if r3:
        sistema.confirmar_reserva("R003", tasa_impuesto=0.19, descuento=1.5)

    # 10. Confirmación exitosa de R003 con recargo adicional y posterior procesamiento
    print("\n[Op 10] Confirmación correcta de R003 (Equipo S002) con recargo y procesamiento:")
    # Ahora confirmamos R003 con datos válidos: 19 % de impuesto, 5 % de descuento y 10.000 de recargo
    total_r3 = sistema.confirmar_reserva("R003", tasa_impuesto=0.19, descuento=0.05, recargo_adicional=10000.0)
    # Si la confirmación funcionó, la procesamos; si el procesamiento también funciona, mostramos la reserva
    if total_r3 is not None and sistema.procesar_reserva("R003"):
        print(f"  OK -> {r3}")

    # 11. Intento de cancelar una reserva ya procesada (Operación no permitida)
    print("\n[Op 11] Intento de cancelar reserva R003 que ya fue procesada:")
    # Una reserva procesada no se puede cancelar: se lanza ErrorOperacionNoPermitida y queda en el log
    sistema.cancelar_reserva("R003")

    # 12. Creación, confirmación y cancelación válida de asesoría (libera el servicio)
    print("\n[Op 12] Creación, confirmación y cancelación controlada de R004 (Asesoría S003):")
    # Creamos R004: cliente C001, asesoría S003, 2 horas
    r4 = sistema.crear_reserva("R004", "C001", "S003", duracion=2)
    # Si se creó correctamente
    if r4:
        # La confirmamos sin impuesto (tasa 0.0)
        sistema.confirmar_reserva("R004", tasa_impuesto=0.0)
        # La cancelamos; si funciona, el servicio queda libre y mostramos la reserva
        if sistema.cancelar_reserva("R004"):
            print(f"  OK -> {r4}")

    # Línea en blanco y separador de cierre
    print("\n" + "=" * 65)
    # Mensaje final: el programa terminó las 12 operaciones sin detenerse
    print(" SIMULACIÓN FINALIZADA SIN INTERRUPCIONES (Revise software_fj.log)")
    # Separador final
    print("=" * 65)


# --- Utilidades para el Menú Interactivo ---

# Lee un número decimal desde el teclado, repitiendo hasta que el usuario escriba algo válido
def leer_flotante(mensaje: str, valor_por_defecto: float = None) -> float:
    # Ciclo infinito: solo termina cuando se devuelve un valor
    while True:
        # Pedimos el dato y quitamos espacios sobrantes
        entrada = input(mensaje).strip()
        # Si el usuario presionó Enter sin escribir y hay un valor por defecto, lo usamos
        if entrada == "" and valor_por_defecto is not None:
            return valor_por_defecto
        # Intentamos convertir el texto a número decimal
        try:
            return float(entrada)
        # Si no es un número válido, se produce ValueError
        except ValueError:
            # Avisamos y el ciclo vuelve a pedir el dato
            print("  [AVISO] Ingrese un número válido.")


# Lee un número entero desde el teclado, repitiendo hasta que el usuario escriba algo válido
def leer_entero(mensaje: str) -> int:
    # Ciclo infinito: solo termina cuando se devuelve un valor
    while True:
        # Intentamos leer y convertir el texto a entero
        try:
            return int(input(mensaje).strip())
        # Si no es un entero válido, se produce ValueError
        except ValueError:
            # Avisamos y el ciclo vuelve a pedir el dato
            print("  [AVISO] Ingrese un número entero válido.")


# Submenú para registrar un servicio escogiendo su tipo
def menu_registrar_servicio(sistema: SistemaSoftwareFJ) -> None:
    # Mostramos los tipos de servicio disponibles
    print("\nTipos de servicio: 1. Sala | 2. Equipo | 3. Asesoría")
    # Leemos el tipo elegido
    tipo = input("Seleccione tipo (1-3): ").strip()
    # Leemos los datos comunes a todos los servicios
    id_srv = input("ID del servicio: ").strip()
    # Nombre del servicio
    nombre = input("Nombre del servicio: ").strip()
    # Tarifa base (se valida que sea un número)
    tarifa = leer_flotante("Tarifa base: ")

    # Bloque try: crear el servicio puede lanzar errores de validación
    try:
        # Si eligió 1, se crea una sala
        if tipo == "1":
            # Pedimos la capacidad como entero
            capacidad = leer_entero("Capacidad de personas: ")
            # Si responde "s" hay proyector; cualquier otra respuesta es False
            proyector = input("¿Tiene proyector? (s/n): ").strip().lower() == "s"
            # Creamos la sala con los datos ingresados
            srv = ReservaSala(id_srv, nombre, tarifa, capacidad, proyector)
        # Si eligió 2, se crea un alquiler de equipo
        elif tipo == "2":
            # Pedimos el tipo de equipo
            tipo_eq = input("Tipo de equipo: ").strip()
            # Pedimos el depósito (Enter equivale a 0)
            deposito = leer_flotante("Depósito de garantía (Enter para 0): ", 0.0)
            # Creamos el alquiler de equipo
            srv = AlquilerEquipo(id_srv, nombre, tarifa, tipo_eq, deposito)
        # Si eligió 3, se crea una asesoría
        elif tipo == "3":
            # Pedimos la especialidad
            esp = input("Especialidad: ").strip()
            # Pedimos el nivel de complejidad
            nivel = input("Nivel (basico/intermedio/avanzado): ").strip()
            # Creamos la asesoría
            srv = AsesoriaEspecializada(id_srv, nombre, tarifa, esp, nivel)
        # Si escribió cualquier otra cosa, el tipo no es válido
        else:
            # Avisamos del error
            print("  [AVISO] Tipo de servicio no válido.")
            # Salimos de la función sin registrar nada
            return

        # Registramos el servicio creado; si funciona, lo mostramos
        if sistema.registrar_servicio(srv):
            print(f"  Servicio registrado: {srv}")
    # Si al crear el servicio hubo un error propio del sistema
    except ErrorSoftwareFJ as error:
        # Lo registramos en el log y el programa continúa
        sistema.registrar_error_externo(error, contexto="Registro manual de servicio")


# Muestra en pantalla todo el contenido del archivo de logs
def mostrar_logs(ruta_archivo: str) -> None:
    # Título con el nombre del archivo
    print(f"\n--- CONTENIDO DE {ruta_archivo} ---")
    # Bloque try: abrir el archivo puede fallar (por ejemplo, si no existe)
    try:
        # Abrimos el archivo en modo lectura ("r")
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            # Leemos todo el texto
            contenido = archivo.read()
            # Mostramos el contenido; si está vacío, avisamos
            print(contenido if contenido else "(Archivo vacío)")
    # Si ocurre un error de lectura/escritura (OSError)
    except OSError as error:
        # Avisamos sin detener el programa
        print(f"No se pudo leer el archivo de logs: {error}")


# Menú interactivo que se repite hasta que el usuario elija salir
def ejecutar_menu_interactivo(sistema: SistemaSoftwareFJ, ruta_log: str) -> None:
    # Ciclo infinito: solo termina con la opción 0 (break)
    while True:
        # Línea separadora
        print("\n" + "-" * 45)
        # Título del menú
        print(" MENÚ INTERACTIVO - SOFTWARE FJ")
        # Línea separadora
        print("-" * 45)
        # Opciones disponibles
        print("1. Registrar cliente")
        print("2. Registrar servicio")
        print("3. Crear reserva")
        print("4. Confirmar reserva")
        print("5. Procesar reserva")
        print("6. Cancelar reserva")
        print("7. Listar clientes, servicios y reservas")
        print("8. Ver archivo de logs")
        print("0. Salir")

        # Leemos la opción elegida
        opcion = input("Seleccione una opción: ").strip()

        # Opción 1: registrar un cliente
        if opcion == "1":
            # Pedimos los datos del cliente uno por uno
            id_cli = input("ID Cliente: ").strip()
            nombre = input("Nombre: ").strip()
            doc = input("Documento (5-15 dígitos): ").strip()
            correo = input("Correo: ").strip()
            tel = input("Teléfono (7-15 dígitos): ").strip()
            # Registramos el cliente (el gestor valida y maneja los errores)
            cli = sistema.registrar_cliente(id_cli, nombre, doc, correo, tel)
            # Si se registró bien, lo mostramos
            if cli:
                print(f"  Cliente registrado: {cli}")

        # Opción 2: registrar un servicio
        elif opcion == "2":
            # Delegamos en el submenú de servicios
            menu_registrar_servicio(sistema)

        # Opción 3: crear una reserva
        elif opcion == "3":
            # Pedimos los datos de la reserva
            id_res = input("ID Reserva: ").strip()
            id_cli = input("ID Cliente: ").strip()
            id_srv = input("ID Servicio: ").strip()
            duracion = leer_flotante("Duración (horas): ")
            # Creamos la reserva (queda en estado PENDIENTE)
            res = sistema.crear_reserva(id_res, id_cli, id_srv, duracion)
            # Si se creó bien, la mostramos
            if res:
                print(f"  Reserva creada: {res}")

        # Opción 4: confirmar una reserva
        elif opcion == "4":
            # Pedimos el identificador de la reserva
            id_res = input("ID Reserva a confirmar: ").strip()
            # Impuesto, descuento y recargo son opcionales: con Enter se usan los valores por defecto
            imp = leer_flotante("Tasa impuesto 0-1 (Enter para 0.19): ", 0.19)
            desc = leer_flotante("Descuento 0-1 (Enter para 0.0): ", 0.0)
            rec = leer_flotante("Recargo adicional (Enter para 0.0): ", 0.0)
            # Confirmamos la reserva; devuelve el total o None si falló
            total = sistema.confirmar_reserva(id_res, imp, desc, rec)
            # Si se confirmó, mostramos el total formateado
            if total is not None:
                print(f"  Reserva confirmada. Total a pagar: ${total:,.2f}")

        # Opción 5: procesar una reserva
        elif opcion == "5":
            # Pedimos el identificador de la reserva
            id_res = input("ID Reserva a procesar: ").strip()
            # Si se procesó bien, avisamos
            if sistema.procesar_reserva(id_res):
                print("  Reserva procesada y servicio liberado.")

        # Opción 6: cancelar una reserva
        elif opcion == "6":
            # Pedimos el identificador de la reserva
            id_res = input("ID Reserva a cancelar: ").strip()
            # Si se canceló bien, avisamos
            if sistema.cancelar_reserva(id_res):
                print("  Reserva cancelada correctamente.")

        # Opción 7: listar todo lo registrado
        elif opcion == "7":
            # Listado de clientes
            print("\n--- CLIENTES ---")
            for c in sistema.clientes:
                print(f"  [{c.identificador}] {c}")
            # Listado de servicios
            print("\n--- SERVICIOS ---")
            for s in sistema.servicios:
                print(f"  {s}")
            # Listado de reservas
            print("\n--- RESERVAS ---")
            for r in sistema.reservas:
                print(f"  {r}")

        # Opción 8: ver el archivo de logs
        elif opcion == "8":
            # Mostramos el contenido del archivo de logs
            mostrar_logs(ruta_log)

        # Opción 0: salir del programa
        elif opcion == "0":
            # Mensaje de despedida
            print("Cerrando Sistema Software FJ. ¡Hasta pronto!")
            # Rompemos el ciclo y termina el menú
            break
        # Cualquier otra opción no es válida
        else:
            # Avisamos y el ciclo vuelve a mostrar el menú
            print("Opción no válida. Intente nuevamente.")


# Este bloque se ejecuta solo cuando se corre este archivo directamente (python main.py)
if __name__ == "__main__":
    # Creamos el registrador que guardará los logs en "software_fj.log"
    logger = LoggerArchivo("software_fj.log")
    # Creamos el sistema principal, pasándole el registrador
    sistema = SistemaSoftwareFJ(logger)

    # Primero ejecutamos las 12 operaciones automáticas de prueba
    ejecutar_simulacion_automatica(sistema)
    # Luego abrimos el menú interactivo para que el usuario use el sistema
    ejecutar_menu_interactivo(sistema, logger.ruta_archivo)
