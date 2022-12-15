# Grupo Rojo Ingenieria Web

Proyecto final de Ingenieria Web. Ingenieria de la Salud. Universidad de Malaga

----

# Autores

- Alejandro Dominguez Recio
- Hugo Avalos de Rorthais
- Rosario Garcia Morales
- Laura Nuñez Jimenez
- Jesus Aldana Martın

----
# Instalacion

Para ejecutar la aplicacion es suficiente instalando todas las librerias indicadas en el archivo requirements.txt . Las principales librerias utilizadas son:

- FLASK
- SQLALCHEMY

---
# Funcionalidades

Para acceder a la aplicacion utilizar los siguientes parametros:
- Usuario = admin
- Contraseña = admin

Desde ahi podemos ver el resto de cuenta registradas y como acceder a la vista del medico.
Todas las tablas se pueden ordenar haciendo click en la columna.

## Administrador

Desde la vista del administrador se puede añadir y visualizar los usuarios, las tareas y los robots con los que se trabaja en el hospital. Ademas se pueden eliminar los usuarios que dejen de trabajar con la app, asi como editar aquellas tareas que con el tiempo se vayan modificando. Los robots solo se podran cambiar desde el codigo fuente, ya que no deberia de ser frecuente.

Desde esta vista tambien podemos los problemas reportados por los medicos.

## Medico

Desde la vista del médico nos vamos a encontrar una tabla donde poemos ver los robots introducidos por el tecnico. Cada robot posee un estado en el que se encuentra siendo este "Disponible" u "Ocupado" en caso de estar o no realziando una tarea. El medico puede asignarle a los robots disponibles una tarea predefinida.

Cualquier problema tecnico mediante el boton de enviar incidencias se puede reportar al administrador.

### Disclaimer

El tiempo estimado para las tareas es inventado y esta puesto como si duraran 1 minuto aproximadamente (tras pasar este tiempo se actualiza a disponible el estado del robot). 

La vista de cada robot esta en proceso. En ella se espera mostrar una descripcion del robot en cuestion asi como una imagen del mismo.



