# Clase que representa a un profesor
class Profesor:
    def __init__(self, id, nombre, apellido, materia, codigo):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.materia = materia
        self.codigo = codigo

# Clase que representa a un estudiante
class Estudiante:
    def __init__(self, id, nombre, apellido, notas, materia, profesor):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.notas = notas
        self.materia = materia
        self.profesor = profesor
        self.promedio = self._calcular_promedio()
        self.debe_recuperar = self.promedio < 4
        self.promocionado = self.promedio >= 7
        self.asistencia_completa = all(nota != -1 for nota in notas)

    def _calcular_promedio(self):
        notas_validas = [nota for nota in self.notas if nota != -1]
        if len(notas_validas) != 3:
            return 0
        return sum(notas_validas) / 3

# Función para ingresar los datos de un profesor
def ingresar_datos_profesor():
    nombre = input("Ingrese el nombre del profesor: ")
    apellido = input("Ingrese el apellido del profesor: ")
    materia = input("Ingrese la materia que enseña el profesor: ")
    codigo = input("Ingrese el código del profesor: ")
    profesor = Profesor(1, nombre, apellido, materia, codigo)
    print(f"Bienvenido profesor {profesor.nombre} {profesor.apellido} de la materia {profesor.materia}")
    return profesor

# Función para ingresar los datos de los estudiantes
def ingresar_datos_alumno(profesor):
    lista_alumnos = []
    nombres_ingresados = set()
    while True:
        nombre = input("Ingrese el nombre del alumno (o 'salir' para terminar): ")
        if nombre.lower() == "salir":
            break
        apellido = input("Ingrese el apellido del alumno: ")
        nombre_completo = f"{nombre} {apellido}"
        if nombre_completo in nombres_ingresados:
            print("Error: el dato ingresado ya fue cargado.")
            continue
        notas = []
        for i in range(1, 4):
            while True:
                try:
                    nota = float(input(f"Ingrese la nota del parcial {i} para {nombre} {apellido} (usar -1 si estuvo ausente): "))
                    if -1 <= nota <= 10:
                        notas.append(nota)
                        break
                    else:
                        print("Nota inválida. Debe estar entre -1 y 10.")
                except ValueError:
                    print("Entrada inválida. Por favor, ingrese un número.")
        id = len(lista_alumnos) + 1
        alumno = Estudiante(id, nombre, apellido, notas, profesor.materia, profesor)
        lista_alumnos.append(alumno)
        nombres_ingresados.add(nombre_completo)
    return lista_alumnos

# Función para clasificar a los estudiantes según su rendimiento
def clasificar_estudiantes(estudiantes):
    recursantes, finales, promocionados, ausentes, deben_recuperar = [], [], [], [], []

    for estudiante in estudiantes:
        if not estudiante.asistencia_completa:
            ausentes.append(estudiante)
            deben_recuperar.append(estudiante)
        elif estudiante.debe_recuperar:
            deben_recuperar.append(estudiante)
        elif estudiante.promocionado:
            promocionados.append(estudiante)
        elif estudiante.promedio >= 4:
            finales.append(estudiante)
        else:
            recursantes.append(estudiante)

    return recursantes, finales, promocionados, ausentes, deben_recuperar

# Función para mostrar la lista de estudiantes
def mostrar_listado(titulo, estudiantes):
    print(f"\n{titulo}:")
    for estudiante in sorted(estudiantes, key=lambda x: x.nombre):
        print(f"ID: {estudiante.id}, Nombre: {estudiante.nombre}, Apellido: {estudiante.apellido}, Materia: {estudiante.materia}, Profesor: {estudiante.profesor.nombre} {estudiante.profesor.apellido}, Notas: {estudiante.notas}, Promedio: {estudiante.promedio:.2f}, Debe recuperar: {'Sí' if estudiante.debe_recuperar else 'No'}")

# Función principal
def main():
    profesor_actual = ingresar_datos_profesor()
    estudiantes = ingresar_datos_alumno(profesor_actual)
    recursantes, finales, promocionados, ausentes, deben_recuperar = clasificar_estudiantes(estudiantes)
    
    mostrar_listado("Estudiantes que deben recursar", recursantes)
    mostrar_listado("Estudiantes que deben rendir final", finales)
    mostrar_listado("Estudiantes promocionados", promocionados)
    mostrar_listado("Estudiantes ausentes", ausentes)
    mostrar_listado("Estudiantes que deben recuperar", deben_recuperar)

    if promocionados:
        print("\nAlumnos que promocionaron la materia con una nota mayor o igual a 7:")
        for estudiante in promocionados:
            print(f"{estudiante.nombre} {estudiante.apellido} - Promedio: {estudiante.promedio:.2f}")

    if ausentes:
        print("\nAlumnos ausentes que deben recuperar:")
        for estudiante in ausentes:
            print(f"{estudiante.nombre} {estudiante.apellido} - Se ausentó y debe recuperar")

if __name__ == "__main__":
    main()