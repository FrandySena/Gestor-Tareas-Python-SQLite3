CREATE TABLE IF NOT EXISTS GestorTareas ( 
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NombreTarea VARCHAR(100), 
    Descripcion VARCHAR(500), 
    FechaInicio DATE, 
    FechaFin DATE, 
    Estado VARCHAR(50), 
    Prioridad VARCHAR(20), 
    Responsable VARCHAR(100)
);
