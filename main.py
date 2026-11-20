from logger import LoggerArchivo
from gestor import SistemaSoftwareFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import ErrorSoftwareFJ


def ejecutar_simulacion_automatica(sistema: SistemaSoftwareFJ) -> None:
    """
    Ejecuta 12 operaciones completas (válidas e inválidas) demostrando
    polimorfismo, sobrecarga de costos, control de estados y manejo de excepciones.
    """
    print("=" * 65)
    print(" INICIO DE SIMULACIÓN AUTOMÁTICA - SOFTWARE FJ (12 OPERACIONES)")
    print("=" * 65)

    # 1. Registro válido de cliente
    print("\n[Op 1] Registro de cliente válido (C001):")
    c1 = sistema.registrar_cliente("C001", "Laura Martínez", "1020304050", "laura@softwarefj.com", "3001234567")
    if c1:
        print(f"  OK -> {c1}")

    # 2. Registro inválido de cliente (correo y teléfono mal formados)
    print("\n[Op 2] Registro de cliente inválido (C002 - correo incorrecto):")
    sistema.registrar_cliente("C002", "Carlos Ruiz", "98765432", "correo_invalido", "3109876543")

    # 3. Registro de segundo cliente válido
    print("\n[Op 3] Registro de cliente válido (C003):")
    c3 = sistema.registrar_cliente("C003", "Andrés Gómez", "80112233", "andres.gomez@empresa.co", "+573152223344")
    if c3:
        print(f"  OK -> {c3}")

    # 4. Creación válida de 3 servicios especializados (Polimorfismo)
    print("\n[Op 4] Creación y registro de 3 servicios válidos:")
    servicios_validos = [
        ReservaSala("S001", "Sala Innovación", 80000.0, capacidad=12, tiene_proyector=True),
        AlquilerEquipo("S002", "Workstation Dell Precision", 35000.0, tipo_equipo="Portátil CAD", deposito_garantia=50000.0),
        AsesoriaEspecializada("S003", "Arquitectura Cloud", 120000.0, especialidad="DevOps", nivel_complejidad="avanzado")
    ]
    for srv in servicios_validos:
        if sistema.registrar_servicio(srv):
            print(f"  OK -> {srv}")

    # 5. Creación inválida de servicio (tarifa negativa y nivel inválido)
    print("\n[Op 5] Intento de creación de servicio inválido (tarifa negativa):")
    try:
        srv_invalido = ReservaSala("S004", "Sala Error", -50000.0, capacidad=5)
        sistema.registrar_servicio(srv_invalido)
    except ErrorSoftwareFJ as error:
        sistema.registrar_error_externo(error, contexto="Creación de servicio S004")

    # 6. Creación inválida de asesoría (nivel de complejidad inexistente)
    print("\n[Op 6] Intento de creación de asesoría con nivel inválido:")
    try:
        asesoria_err = AsesoriaEspecializada("S005", "Asesoría IA", 100000.0, especialidad="ML", nivel_complejidad="experto")
        sistema.registrar_servicio(asesoria_err)
    except ErrorSoftwareFJ as error:
        sistema.registrar_error_externo(error, contexto="Creación de servicio S005")

    # 7. Reserva exitosa + Confirmación con impuesto y descuento (Sobrecarga de calcular_costo)
    print("\n[Op 7] Reserva válida R001 (Sala S001) y confirmación con IVA 19% y descuento 10%:")
    r1 = sistema.crear_reserva("R001", "C001", "S001", duracion=3)
    if r1:
        total = sistema.confirmar_reserva("R001", tasa_impuesto=0.19, descuento=0.10)
        if total is not None:
            print(f"  OK -> {r1}")

    # 8. Intento de reservar un servicio que ya no está disponible
    print("\n[Op 8] Intento de confirmar reserva R002 sobre sala S001 ya ocupada:")
    r2 = sistema.crear_reserva("R002", "C003", "S001", duracion=2)
    if r2:
        sistema.confirmar_reserva("R002")

    # 9. Intento de confirmación con parámetro de cálculo inconsistente (descuento > 100%)
    print("\n[Op 9] Intento de confirmar reserva R003 con descuento inválido (1.5 -> 150%):")
    r3 = sistema.crear_reserva("R003", "C003", "S002", duracion=4)
    if r3:
        sistema.confirmar_reserva("R003", tasa_impuesto=0.19, descuento=1.5)

    # 10. Confirmación exitosa de R003 con recargo adicional y posterior procesamiento
    print("\n[Op 10] Confirmación correcta de R003 (Equipo S002) con recargo y procesamiento:")
    total_r3 = sistema.confirmar_reserva("R003", tasa_impuesto=0.19, descuento=0.05, recargo_adicional=10000.0)
    if total_r3 is not None and sistema.procesar_reserva("R003"):
        print(f"  OK -> {r3}")

    # 11. Intento de cancelar una reserva ya procesada (Operación no permitida)
    print("\n[Op 11] Intento de cancelar reserva R003 que ya fue procesada:")
    sistema.cancelar_reserva("R003")

    # 12. Creación, confirmación y cancelación válida de asesoría (libera el servicio)
    print("\n[Op 12] Creación, confirmación y cancelación controlada de R004 (Asesoría S003):")
    r4 = sistema.crear_reserva("R004", "C001", "S003", duracion=2)
    if r4:
        sistema.confirmar_reserva("R004", tasa_impuesto=0.0)
        if sistema.cancelar_reserva("R004"):
            print(f"  OK -> {r4}")

    print("\n" + "=" * 65)
    print(" SIMULACIÓN FINALIZADA SIN INTERRUPCIONES (Revise software_fj.log)")
    print("=" * 65)


