#!/usr/bin/env pybricks-micropython
#Importar librerias necesarias 
#Las de pybricks es para el bloque ev3
#_thread genera hilos en paralelo al programa principal
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor,  ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import _thread
#Lo separo por secciones para que este mas organizadito todo, primero es clases luego funiones x, funciones principales
#variables vectores diccionarios y todo eso para que funcione bien el programa
#el monton de try except para verificar que todo este conectado y recien el main() al final
###################################################################################################################################
#Crear las clases necesarias
#Clase usuario
#Atributos de nombre de usuario, contrase;a y nivel 
#Internamente se generaran el resto de atributos que se usan para el menu 
#el menu que genera lo saca comparando el nivel como key del diccionario y de ahi saca el vector auxiliar
#el vector auxiliar son trues y falses que determinan si tiene acceso a un nivel o no y luego en otro vector pega las funciones
class Usuarios:
    def __init__(self, user, contra, nivel="visitante"):
        self.user=user
        self.contra=contra
        self.nivel=nivel
        self.vec_aux=niveles.get(nivel,[])
        self.vec_menu=[]
        for i in range(len(self.vec_aux)):
            if self.vec_aux[i]:
                self.vec_menu.append(vec_ref[i])
        self.vec_menu.append("Salir")

    #se llama a esta funcion en los casos de que se modifica los accesos y cosas asi practicamente actualiza el menu
    def generar_menu(self):
        self.vec_menu.clear()
        for i in range(len(self.vec_aux)):
            if self.vec_aux[i]:
                self.vec_menu.append(vec_ref[i])
        self.vec_menu.append("Salir")
    
    #permite cambiar o mantener el nivel del usuario
    def cambiar_nivel(self):
        reportes.append(["Cambiando: " + self.user, transformar(contador_segundos)])
        op=seleccionar_opcion("Act: {}".format(self.nivel), ["Cambiar", "Listo"])
        if op==0:
            op2=seleccionar_opcion("Nuevo nivel", list_niveles)
            self.nivel=list_niveles[op2]
            self.vec_menu.clear()
            self.vec_aux=niveles.get(self.nivel,[])
            self.generar_menu()
            reportes.append(["Nuevo nivel: " + self.nivel, transformar(contador_segundos)])
            self.cambiar_nivel()
            



#Clase container (para empaquetado)
#recibe como atributos el numero de container y la cantidad de cada color a la que se quiere llegar
#genera una lista de 0 que corresponden a la cantidad actual de cada tipos de cubos 
class Container:
    def __init__(self, numero, b=0, r=0, y=0, o=0):
        self.numero=numero
        self.limite=[b, r, y, o]
        self.act=[0, 0, 0, 0]
    
    def reiniciar(self):
        reportes.append(["Reinicio container "+str(self.numero), transformar(contador_segundos)])
        self.act=[0, 0, 0, 0]

#Clase cubo(para selector y info)
#Inicializo la clase con loos atributos de color, cantidad, sabor y marca 
# (los cubos hacen referencia a cajas de te)
#dependiendo el color se llena el resto de info que son la marca y el sabor del te
#y se genera un contador que empieza en 0
#tammbien predefine a que contenedor se ira cada color, pero se puede cambiar
class Cubo:
    def __init__(self, color, cantidad=0):
        self.color=color
        self.cant=cantidad
        if self.color=='RED':
            self.code=Color.RED
            self.sabor= "Canela"
            self.marca="Windsor"
            self.container=2
        elif self.color=='BLUE':
            self.code=Color.BLUE
            self.sabor= "Menta"
            self.marca="Lipton"
            self.container=3
        elif self.color=='YELLOW':
            self.code=Color.YELLOW
            self.sabor= "Manzanilla"
            self.marca="Supremo"
            self.container=1
        else:
            self.code=None
            self.sabor= ""
            self.marca=""
            self.container=4

    #permite cambiar el container al cual se depositara ese cubo
    def cambiar_container(self):
        self.container=1+seleccionar_opcion("Elije el contenedor",["1", "2", "3", "4"])
        reportes.append(["Cambio "+self.color+"a"+ str(self.container), transformar(contador_segundos)])

    #Muestra informacion de cada tipo sabor y marca el te
    def imprimir_reporte(self):
        reportes.append(["Imprimio reporte "+self.color, transformar(contador_segundos)])
        ev3.screen.draw_text(25, 10, "Te de sabor")
        ev3.screen.draw_text(35, 28, self.sabor)
        ev3.screen.draw_text(40, 46, "Marca")
        ev3.screen.draw_text(30, 64, self.marca)
        ev3.screen.draw_text(20, 82, "Y hay: {}".format(self.cant))
        ev3.screen.draw_text(20, 100, "[Atras]")
    
    #Aumenta el contador 
    def agregar_cubo(self):
        self.cant+=1    

