# prototipo-hmi-lego
Prototipo de una interfaz humano maquina (HMI), con 5 nivele de acceso, ingreso por usuarios con contraseña y mas de 10 funciones modificables a cada nivel de acceso.


## Archivos

- `main.py`: Código .
- `README.md`: Los niveles de acceso son:
Visitante, Operador, Mantenimiento, Genrente y programador
Los usuarios ya creados por defecto se puede cambiar desde el codigo ai como sus niveles correspondientes y sus contrase;as
Para definir un usuario hay que tener cuidado de que este escrito con pura mayuscula y sin espacios
Para la contrase;a se debe tener cuidado que sean solo numeros
Las funciones existententes son: 
Seleccionador_v que es una funcion limitada de seleccion de cubos de color en la cual solo se puede iniciar y pausar
Seleccionador la funcion completa de seleccion de ccubos que permite reiniciar el conteo
Empaquetador segun los datos prefijados llena los contenedores con la cantidad de cubos de cada color ya fijados puedes iniciar pausar y reiniciar
Ver_info en esta funcion puedes ver la informacion de cada colo de cubo registrado (cada cubo simula ser un tipo de te con los atributos de color, sabor y marca)
Modificar configuracion permite cambiar la informacion de los cubos registrados y de las funciones seleccionador y empaquetador
Verificar estado te permite accionar manualmente las funciones mecanicas
Horas te muestra las horas que lleva encendido el bloque
Cambiar acceso te permite cambiar el nivel de acceso de un usuario o a todo un nivel ccambiar las funciones a las que puede o no ingresar
Cambiar contra te permmite cambiar la contrase;a de un usuario
Crear user te permite crear un usuario nuevo
Reportes puedes ver la cantidad de acciones que se realizaron desde el encendido y tambien tiee la funcion de guardar reporte
En los reportes guardados tiene formato definido de "reporte" y seguido a eso los segundos transcurridos desde el inicio y un texto ingresado desde el bloque
Para poder leer los reportes guardados debes conectar el bloque ev3 a la computadora y enlazarlos desde shell
Para esto escribes en power shell:
ssh robot@ev3dev.local
te pedira contrase;a que por defecto generalmente es "maker"
Y posterior a eso en otra terminal de power shell usando el comando de scp debes copiar los archivos dentro de la carpeta de tu proyecto en el ev3 a un diretorio en tu computadora



## Autor

Alvaro Saavedra