# --- Utilidades para el Menú Interactivo ---

def leer_flotante(mensaje: str, valor_por_defecto: float = None) -> float:
    while True:
        entrada = input(mensaje).strip()
        if entrada == "" and valor_por_defecto is not None:
            return valor_por_defecto
        try:
            return float(entrada)
        except ValueError:
            print("  [AVISO] Ingrese un número válido.")


def leer_entero(mensaje: str) -> int:
    while True:
        try:
            return int(input(mensaje).strip())
        except ValueError:
            print("  [AVISO] Ingrese un número entero válido.")


def menu_registrar_servicio(sistema: SistemaSoftwareFJ) -> None:
    print("\nTipos de servicio: 1. Sala | 2. Equipo | 3. Asesoría")
    tipo = input("Seleccione tipo (1-3): ").strip()
    id_srv = input("ID del servicio: ").strip()
    nombre = input("Nombre del servicio: ").strip()
    tarifa = leer_flotante("Tarifa base: ")

    try:
        if tipo == "1":
            capacidad = leer_entero("Capacidad de personas: ")
            proyector = input("¿Tiene proyector? (s/n): ").strip().lower() == "s"
            srv = ReservaSala(id_srv, nombre, tarifa, capacidad, proyector)
        elif tipo == "2":
            tipo_eq = input("Tipo de equipo: ").strip()
            deposito = leer_flotante("Depósito de garantía (Enter para 0): ", 0.0)
            srv = AlquilerEquipo(id_srv, nombre, tarifa, tipo_eq, deposito)
        elif tipo == "3":
            esp = input("Especialidad: ").strip()
            nivel = input("Nivel (basico/intermedio/avanzado): ").strip()
            srv = AsesoriaEspecializada(id_srv, nombre, tarifa, esp, nivel)
        else:
            print("  [AVISO] Tipo de servicio no válido.")
            return

        if sistema.registrar_servicio(srv):
            print(f"  Servicio registrado: {srv}")
    except ErrorSoftwareFJ as error:
        sistema.registrar_error_externo(error, contexto="Registro manual de servicio")


def mostrar_logs(ruta_archivo: str) -> None:
    print(f"\n--- CONTENIDO DE {ruta_archivo} ---")
    try:
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            print(contenido if contenido else "(Archivo vacío)")
    except OSError as error:
        print(f"No se pudo leer el archivo de logs: {error}")


def ejecutar_menu_interactivo(sistema: SistemaSoftwareFJ, ruta_log: str) -> None:
    while True:
        print("\n" + "-" * 45)
        print(" MENÚ INTERACTIVO - SOFTWARE FJ")
        print("-" * 45)
        print("1. Registrar cliente")
        print("2. Registrar servicio")
        print("3. Crear reserva")
        print("4. Confirmar reserva")
        print("5. Procesar reserva")
        print("6. Cancelar reserva")
        print("7. Listar clientes, servicios y reservas")
        print("8. Ver archivo de logs")
        print("0. Salir")

        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            id_cli = input("ID Cliente: ").strip()
            nombre = input("Nombre: ").strip()
            doc = input("Documento (5-15 dígitos): ").strip()
            correo = input("Correo: ").strip()
            tel = input("Teléfono (7-15 dígitos): ").strip()
            cli = sistema.registrar_cliente(id_cli, nombre, doc, correo, tel)
            if cli:
                print(f"  Cliente registrado: {cli}")

        elif opcion == "2":
            menu_registrar_servicio(sistema)

        elif opcion == "3":
            id_res = input("ID Reserva: ").strip()
            id_cli = input("ID Cliente: ").strip()
            id_srv = input("ID Servicio: ").strip()
            duracion = leer_flotante("Duración (horas): ")
            res = sistema.crear_reserva(id_res, id_cli, id_srv, duracion)
            if res:
                print(f"  Reserva creada: {res}")

        elif opcion == "4":
            id_res = input("ID Reserva a confirmar: ").strip()
            imp = leer_flotante("Tasa impuesto 0-1 (Enter para 0.19): ", 0.19)
            desc = leer_flotante("Descuento 0-1 (Enter para 0.0): ", 0.0)
            rec = leer_flotante("Recargo adicional (Enter para 0.0): ", 0.0)
            total = sistema.confirmar_reserva(id_res, imp, desc, rec)
            if total is not None:
                print(f"  Reserva confirmada. Total a pagar: ${total:,.2f}")

        elif opcion == "5":
            id_res = input("ID Reserva a procesar: ").strip()
            if sistema.procesar_reserva(id_res):
                print("  Reserva procesada y servicio liberado.")

        elif opcion == "6":
            id_res = input("ID Reserva a cancelar: ").strip()
            if sistema.cancelar_reserva(id_res):
                print("  Reserva cancelada correctamente.")

        elif opcion == "7":
            print("\n--- CLIENTES ---")
            for c in sistema.clientes:
                print(f"  [{c.identificador}] {c}")
            print("\n--- SERVICIOS ---")
            for s in sistema.servicios:
                print(f"  {s}")
            print("\n--- RESERVAS ---")
            for r in sistema.reservas:
                print(f"  {r}")

        elif opcion == "8":
            mostrar_logs(ruta_log)

        elif opcion == "0":
            print("Cerrando Sistema Software FJ. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    logger = LoggerArchivo("software_fj.log")
    sistema = SistemaSoftwareFJ(logger)

    ejecutar_simulacion_automatica(sistema)
    ejecutar_menu_interactivo(sistema, logger.ruta_archivo)