#Funciones x necesarias mas que todo para la hmi y miniprocesos
###################################################################################################################################
#Convierte el tiempo de segundos a un str con formato bonito
def transformar(n):
    aux=n%60
    aux_min=((n-n%60)/60)%60
    aux_hora=(n-n%3600)/3600
    hora =""
    if aux_hora<10:
        hora+="0"
    hora+=str(int(aux_hora))+":"
    if aux_min<10:
        hora+="0"
    hora+=str(int(aux_min))+":"
    if aux<10:
        hora+="0"
    hora+=str(aux)
    return hora

#este lo mando como hilo practicamente al mismo tiempo del main para que en segundo plano vaya contando el tiempo
def contar_tiempo():
    global contador_segundos
    while ejecutando:
        wait(1000)
        contador_segundos += 1

#refresca la pantalla que verifica si todo esta conectado
def actualizar_verificacion():
    ev3.screen.draw_text(0, 10, "S.Color")
    ev3.screen.draw_text(0, 30, "S.Ultra")
    ev3.screen.draw_text(0, 50, "Selector")
    ev3.screen.draw_text(0, 70, "Cinta")
    for i, val in enumerate(vec_verif):
        if val:
            ev3.screen.draw_text(100, 10+20*i, "OK")

#Funcion auxiliar para mostrar teclado en la pantalla y recibir una palabra el n es para ver si usar teclado alfabetico o numerico
#n 1 es para numeros y 0 para alfabeto 
def ingresar_texto(posy,texto, n, posy2=0, text2=""):
    palabra = ""
    fila = 0
    col = 0
    while True:
        ev3.screen.clear()
        ev3.screen.draw_text(0,posy,texto+": " + palabra)
        ev3.screen.draw_text(0, posy2, text2)
        # Mostrar teclado
        for i, fila_teclado in enumerate(teclados[n]):
            linea = ""
            for j, letra in enumerate(fila_teclado):
                if i == fila and j == col:
                    linea += "[" + letra + "]"  # Cursor
                else:
                    linea += " " + letra + " "
            ev3.screen.draw_text(0, 50+i*15,linea)
        
        wait(200)

        while not ev3.buttons.pressed():
            wait(10)
        btn = ev3.buttons.pressed()
        wait(200)

        if Button.UP in btn:
            fila = (fila - 1) % len(teclados[n])
        elif Button.DOWN in btn:
            fila = (fila + 1) % len(teclados[n])
        elif Button.LEFT in btn:
            col = (col - 1) % len(teclados[n][0])
        elif Button.RIGHT in btn:
            col = (col + 1) % len(teclados[n][0])
        elif Button.CENTER in btn:
            letra = teclados[n][fila][col]
            if letra == "OK":
                if palabra=="":
                    palabra="0"
                return palabra
            elif letra == "<":
                palabra = palabra[:-1]  # Borrar último carácter
            elif letra != "":
                palabra += letra


#Funcion auxiliar para el menu
def imprimir(fila, texto, seleccionado):
    if seleccionado:
        ev3.screen.draw_text(0, fila * 20, "-> " + texto)
    else:
        ev3.screen.draw_text(0, fila * 20, "   " + texto)

#Funcion auxiliar para el menu
def mostrar_menu(titulo, opciones, opcion_seleccionada):
    ev3.screen.clear()
    ev3.screen.draw_text(0, 0, titulo)
    for i, opcion in enumerate(opciones):
        imprimir(i + 1, opcion, i == opcion_seleccionada)
    #ev3.screen.update()

#Funcion generica para hacer menus dinamicos
def seleccionar_opcion(titulo, opciones):
    opcion_seleccionada = 0
    mostrar_menu(titulo, opciones, opcion_seleccionada)
    while True:
        botones = ev3.buttons.pressed()
        if Button.UP in botones:
            opcion_seleccionada = (opcion_seleccionada - 1) % len(opciones)
            mostrar_menu(titulo, opciones, opcion_seleccionada)
            wait(300)
        elif Button.DOWN in botones:
            opcion_seleccionada = (opcion_seleccionada + 1) % len(opciones)
            mostrar_menu(titulo, opciones, opcion_seleccionada)
            wait(300)
        elif Button.CENTER in botones:
            ev3.screen.clear()
            ev3.screen.draw_text(0, 70, "Opción selec:")
            ev3.screen.draw_text(0, 90, opciones[opcion_seleccionada])
            ev3.speaker.beep()
            wait(1000)
            return opcion_seleccionada
        wait(50)

#la pantalla de cuanto va de cada tipo en las funciones de selector 
def refresh(texto="[Atras]"):
    ev3.screen.clear()
    for i in range(len(vec_cubos_registrados)):
        ev3.screen.draw_text(0, 10+i*20, "{}:".format(vec_cubos_registrados[i].color))
        ev3.screen.draw_text(140, 10+i*20, vec_cubos_registrados[i].cant)
    ev3.screen.draw_text(0, 90, texto)

