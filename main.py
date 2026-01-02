import datetime 
import sqlite3

conn = sqlite3.connect("GestorTareas.db")
cursor = conn.cursor()

with open('GestorTareas.sql', 'r', encoding='utf-8') as f: # Cargar el script SQL
    sql_script = f.read()
    cursor.executescript(sql_script)
conn.commit()

def agregar_Tarea():
    # Solicitar datos de la tarea al usuario
    nombreT = input("Introduce el nombre de la tarea: ")
    descripcionT = input("Introduce la descripción de la tarea: ")

    while True:

        print("\n" + "=" * 80)
        print("Introduce la prioridad de la tarea (Alta, Media, Baja)")
        print("=" * 80)
        print("1 - Alta")
        print("2 - Media")
        print("3 - Baja")
        print("-" * 80)
        print()

        opc = input("Introduce la prioridad de la tarea: ")
        if opc == "1":
            prioridadT = "Alta"
            break
        elif opc == "2":
            prioridadT = "Media"
            break
        elif opc == "3":
            prioridadT = "Baja"
            break
        else:
            print("Opción inválida. Introduce 1, 2 o 3.")
            continue

    fechaHoy = datetime.datetime.today().strftime("%Y-%m-%d")
    fechaInicioT = datetime.datetime.strptime(fechaHoy, "%Y-%m-%d").date()

    while True:
        fechaT = input("Introduce la fecha de finalización de la tarea YYYY-MM-DD (año-mes-dia): ")

        try:
            fechaFinT = datetime.datetime.strptime(fechaT, "%Y-%m-%d").date()

            if fechaFinT < fechaInicioT:
                print("La fecha para realizar la tarea no puede ser inferior a la fecha actual.")
                continue
            fechaFinT = fechaT
            break

        except ValueError:
            print("La fecha debe seguir el formato YYYY-MM-DD (año-mes-dia)")

    estadoT = "Pendiente"
    responsableT = input("Introduce el responsable de la tarea: ")

    cursor.execute("""
        INSERT INTO GestorTareas (NombreTarea, Descripcion, Prioridad, FechaInicio, FechaFin, Estado, Responsable)
        VALUES (?,?,?,?,?,?,?) """, (nombreT, descripcionT, prioridadT, fechaInicioT, fechaFinT, estadoT, responsableT))
    conn.commit()
    print("Se ha insertado una tarea en la base de datos")

def mostrarTareas():
    # Mostrar todas las tareas de la base de datos
    cursor.execute("SELECT * FROM GestorTareas")
    tareas = cursor.fetchall()

    if not tareas:
        print("No hay tareas en la base de datos\n")
        return

    print("\n" + "=" * 80)
    print("TAREAS EN LA BASE DE DATOS")
    print("=" * 80)
    for tarea in tareas:
        print(f"ID: {tarea[0]}")
        print(f"  Nombre: {tarea[1]}")
        print(f"  Descripción: {tarea[2]}")
        print(f"  Fecha Inicio: {tarea[3]}")
        print(f"  Fecha Fin: {tarea[4]}")
        print(f"  Estado: {tarea[5]}")
        print(f"  Prioridad: {tarea[6]}")
        print(f"  Responsable: {tarea[7]}")
        print("-" * 80)
    print()

def mostrarTareasNombre():
    # Mostrar tareas por nombre de la base de datos
    while True:
        nombreT = input("Introduce el nombre de la tarea que deseas buscar: ")
        cursor.execute("SELECT * FROM GestorTareas WHERE NombreTarea = ?", (nombreT, ))
        tareas = cursor.fetchall()

        if tareas:
            for tarea in tareas:
                print("\n" + "=" * 80)
                print("TAREAS EN LA BASE DE DATOS")
                print("=" * 80)
                print(f"ID: {tarea[0]}")
                print(f"  Nombre: {tarea[1]}")
                print(f"  Descripción: {tarea[2]}")
                print(f"  Fecha Inicio: {tarea[3]}")
                print(f"  Fecha Fin: {tarea[4]}")
                print(f"  Estado: {tarea[5]}")
                print(f"  Prioridad: {tarea[6]}")
                print(f"  Responsable: {tarea[7]}")
                print("-" * 80)
            print()
            break
        else:
            print(f"No existe tarea con nombre {nombreT}\n")
            respuesta = input("¿Desea intentar con otro nombre? (s/n): ").lower()
            if respuesta != 's':
                break
            else:
                continue