#la pantalla de cuantos va de cada color en cada container  de la funcion empaquetador 
#muestra como matriz bien bonito
def refresh_emp():
    ev3.screen.clear()
    ev3.screen.draw_text(0, 0, "C  B  R  Y  O")
    linea=""
    for k, c in enumerate(vec_containers):
        linea=str(c.numero)
        for i in range(4):
            linea= linea + "  "+ str(c.act[i])
        ev3.screen.draw_text(0,20+20*k , linea)
    ev3.screen.draw_text(0, 100, "[Pausar]")

#mueve el selector dependiendo el contenedor al cual corresponda
def mover_selector(container):
    if container == 2:
        wait(3200) 
    elif container == 3:
        wait(1500)
    elif container == 1:
        wait(2100)
    else:
        return
    selector.run_target(400, 360)  # moverse a 360 grados
    wait(10)  # esperar un momento
    if container == 3:
        wait(590)
    selector.run_target(750, 0)    # volver a la posición inicial

#tiene movimientos prefijados para probar manualmente
# la cinta va atras y adelante
#el selector se mueve dependiendo del contenedor que se elija
def probar_comandos():
    reportes.append(["Ingreso a probar comandos", transformar(contador_segundos)])
    op=seleccionar_opcion("Elija motor", ["Cinta", "Seleccionador", "Salir"])
    if op==0:
        while True:
            op2=seleccionar_opcion("Elija sentido", ["Adelante","Atras", "Salir"])
            if op2==2:
                break
            elif op2==0:
                cinta.run(150)
                ev3.screen.draw_text(0, 0,"Probando...")
                wait(5000)
                cinta.run(0)
                ev3.screen.clear()
                ev3.screen.draw_text(0, 0, "Sin errores")
            elif op2==1:
                cinta.run(-150)
                ev3.screen.draw_text(0, 0,"Probando...")
                wait(5000)
                cinta.run(0)
                ev3.screen.clear()
                ev3.screen.draw_text(0, 0, "Sin errores")
            wait(1000)
        probar_comandos()
    elif op==1:
        while True:
            op2=seleccionar_opcion("Elija pos", ["1", "2", "3", "Salir"])
            if op2==3:
                break
            mover_selector(op+1)
            ev3.screen.clear()
            ev3.screen.draw_text(0, 0, "Sin errores")
        probar_comandos()
        
#eliges un color de cubo y cambias el contenedor al cual se depositara
def modificar_containers():
    reportes.append(["Ingreso a modificar containers", transformar(contador_segundos)])
    list_aux=[]
    for  cubo in vec_cubos_registrados:
        list_aux.append(cubo.color)
    list_aux.append("Salir")
    op=seleccionar_opcion("Cubos", list_aux)
    if list_aux[op]!=list_aux[-1]:
        vec_cubos_registrados[op].cambiar_container()
        modificar_containers()

#Cambias algun limite de color de algun contenedor 
#Tiene un menu de ver actual que te muestra la matriz de cantidades imites
#y de modificar donde te pedira mediante menus que elijas el contenedor y el color que quieres cambiar 
def modificar_cant_containers():
    reportes.append(["Ingreso a modificar cant containers", transformar(contador_segundos)])
    op= seleccionar_opcion("Elige", ["Ver act", "Modificar", "Salir"])
    if op==0:
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, "C  B  R  Y  O")
        linea=""
        for k, c in enumerate(vec_containers):
            linea=str(c.numero)
            for i in range(4):
                linea=linea+"  "+str(c.limite[i])
            ev3.screen.draw_text(0,20+20*k , linea)
        ev3.screen.draw_text(0, 100, "[Atras]")
        while not Button.CENTER in ev3.buttons.pressed():
            continue
        wait(1000)
    elif op==1:
        op2=seleccionar_opcion("Contenedor", ["1", "2", "3"])
        op3=seleccionar_opcion("Tipo", ["Azul", "Rojo", "Amarillo","Def"])
        new_cant=ingresar_texto(15, "Cant: ", 1 ,0, "Act: "+ str(vec_containers[op2].limite[op3]))
        vec_containers[op2].limite[op3]=int(new_cant)
        ev3.screen.clear()
        ev3.screen.draw_text(0, 50, "Modificado")
        wait(1000)
    if op!=2:
        modificar_cant_containers()

#Sirve para cambiar la informacion de los cubos, solo el sabor y la marca
def modificar_info():
    reportes.append(["Ingreso a modificar info", transformar(contador_segundos)])
    op=seleccionar_opcion("Tipo", ["Azul", "Rojo", "Amarillo", "Salir"])
    if op!=3:
        op2=seleccionar_opcion("Info", ["Sabor", "Marca"])
        if op2==0:
            vec_cubos_registrados[op+1].sabor=ingresar_texto(15, "New", 0 ,0, "Act: "+vec_cubos_registrados[op+1].sabor)
        elif op2==1:
            vec_cubos_registrados[op+1].marca=ingresar_texto(15, "New", 0 ,0, "Act: "+vec_cubos_registrados[op+1].marca)
        ev3.screen.clear()
        ev3.screen.draw_text(0, 50, "Modificado")
        wait(1000)
        modificar_info()

#Genera un archivo de texto donde se guardan todas las acciones con la hora en la que se realizaron
#si existe un archivo con el mismo nombre se reescribe
#pero para evitar eso el formato del normbre de archivo es reporte_ el segundo en el que se guarda y te permite escribir el final manualmente
def guardar_reporte():
    nombre_archivo="Reporte_"+str(contador_segundos)+"_"+ingresar_texto(0, "Name", 0)+".txt"
    with open(nombre_archivo, "w") as archivo:
        archivo.write("Reporte:\n")
        for rep in reportes:
            archivo.write(rep[1]+"   "+rep[0]+"\n")
    ev3.screen.clear()
    ev3.screen.draw_text(0, 0, "Reporte generado")
    wait(1000)

#Ahora las funciones principales
###################################################################################################################################
#Ves el sabor la marca y la cantidad del color de cbo que elijas
def ver_info():
    reportes.append(["Ingreso a ver info", transformar(contador_segundos)])
    op=seleccionar_opcion("Clase", ["Azul", "Rojo", "Amarillo", "Atras"])
    ev3.screen.clear()
    if op!=3:       
        vec_cubos_registrados[op+1].imprimir_reporte()
        reportes.append(["Ver info "+ str(vec_cubos_registrados[op+1].color), transformar(contador_segundos)])
        while not Button.CENTER in ev3.buttons.pressed():
            continue
        ev3.screen.clear()
        wait(500)
        ver_info()

#Selector de cubos segun color basico, solo te permite pausarlo especial para nivel visitante
def selector_v():
    reportes.append(["Ingreso a selector_v", transformar(contador_segundos)])
    cinta.run(150)
    selector.run_target(750,0)
    refresh()
    while not Button.CENTER in ev3.buttons.pressed():
        #Se mantiene en bucle infinito hasta que se aprete el boton del centro del ev3 
        #Verifica si hay un objeto frente al sensor
        distance = ultrasonic.distance()
        if distance <=55:
            wait(100)
            #Mide el color del objeto
            color_act=s_color.color()
            #Si el color corresponde a uno de los predefinidos crea un hilo para el seleccionador 
            identificado=False
            for i in range(len(vec_cubos_registrados)):
                if color_act==vec_cubos_registrados[i].code:
                    identificado=True
                    _thread.start_new_thread(mover_selector, (vec_cubos_registrados[i].container,))
                    vec_cubos_registrados[i].agregar_cubo()
                    refresh()
                    break
            #Si es un color extra;o salta una alarma y lo deja pasar
            if not identificado:
                vec_cubos_registrados[0].agregar_cubo()
                refresh()
                ev3.speaker.beep()
                wait(50)
                ev3.speaker.beep()
                wait(50)
                ev3.speaker.beep()
                wait(50)
            wait(1000)
    #Al precionar el boton central del ev3 se detiene el proceso
    cinta.run(0)
    wait(2000) 
    text=""
    for c in vec_cubos_registrados:
        text=text+str(c.cant)+" "
    reportes.append(["Pauso selector_v: "+ text, transformar(contador_segundos)])
    ev3.screen.clear()
    ev3.screen.clear()

#la version completa de selector en la cual puedes reiniciar el contador
def selector_fun():
    reportes.append(["Ingreso a selector", transformar(contador_segundos)])
    cinta.run(150)
    selector.run_target(750,0)
    refresh("[Pausar]")
    while not Button.CENTER in ev3.buttons.pressed():
        #Se mantiene en bucle infinito hasta que se aprete el boton del centro del ev3 
        #Verifica si hay un objeto frente al sensor
        distance = ultrasonic.distance()
        if distance <=55:
            wait(100)
            #Mide el color del objeto
            color_act=s_color.color()
            #Si el color corresponde a uno de los predefinidos crea un hilo para el seleccionador 
            identificado=False
            for i in range(len(vec_cubos_registrados)):
                if color_act==vec_cubos_registrados[i].code:
                    identificado=True
                    _thread.start_new_thread(mover_selector, (vec_cubos_registrados[i].container,))
                    vec_cubos_registrados[i].agregar_cubo()
                    refresh("[Pausar]")
                    break
            #Si es un color extra;o salta una alarma y lo deja pasar
            if not identificado:
                vec_cubos_registrados[0].agregar_cubo()
                refresh("[Pausar]")
                ev3.speaker.beep()
                wait(50)
                ev3.speaker.beep()
                wait(50)
                ev3.speaker.beep()
                wait(50)
            wait(1000)
    #Al precionar el boton central del ev3 se detiene el proceso
    cinta.run(0)
    wait(2000)
    text=""
    for c in vec_cubos_registrados:
        text=text+str(c.cant)+" "
    reportes.append(["Pauso selector act: "+ text, transformar(contador_segundos)])
    ev3.screen.clear()
    op=seleccionar_opcion("Menu", ["Continuar", "Reiniciar", "Salir" ])
    if op==0:
        selector_fun()
    #Reestablece la cantidad de todos los cubos a 0
    elif op==1:
        for i in range(len(vec_cubos_registrados)):
            vec_cubos_registrados[i].cant=0
        ev3.screen.clear()
        ev3.screen.draw_text(10, 10, "Reiniciado")
        wait(1000)
        ev3.screen.clear()
        op2=seleccionar_opcion("Menu", ["Continuar", "Salir" ])
        if op2==0:
            selector_fun()