def mostrarTareasEstado():
    # Mostrar tareas por estado de la base de datos
    while True:
        print("\n" + "=" * 80)
        print("Introduce el estado de la tarea que desea buscar (Pendiente, En Progreso, Completada)")
        print("=" * 80)
        print("1 - Pendiente")
        print("2 - En Progreso")
        print("3 - Completada")
        print("-" * 80)
        print()

        opc = input("Introduce el estado de la tarea: ")

        if opc == "1":
            estadoT = "Pendiente"
            break
        elif opc == "2":
            estadoT = "En Progreso"
            break
        elif opc == "3":
            estadoT = "Completada"
            break
        else:
            print("Opción inválida. Introduce 1, 2 o 3.")
            continue

    cursor.execute("SELECT * FROM GestorTareas WHERE Estado = ?", (estadoT, ))
    tareas = cursor.fetchall()

    if tareas:
        for tarea in tareas:
            print("\n" + "=" * 80)
            print("TAREAS EN LA BASE DE DATOS")
            print("=" * 80)
            print(f"ID: {tarea[0]}")
            print(f"  Nombre: {tarea[1]}")
            print(f"  Descripción: {tarea[2]}")
            print(f"  Fecha Inicio: {tarea[3]}")
            print(f"  Fecha Fin: {tarea[4]}")
            print(f"  Estado: {tarea[5]}")
            print(f"  Prioridad: {tarea[6]}")
            print(f"  Responsable: {tarea[7]}")
            print("-" * 80)
        print()
    else:
        print(f"No existen tareas en el estado: {estadoT}\n")

def actualizar_Tarea():
    # Actualizar una tarea completa o solo el estado de la base de datos
    while True:
        try:
            idTarea = int(input("Introduce el ID de la tarea que deseas modificar: "))
            cursor.execute("SELECT * FROM GestorTareas WHERE ID = ?",
                           (idTarea, ))
            tarea = cursor.fetchone()

            if not tarea:
                print(f"No existe tarea con ID {idTarea}\n")
                respuesta = input(
                    "¿Desea intentar con otro ID? (s/n): ").lower()
                if respuesta != 's':
                    break
                continue

            print(f"\nTarea actual: ID: {tarea[0]}, Nombre: {tarea[1]}, Estado: {tarea[5]}")

            print("\n¿Qué deseas modificar?")
            print("1. Solo el estado")
            print("2. Todos los campos")
            print("3. Cancelar")

            while True:
                opcion = input("Selecciona una opción (1/2/3): ")
                if opcion == "1":
                    while True:

                        print("\n" + "=" * 80)
                        print("Introduce el nuevo estado (Pendiente, En Progreso, Completada)")
                        print("=" * 80)
                        print("1 - Pendiente")
                        print("2 - En Progreso")
                        print("3 - Completada")
                        print("-" * 80)
                        print()

                        opc = input("Introduce la prioridad de la tarea: ")
                        if opc == "1":
                            estadoT = "Pendiente"
                            break
                        elif opc == "2":
                            estadoT = "En Progreso"
                            break
                        elif opc == "3":
                            estadoT = "Completada"
                            break
                        else:
                            print("Opción inválida. Introduce 1, 2 o 3.")
                            continue

                    cursor.execute("UPDATE GestorTareas SET Estado = ? WHERE ID = ?", (estadoT, idTarea))
                    conn.commit()
                    print("Estado de la tarea actualizado\n")
                    break

                elif opcion == "2":
                    nombreT = input("Introduce el nuevo nombre de la tarea: ")
                    descripcionT = input("Introduce la nueva descripción de la tarea: ")

                    while True:

                        print("\n" + "=" * 80)
                        print("Introduce la prioridad de la tarea (Alta, Media, Baja)")
                        print("=" * 80)
                        print("1 - Alta")
                        print("2 - Media")
                        print("3 - Baja")
                        print("-" * 80)
                        print()

                        opc = input("Introduce la prioridad de la tarea: ")
                        if opc == "1":
                            prioridadT = "Alta"
                            break
                        elif opc == "2":
                            prioridadT = "Media"
                            break
                        elif opc == "3":
                            prioridadT = "Baja"
                            break
                        else:
                            print("Opción inválida. Introduce 1, 2 o 3.")
                            continue

                    fechaFinT = input("Introduce la nueva fecha de finalización (YYYY-MM-DD): ")

                    while True:

                        print("\n" + "=" * 80)
                        print("Introduce el nuevo estado (Pendiente, En Progreso, Completada)")
                        print("=" * 80)
                        print("1 - Pendiente")
                        print("2 - En Progreso")
                        print("3 - Completada")
                        print("-" * 80)
                        print()

                        opc = input("Introduce el estado de la tarea: ")
                        if opc == "1":
                            estadoT = "Pendiente"
                            break
                        elif opc == "2":
                            estadoT = "En Progreso"
                            break
                        elif opc == "3":
                            estadoT = "Completada"
                            break
                        else:
                            print("Opción inválida. Introduce 1, 2 o 3.")
                            continue

                    responsableT = input("Introduce el nuevo responsable de la tarea: ")

                    cursor.execute("""
                      UPDATE GestorTareas 
                      SET NombreTarea = ?, Descripcion = ?, Prioridad = ?, FechaFin = ?, Estado = ?, Responsable = ?
                      WHERE ID = ? """, (nombreT, descripcionT, prioridadT, fechaFinT, estadoT, responsableT, idTarea))
                    conn.commit()
                    print("Tarea modificada exitosamente\n")
                    break

                elif opcion == "3":
                    print("Operación cancelada\n")
                    break
                else:
                    print("Opción inválida\n")
                    continue

            respuesta = input("¿Desea modificar otra tarea? (s/n): ").lower()
            if respuesta != 's':
                break

        except ValueError:
            print("El ID debe ser un número entero\n")
            continue