#la funcion empaquetadora que distribuye los cubos segun los requerimientos de los containers
def empaquetado():
    reportes.append(["Ingreso a empaquetado", transformar(contador_segundos)])
    cinta.run(150)
    selector.run_target(750,0)
    refresh_emp()
    while not Button.CENTER in ev3.buttons.pressed():
        #Se mantiene en bucle infinito hasta que se aprete el boton del centro del ev3 
        #Verifica si hay un objeto frente al sensor
        distance = ultrasonic.distance()
        if distance <=55:
            wait(100)
            #Mide el color del objeto
            color_act=s_color.color()
            if color_act==Color.BLUE:
                for c in vec_containers:
                    if c.limite[0]>c.act[0]:
                        _thread.start_new_thread(mover_selector, (c.numero,))
                        c.act[0]+=1
                        break
            elif color_act==Color.RED:
                for c in vec_containers:
                    if c.limite[1]>c.act[1]:
                        _thread.start_new_thread(mover_selector, (c.numero,))
                        c.act[1]+=1
                        break
            elif color_act==Color.YELLOW:
                for c in vec_containers:
                    if c.limite[2]>c.act[2]:
                        _thread.start_new_thread(mover_selector, (c.numero,))
                        c.act[2]+=1
                        break
            else:
                for c in vec_containers:
                    if c.limite[3]>c.act[3]:
                        _thread.start_new_thread(mover_selector, (c.numero,))
                        c.act[3]+=1
                        break
            refresh_emp()
            wait(1000)
        if (vec_containers[0].limite==vec_containers[0].act and
            vec_containers[1].limite==vec_containers[1].act and
            vec_containers[2].limite==vec_containers[2].act):
            reportes.append(["Completo empaquetado", transformar(contador_segundos)])
            break                  
    cinta.run(0)
    wait(2000)
    reportes.append(["Pausa empaquetado", transformar(contador_segundos)])
    for c in vec_containers:
        text=""
        text=str(c.numero)+" "+str(c.act[0])+" "+str(c.act[1])+" "+str(c.act[2])+" "+str(c.act[3])
        reportes.append(["Finalizo container"+text, transformar(contador_segundos)])
    ev3.screen.clear()
    if (vec_containers[0].limite==vec_containers[0].act and
        vec_containers[1].limite==vec_containers[1].act and
        vec_containers[2].limite==vec_containers[2].act):
        op=seleccionar_opcion("Menu", ["Reiniciar", "Salir" ])
        if op==0:
            for c in vec_containers:
                c.reiniciar()
            ev3.screen.clear()
            ev3.screen.draw_text(10, 10, "Reiniciado")
            wait(1000)
            ev3.screen.clear()
            op2=seleccionar_opcion("Menu", ["Continuar", "Salir" ])
            if op2==0:
                empaquetado()
    else:    
        op=seleccionar_opcion("Menu", ["Continuar", "Reiniciar", "Salir" ])
        if op==0:
            empaquetado()
        elif op==1:
            for c in vec_containers:
                c.reiniciar()
            ev3.screen.clear()
            ev3.screen.draw_text(10, 10, "Reiniciado")
            wait(1000)
            ev3.screen.clear()
            op2=seleccionar_opcion("Menu", ["Continuar", "Salir" ])
            if op2==0:
                empaquetado()

#Menu del reporte te da dos opciones o guardarlo o ver la cantidad de acciones hasta el momento
def report():
    reportes.append(["Ingreso a reporte", transformar(contador_segundos)])
    ev3.screen.clear()
    op=seleccionar_opcion("Elija una opcion",["Reportes", "Guardar", "Salir"])
    if op==0:
        reportes.append(["Ingreso a ver cant report", transformar(contador_segundos)])
        ev3.screen.clear()
        ev3.screen.draw_text(0, 10, "Cantidad de acciones")
        ev3.screen.draw_text(50, 30, str(len(reportes)))
        ev3.screen.draw_text(20, 70, "[Salir]")
        while not Button.CENTER in ev3.buttons.pressed():
            continue
        ev3.screen.clear()
        wait(500)
        report()
    elif op==1:
        guardar_reporte()
        report()

#menu para verificar los motores, tiene las opciones de verificar que revisa las conexiones y la de probar (manualmente)
def verificar_estado():
    reportes.append(["Ingreso a verificar estado", transformar(contador_segundos)])
    op=seleccionar_opcion("Elija una opcion",["Verificar", "Probar", "Salir"])
    if op==0:
        reportes.append(["Ingreso a verificar", transformar(contador_segundos)])
        ev3.screen.clear()
        ev3.screen.draw_text(0, 10, "Selector")
        ev3.screen.draw_text(0, 30, "Cinta")
        if vec_verif[2]:
            ev3.screen.draw_text(80, 10, "OK")
        if vec_verif[3]:
            ev3.screen.draw_text(80, 30, "OK")
        ev3.screen.draw_text(20, 70, "[Salir]")
        while not Button.CENTER in ev3.buttons.pressed():
            try:
                selector = Motor(Port.A)
                vec_verif[2]=True
            except OSError:
                selector = None
                vec_verif[2]=False
            wait(100)
            ev3.screen.clear()
            ev3.screen.draw_text(0, 10, "Selector")
            ev3.screen.draw_text(0, 30, "Cinta")
            if vec_verif[2]:
                ev3.screen.draw_text(80, 10, "OK")
            if vec_verif[3]:
                ev3.screen.draw_text(80, 30, "OK")
            ev3.screen.draw_text(20, 70, "[Salir]")
            try:
                cinta = Motor(Port.B)
                vec_verif[3]=True
            except OSError:
                cinta = None
                vec_verif[3]=False
            wait(100)
            ev3.screen.clear()
            ev3.screen.draw_text(0, 10, "Selector")
            ev3.screen.draw_text(0, 30, "Cinta")
            if vec_verif[2]:
                ev3.screen.draw_text(80, 10, "OK")
            if vec_verif[3]:
                ev3.screen.draw_text(80, 30, "OK")
            ev3.screen.draw_text(20, 70, "[Salir]")
        ev3.screen.clear()
        wait(500)
        verificar_estado()
    elif op==1:
        probar_comandos()
        verificar_estado()

#solo ves las horas trabajadas (en mi mente era util)
def horas_trabajadas():
    reportes.append(["Ingreso a horas trabajadas", transformar(contador_segundos)])
    ev3.screen.clear()
    hora=transformar(contador_segundos)
    ev3.screen.draw_text(0, 30, "Las horas trabajadas son: ")
    ev3.screen.draw_text(0, 50, hora)
    ev3.screen.draw_text(0, 70, "[Salir]")
    while not Button.CENTER in ev3.buttons.pressed():
        continue
    wait(1000)

#Menu para modificar la info que quieras, tiene como opciones modificar los ajustes de selector, empaquetador y la infode los cubos
def modificar_configuraciones():
    reportes.append(["Ingreso a modificar configuraciones", transformar(contador_segundos)])
    op=seleccionar_opcion("Elija la funcion",["Selector", "Empaquetador", "Info", "Salir"])
    if op==0:
        modificar_containers()
        modificar_configuraciones()
    elif op==1:
        modificar_cant_containers()
        modificar_configuraciones()
    elif op==2:
        modificar_info()
        modificar_configuraciones()

#tu eliges si cambiar por nivel osea agregar o quitar accesos a un nivel o bien elegir un usuario y cambiarle su nivel
def cambiar_accesos():
    reportes.append(["Ingreso a cambiar acceso", transformar(contador_segundos)])
    op=seleccionar_opcion("Elige: ", ["Por niveles", "Usuario", "Salir"])
    if op==1:
        reportes.append(["Ingreso a cambiar acceso a usuario", transformar(contador_segundos)])
        ev3.screen.clear()
        list_users=[]
        for user_aux in vec_usuarios:
            list_users.append(user_aux.user)
        list_users.append("Salir")
        op=seleccionar_opcion("Usuarios", list_users)
        if list_users[op]!="Salir":
            ev3.screen.clear()
            vec_usuarios[op].cambiar_nivel()
            ev3.screen.clear()
            ev3.screen.draw_text(0,0, "Nivel cambiado")
            wait(500)
        cambiar_accesos()
    elif op==0:
        reportes.append(["Ingreso a cambiar acceso por niveles", transformar(contador_segundos)])
        list_aux=[]
        list_aux2=[]
        list_aux3=[]
        list_aux=list_niveles[:]
        list_aux.append("Salir")
        op2=seleccionar_opcion("Niveles", list_aux)
        if list_aux[op2]!="Salir":
            reportes.append(["Nivel elgido "+list_aux[op2], transformar(contador_segundos)])
            op3=seleccionar_opcion("Accesos", ["Agregar", "Quitar", "Salir"])
            if op3==1:
                reportes.append(["Ingreso a quitar", transformar(contador_segundos)])
                list_aux2=niveles.get(list_aux[op2],[])
                for i in range(len(list_aux2)):
                    if list_aux2[i]:
                        list_aux3.append(vec_ref[i])
                list_aux3.append("Salir")
                op4=seleccionar_opcion("", list_aux3)
                if list_aux3[op4]!="Salir":
                    reportes.append(["Se quito "+ list_aux3[op4], transformar(contador_segundos)])
                    for a, fun123 in enumerate(vec_ref):
                        if fun123==list_aux3[op4]:
                            niveles[list_aux[op2]][a]=False
            elif op3==0:
                reportes.append(["Ingreso a agregar", transformar(contador_segundos)])
                list_aux2=niveles.get(list_aux[op2],[])
                for i in range(len(list_aux2)):
                    if not list_aux2[i]:
                        list_aux3.append(vec_ref[i])
                list_aux3.append("Salir")
                op4=seleccionar_opcion("", list_aux3)
                if list_aux3[op4]!="Salir":
                    reportes.append(["Se agrego "+ list_aux3[op4], transformar(contador_segundos)])
                    for a, fun123 in enumerate(vec_ref):
                        if fun123==list_aux3[op4]:
                            niveles[list_aux[op2]][a]=True
        cambiar_accesos()