def eliminar_Tarea():
    # Eliminar una tarea de la base de datos
    while True:
        try:
            idTarea = int(input("Introduce el ID de la tarea que deseas eliminar: "))
            cursor.execute("SELECT * FROM GestorTareas WHERE ID = ?", (idTarea, ))
            tarea = cursor.fetchone()

            if not tarea:
                print(f"No existe tarea con ID {idTarea}\n")
                return

            print(f"\nVas a eliminar: {tarea[1]}")
            confirmacion = input("¿Estás seguro? (s/n): ").lower()

            if confirmacion == 's':
                cursor.execute("DELETE FROM GestorTareas WHERE ID = ?",
                               (idTarea, ))
                conn.commit()
                print("Tarea eliminada exitosamente\n")
                break
            else:
                print("Operación cancelada\n")

        except ValueError:
            print("El ID debe ser un número entero\n")
            continue

def menu_buscar():
    # Menú de búsqueda de tareas
    while True:
        print("\n" + "=" * 80)
        print("🔍 BUSCAR TAREA")
        print("=" * 80)
        print("1. Buscar por nombre")
        print("2. Buscar por estado")
        print("3. Mostrar todas las tareas")
        print("0. Volver al menú principal")
        print("=" * 80)

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            mostrarTareasNombre()
        elif opcion == "2":
            mostrarTareasEstado()
        elif opcion == "3":
            mostrarTareas()
        elif opcion == "0":
            break
        else:
            print("\nOpción inválida. Intenta de nuevo.\n")

def menu_principal():
    # Menú principal del gestor de tareas
    while True:
        print("\n" + "=" * 80)
        print("GESTOR DE TAREAS")
        print("=" * 80)
        print("1. Agregar tarea")
        print("2. Actualizar tarea")
        print("3. Eliminar tarea")
        print("4. Buscar tarea")
        print("0. Salir")
        print("=" * 80)

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_Tarea()
        elif opcion == "2":
            actualizar_Tarea()
        elif opcion == "3":
            eliminar_Tarea()
        elif opcion == "4":
            menu_buscar()
        elif opcion == "0":
            print("\nCerrando gestor de tareas...")
            break
        else:
            print("\nOpción inválida. Intenta de nuevo.\n")

if __name__ == "__main__":
    try:
        menu_principal()
    finally:
        cursor.close()
        conn.close()