#eliges un usuario y le cambias la contrase;a
def cambiar_contra():
    reportes.append(["Ingreso a cambiar contra", transformar(contador_segundos)])
    ev3.screen.clear()
    list_users=[]
    for user in vec_usuarios:
        list_users.append(user.user)
    list_users.append("Salir")
    op=seleccionar_opcion("Usuarios", list_users)
    if list_users[op]!="Salir":
        ev3.screen.clear()
        vec_usuarios[op].contra=ingresar_texto(15, "New", 1 ,0, "Usuario: "+vec_usuarios[op].user)
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, "Contra cambiada")
        wait(1000)
        ev3.screen.clear()
        cambiar_contra()

#puedes crear un usuario y eliges su nivel
def crear_usuario():
    reportes.append(["Ingreso a crear usuario", transformar(contador_segundos)])
    ev3.screen.clear()
    usuario_nuevo=ingresar_texto(0, "Usuario", 0)
    ev3.screen.clear()
    contra_nuevo=ingresar_texto(15, "contra", 1 ,0, "Usuario: "+usuario_nuevo)
    ev3.screen.clear()
    vec_usuarios.append(Usuarios(usuario_nuevo, contra_nuevo, "visitante"))
    reportes.append(["Creo Usuario" + vec_usuarios[-1].user, transformar(contador_segundos)])
    vec_usuarios[-1].cambiar_nivel()
    ev3.screen.clear()
    ev3.screen.draw_text(0,0, "Usuario creado")
    wait(100)
    
#es el menu no hay mas jsjjsjsjs
#te permite visualizar el menu que ya se genera de porsi en la clase usuario
def menu_principal(user):
    reportes.append(["Ingreso "+user.user, transformar(contador_segundos)])
    while True:
        user.generar_menu()
        op=seleccionar_opcion("", user.vec_menu)
        if user.vec_menu[op]=="Salir":
            break
        accion=functions[user.vec_menu[op]]
        accion()


###################################################################################################################################
#Ahora sí, el programa principal puede empezar
#Primero te solicita que ingreses tu usuario y tu contase;a, si todo esta correcto ingresa a menu principal y sino te pide denuevo
def main():
    while(True):
        op=seleccionar_opcion("", ["Ingresar", "Apagar"])
        if(op==1):
            break
        ev3.screen.clear()
        usuario_ingresado=ingresar_texto(0, "Usuario", 0)
        ev3.screen.clear()
        contra=ingresar_texto(15, "contra", 1 ,0, "Usuario: "+usuario_ingresado)
        ev3.screen.clear()
        for usuario in vec_usuarios:
            if(usuario.user==usuario_ingresado and usuario.contra==contra):
                ev3.screen.draw_text(10, 40, "Ingreso con exito")
                wait(1000)
                menu_principal(usuario)
        reportes.append(["Salio", transformar(contador_segundos)])
    ev3.screen.clear()
    ev3.screen.draw_text(10, 10, "Apagando")
    wait(2000)
    ev3.screen.clear()
    ev3.screen.clear()
    ev3.speaker.beep()
####################################################################################################################################


#Vectores y variables extra
#Aqui guardas temporalmente todas las acciones, luego al guardar solo se copia lo que esta aqui pero con otro formato
reportes=[]

#vector auxilira keywords del diccionario niveles
list_niveles=["visitante", "operador", "mantenimiento", "gerente", "programador"]

#diccionario de que funciones estan disponibles para que niveles
niveles={"visitante":[True, True, False, False, False, False, False, False, False, False, False],
         "operador":[True, False, True, True, True, False, False, False, False, False, False],
         "mantenimiento":[False, False, False, False, False, True, True, False, False, False, False],
         "gerente":[False, False, True, True, True, False, False, True, False, False, False],
         "programador":[False, False, False, False, True, False, False, False, True, True, True]}

#vector auxiliar practicamente las keys del diccionario functions
vec_ref=["Ver info", "Selector v", "Selector", "Empaquetado", "Reporte", "Verif. Est.", "Horas", 
         "Mod Config", "Cambiar Acces", "Cambiar Contra", "Crear User"]

#diccionario de lo que te aparece en pantalla en los menus y las funciones reales 
functions={"Ver info":      ver_info,
           "Selector v":    selector_v,
           "Selector":      selector_fun,
           "Empaquetado":   empaquetado, 
           "Reporte":       report, 
           "Verif. Est.":   verificar_estado, 
           "Horas":         horas_trabajadas, 
           "Mod Config":    modificar_configuraciones, 
           "Cambiar Acces": cambiar_accesos, 
           "Cambiar Contra":cambiar_contra, 
           "Crear User":    crear_usuario}

#Registramos usuarios predefinidos
vec_usuarios=[Usuarios("LEO", "123", "visitante"),
              Usuarios("ABDC", "333", "operador"),
              Usuarios("GFD", "353", "mantenimiento"),
              Usuarios("GABO", "12345", "gerente"),
              Usuarios("CHUMA", "123333", "gerente"),
              Usuarios("ALVARO", "12369", "programador")]

#registramos cubos
vec_cubos_registrados=[Cubo('Defectuoso'),
                       Cubo('BLUE'),
                       Cubo('RED'),
                       Cubo('YELLOW')]

#registramos containers
vec_containers=[Container(1, 1, 2, 1, 2),
                Container(2, 1, 0, 2),
                Container(3, 1, 7),
                Container(4, 100, 100, 100, 100)]

#Alfabeto teclado para ingresar texto
teclado_a = [
    ['A', 'B', 'C', 'D', 'E','F', 'G'],
    ['H', ' I', ' J', 'K', 'L', 'M', 'N'],
    ['O', 'P', 'Q', 'R', 'S', 'T', 'U'],
    ['V', 'W', 'X', 'Y', 'Z', '<', 'OK']
]

#Numerico el otro teclado
teclado_n = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['<', '0', 'OK']
]

#vector para llamar mas facil a los teclados
teclados=[teclado_a, teclado_n]

#Variables auxiliares horas trabajadas
contador_segundos = 0
ejecutando = True

#Crear los objetos necesarios(lego)
ev3 = EV3Brick()

#Variables auxiliares para la verificacion de conexiones
s_color = None
ultrasonic = None
selector = None
cinta = None
vec_verif=[False, False, False, False]

# Bucle de espera hasta que se verifique que todos los sensores y motores esten bien conectados
while True:
    #Verificamos la coneccion del sensor de color
    try:
        s_color = ColorSensor(Port.S4)
        vec_verif[0]=True
    except OSError:
        s_color = None
        vec_verif[0]=False
    wait(100)
    ev3.screen.clear()
    actualizar_verificacion()
    #Verificamos la coneccion del sensor ultrasonico
    try:
        ultrasonic = UltrasonicSensor(Port.S3)
        vec_verif[1]=True
    except OSError:
        ultrasonic = None
        vec_verif[1]=False
    wait(100)
    ev3.screen.clear()
    actualizar_verificacion()
    #Verificamos la coneccion del selector
    try:
        selector = Motor(Port.A)
        vec_verif[2]=True
    except OSError:
        selector = None
        vec_verif[2]=False
    wait(100)
    ev3.screen.clear()
    actualizar_verificacion()
    #Verificamos la coneccion de la cinta
    try:
        cinta = Motor(Port.B)
        vec_verif[3]=True
    except OSError:
        cinta = None
        vec_verif[3]=False
    wait(100)
    ev3.screen.clear()
    actualizar_verificacion()
    # Salir del bucle si y solo si todos los dispositivos están conectados
    if vec_verif[0] and vec_verif[1] and vec_verif[2] and vec_verif[3]:
        ev3.speaker.beep()
        ev3.screen.clear()
        ev3.screen.draw_text(0,30,"Todos los dispositivos")
        ev3.screen.draw_text(0,50,"conectados.")
        wait(2000)
        ev3.screen.clear()
        break     

#post verificacion lanzamos el hilo que cuenta el tiempo  y mandamos el primer reporte de sistema iniciado
_thread.start_new_thread(contar_tiempo, ())
reportes.append(["Sistema iniciado", transformar(contador_segundos)])

#inicia el programa
main()

#corta el hilo que cuenta el tiempo
ejecutando=False
