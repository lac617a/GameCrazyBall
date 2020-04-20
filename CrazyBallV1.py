import pygame
from pygame.locals import *
import time
import sys
import Funciones

#----------------------------
# CONSTANTES DE LA RESOLUCION
#----------------------------
ANCHO = 640
ALTO = 480
#-------------------
# VARIABLES GLOBALES
#-------------------
vida = 3
total = 0
puntuacion = 0
#-----------------
# ESCENA PRINCIPAL
#-----------------
class Escena:
	"ESQUELETO PARA CADA UNA DE LAS ESCENAS DEL VIDEOJUEGO"
	def __init__(self):
		self.proximaEscena = False
		self.jugando = True

	def leer_eventos(self,eventos):
		"LEER LOS EVENTOS PARA INTERACTUAR CON LOS OBJETOS"
		pass

	def actualizar(self,ventana,numero):
		"ACTUALIZA LOS OBJETOS EN LAS PANTALLA"
		pass

	def botones(self,eventos):
		"CONTROLES DE LOS BOTONES"
		pass

	def dibujar(self,ventana,fondo):
		"DIBUJA LOS OBJETO EN LA PANTALLA"
		pass

	def cambiar_escena(self,escena):
		"CAMBIAR LA ESCENA DEL JUEGO"
		self.proximaEscena = escena

#-------------------
# DIRECTOR PRINCIPAL
#-------------------
class Director:
	def __init__(self,titulo="",resolucion=(ANCHO,ALTO)):
		# INICIALIZAMOS LA VENTANA
		pygame.init()
		self.ventana = pygame.display.set_mode(resolucion)
		# TITULO DE LA VENTANA
		pygame.display.set_caption(titulo)
		self.fondo = Funciones.cargar_imag("tracer.png",alpha=True)
		# CREAMOS EL RELOJ
		self.reloj = pygame.time.Clock()
		# VAR -> DE CAMBIO DE ESCENAS
		self.escena = None
		# CAMBIOS DE ESCENAS
		self.escenas = {}
		# AUMENTO DE 1 EN 1 PARA CADA NIVEL
		self.numero = 1

	# CON ESTA FUNCION EJECUTAREMOS LAS ESCENAS
	def ejecutar(self,escena_inicial,fps=60):
		# GUARDAREMOS LAS ESCENAS
		self.escena = self.escenas[escena_inicial]
		# INICIALIZAREMOS EL BUCLE
		jugando = True
		terminado = False
		while jugando:
			self.reloj.tick(fps)
			# CREAMOS LA FUNCION DE TECLADO
			eventos = pygame.event.get()
			# REVISAR TODOS LOS ELEMENTOS
			for evento in eventos:
				if evento.type == pygame.QUIT:
					jugando = False
				if evento.type == pygame.KEYDOWN:
					if evento.key == pygame.K_ESCAPE:
						jugando = False
			
			# LLAMAMOS A LAS FUNCIONES CON SUS RESPECTIVOS PARAMETROS
			self.escena.leer_eventos(eventos)
			self.escena.actualizar(self.ventana,self.numero)
			self.escena.dibujar(self.ventana,self.fondo)
			# CON ESTA FUNCION LLAMARES A LAS ESCENAS
			self.elegirEscena(self.escena.proximaEscena)

			"TODO AUN FALTA ARREGLA AQUI"
			if jugando:
				jugando = self.escena.jugando

			# ACTUALIZAMOS LA VENTANA
			pygame.display.flip()
		
		# LLAMAOS EL TIEMPO POR SEGUNDO DE CADA SIGLO DE LA VENTANA
		time.sleep(1)

	# CON ESTA FUNCION ELEGIREMOS LAS ESCENAS QUE ESTAN GUARDADAS EN DICCIONARIO
	def elegirEscena(self,proximaEscena):
		if proximaEscena:
			self.agregarEscena(proximaEscena)
			self.escena = self.escenas[proximaEscena]
	
	# CON ESTA FUNCION GUARDAREMOS LAS ESCENAS Y LAS LLAMAREMOS EN OTRA OCASION
	def agregarEscena(self,escena):
		escenaClase = "Escena"+escena
		escenaObj = globals()[escenaClase]
		self.escenas[escena] = escenaObj()

#-----------------------
# NIVELES DE LAS ESCENAS
#-----------------------
class EscenaNivel1(Escena):
	def __init__(self):
		# CONSTRUCTOR DE LA CLASE (ESCENA)
		Escena.__init__(self)
		# INSTANCIAS
		self.pelota = Pelota()
		self.paleta = Paleta()
		self.muro = Muro(75) # CANTIDA DE BLOQUE ES DE 75

		# VARIABLES DE ENTORNO
		self.saque = True
		self.final = True

		# REPETIDOR DE SEGUNDO POR MOVIMIENTO
		pygame.key.set_repeat(30)
	
	def leer_eventos(self,eventos):
		for evento in eventos:
			if evento.type == pygame.KEYDOWN:
				self.paleta.update(evento)
				# SAQUE DE LA PELOTA
				if self.saque == True and evento.key == pygame.K_SPACE:
					self.saque = False
					# PELOTA DE X PARA QUE SE DEVUELVA
					if self.pelota.rect.centerx < ANCHO /2:
						self.pelota.speed = [3,-3]
					else:
						self.pelota.speed = [-3,3]
	
	def actualizar(self,ventana,numero):
		global vida,total,puntuacion
		# SAQUE DE LA PELOTA
		if self.saque == False:
		# ACTUALIZAR LA POSICION DE LA PELOTA
			self.pelota.update()
		else:
			# POSICION DE LA PELOTA AL NIVEL DE LA PALETA
			self.pelota.rect.midbottom = self.paleta.rect.midtop

		# COLISIONES ENTRE PELOTA Y PALETA
		if pygame.sprite.collide_rect(self.pelota,self.paleta):
			self.pelota.speed[1] = -self.pelota.speed[1]

		# COLISIONES ENTRE PELOTA CON EL MURO
		lista = pygame.sprite.spritecollide(self.pelota,self.muro,False)
		if lista:
			ladrillo = lista[0]
			cx = self.pelota.rect.centerx
			if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
				self.pelota.speed[0] = -self.pelota.speed[0]
			else:
				self.pelota.speed[1] = -self.pelota.speed[1]
			# SI PELOTA COLISONA CON EL MURO, ELIMINARA ESE MURO COLISIONADO
			self.muro.remove(ladrillo)

			# SI LA PELOTA COLISIONA CON EL MURO SUMA 10 PUNTOS
			puntuacion += 10
			# Y SE GUARDA EN LA PUNTUACION TOTAL
			if puntuacion > total:
				total = puntuacion

		# SI LA PELOTA TOCA LA PARTE DE ABAJO
		if self.pelota.rect.bottom > ALTO:
			time.sleep(1)
			# LE QUITA UNA VIDA
			vida -= 1
			# LA PUNTUACION VUELVE A 0
			puntuacion = 0
			# VUELVE LA PELOTA A LA PALETA
			self.saque = True

		# SI LA VIDA LLEGA A CERO
		if vida < 1:
			# EL JUEGO A TERMINADO
			Funciones.juego_terminado(ventana)
			time.sleep(2)
			# Y MOSTRARA SI QUIERES VOLVER A JUGAR O SALIR
			if self.final:
				self.cambiar_escena("Fin")
				self.final = False

		# CAMBIAMOS LOS MUROS A NUMERO O LONGITUD
		nivel_siguien = len(self.muro)
		# Y LE DECIMOS QUE SI MURO ES MENOR A 1
		if nivel_siguien < 1:
			numero += 1
			# ENTONCES QUE ME MUESTRE EL SIGUIENTE NIVEL
			Funciones.mostrar_nivelup(ventana,numero)
			time.sleep(3)
			# NIVEL SIGUIENTE
			self.cambiar_escena("Nivel2")

	# RELLENAR LA PANTALLA
	def dibujar(self,ventana,fondo):
		#PANTALLA DE FONDO
		ventana.blit(fondo,(0,0))
		# PUNTUACION ACTUAL
		Funciones.mostrar_puntuacion(ventana,puntuacion)
		# VIDA ACTUAL
		Funciones.mostrar_vida(ventana,vida)
		# PELOTA
		ventana.blit(self.pelota.image,self.pelota.rect)
		# PALETA
		ventana.blit(self.paleta.image,self.paleta.rect)
		# MUROS
		self.muro.draw(ventana)

class EscenaNivel2(Escena):
	def __init__(self):
		# CONSTRUCTOR DE LA CLASE (ESCENA)
		Escena.__init__(self)
		# INSTANCIAS
		self.pelota = Pelota()
		self.paleta = Paleta()
		self.muro2 = Muro2()

		# VARIABLES DE ENTORNO
		self.final = True
		self.saque = True

		# REPETIDOR DE SEGUNDO POR MOVIMIENTO
		pygame.key.set_repeat(30)
	
	def leer_eventos(self,eventos):
		for evento in eventos:
			if evento.type == pygame.KEYDOWN:
				self.paleta.update(evento)
				if self.saque == True and evento.key == pygame.K_SPACE:
					self.saque = False
					if self.pelota.rect.centerx < ANCHO /2:
						self.pelota.speed = [3,-3]
					else:
						self.pelota.speed = [-3,3]
	
	def actualizar(self,ventana,numero):
		global vida,total,puntuacion
		# ACTUALIZAR LA POSICION DE LA PELOTA
		if self.saque == False:
			self.pelota.update()
		else:
			self.pelota.rect.midbottom = self.paleta.rect.midtop

		# COLISIONES ENTRE PELOTA Y PALETA
		if pygame.sprite.collide_rect(self.pelota,self.paleta):
			self.pelota.speed[1] = -self.pelota.speed[1]

		# COLISIONES ENTRE PELOTA CON EL MURO
		lista = pygame.sprite.spritecollide(self.pelota,self.muro2,False)
		if lista:
			ladrillo = lista[0]
			cx = self.pelota.rect.centerx
			if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
				self.pelota.speed[0] = -self.pelota.speed[0]
			else:
				self.pelota.speed[1] = -self.pelota.speed[1]
			self.muro2.remove(ladrillo)
			
			puntuacion += 10
			if puntuacion > total:
				total = puntuacion

		if self.pelota.rect.bottom > ALTO:
			# TIEMPO DE ESPERA
			time.sleep(1)
			vida -= 1
			puntuacion = 0
			self.saque = True
			# SI LA VIDA LLEGA A CERO EL JUEGO TERMINARA
			if vida < 1:
				Funciones.juego_terminado(ventana)
				time.sleep(3)
				if self.final:
					self.cambiar_escena("Fin")
					self.final = False
				# SALIR DEL JUEGO

		# SIGUIENTE NIVEL
		nivel_siguien = len(self.muro2)
		if nivel_siguien < 1:
			numero += 2
			Funciones.mostrar_nivelup(ventana,numero)
			time.sleep(3)
			self.cambiar_escena("Nivel3")

	def dibujar(self,ventana,fondo):
		# RELLENAR LA PANTALLA
		ventana.blit(fondo,(0,0))
		Funciones.mostrar_puntuacion(ventana,puntuacion)
		Funciones.mostrar_vida(ventana,vida)
		ventana.blit(self.pelota.image,self.pelota.rect)
		ventana.blit(self.paleta.image,self.paleta.rect)
		self.muro2.draw(ventana)

class EscenaNivel3(Escena):
	def __init__(self):
		# CONSTRUCTOR DE LA CLASE (ESCENA)
		Escena.__init__(self)
		# INSTANCIAS
		self.pelota = Pelota()
		self.paleta = Paleta()
		self.muro3 = Muro3()

		# VARIABLES DE ENTORNO
		self.final = True
		self.saque = True

		# REPETIDOR DE SEGUNDO POR MOVIMIENTO
		pygame.key.set_repeat(30)
	
	def leer_eventos(self,eventos):
		for evento in eventos:
			if evento.type == pygame.KEYDOWN:
				self.paleta.update(evento)
				if self.saque == True and evento.key == pygame.K_SPACE:
					self.saque = False
					if self.pelota.rect.centerx < ANCHO /2:
						self.pelota.speed = [3,-3]
					else:
						self.pelota.speed = [-3,3]
	
	def actualizar(self,ventana,numero):
		global vida,total,puntuacion
		# ACTUALIZAR LA POSICION DE LA PELOTA
		if self.saque == False:
			self.pelota.update()
		else:
			self.pelota.rect.midbottom = self.paleta.rect.midtop

		# COLISIONES ENTRE PELOTA Y PALETA
		if pygame.sprite.collide_rect(self.pelota,self.paleta):
			self.pelota.speed[1] = -self.pelota.speed[1]

		# COLISIONES ENTRE PELOTA CON EL MURO
		lista = pygame.sprite.spritecollide(self.pelota,self.muro3,False)
		if lista:
			ladrillo = lista[0]
			cx = self.pelota.rect.centerx
			if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
				self.pelota.speed[0] = -self.pelota.speed[0]
			else:
				self.pelota.speed[1] = -self.pelota.speed[1]
			self.muro3.remove(ladrillo)
			
			# SI LA PELOTA COLISIONA CON EL MURO ENTONCES SUMARA 10 PUNTOS
			puntuacion += 10
			# Y SE ALMACENARA ESOS PUNTOS, EN PUNTUACION TOTAL
			if puntuacion > total:
				total = puntuacion

		if self.pelota.rect.bottom > ALTO:
			# TIEMPO DE ESPERA
			time.sleep(1)
			vida -= 1
			puntuacion = 0
			self.saque = True
			# SI LA VIDA LLEGA A CERO EL JUEGO TERMINARA
			if vida < 1:
				Funciones.juego_terminado(ventana)
				time.sleep(2)
				if self.final:
					self.cambiar_escena("Fin")
					self.final = False

		# SIGUIENTE NIVEL
		nivel_siguien = len(self.muro3)
		if nivel_siguien < 1:
			numero += 4
			Funciones.mostrar_nivelup(ventana,numero)
			time.sleep(3)
			self.cambiar_escena("Nivel4")

	def dibujar(self,ventana,fondo):
		# RELLENAR LA PANTALLA
		ventana.blit(fondo,(0,0))
		Funciones.mostrar_puntuacion(ventana,puntuacion)
		Funciones.mostrar_vida(ventana,vida)
		ventana.blit(self.pelota.image,self.pelota.rect)
		ventana.blit(self.paleta.image,self.paleta.rect)
		self.muro3.draw(ventana)

class EscenaNivel4(Escena):
	def __init__(self):
		# CONSTRUCTOR DE LA CLASE (ESCENA)
		Escena.__init__(self)
		# INSTANCIAS
		self.pelota = Pelota()
		self.paleta = Paleta()
		self.muro4 = Muro4() # CANTIDA DE BLOQUE ES DE 75

		# VARIABLES DE ENTORNO
		self.saque = True
		self.final = True

		# REPETIDOR DE SEGUNDO POR MOVIMIENTO
		pygame.key.set_repeat(30)
	
	def leer_eventos(self,eventos):
		for evento in eventos:
			if evento.type == pygame.KEYDOWN:
				self.paleta.update(evento)
				# SAQUE DE LA PELOTA
				if self.saque == True and evento.key == pygame.K_SPACE:
					self.saque = False
					# PELOTA DE X PARA QUE SE DEVUELVA
					if self.pelota.rect.centerx < ANCHO /2:
						self.pelota.speed = [3,-3]
					else:
						self.pelota.speed = [-3,3]
	
	def actualizar(self,ventana,numero):
		global vida,total,puntuacion
		# SAQUE DE LA PELOTA
		if self.saque == False:
		# ACTUALIZAR LA POSICION DE LA PELOTA
			self.pelota.update()
		else:
			# POSICION DE LA PELOTA AL NIVEL DE LA PALETA
			self.pelota.rect.midbottom = self.paleta.rect.midtop

		# COLISIONES ENTRE PELOTA Y PALETA
		if pygame.sprite.collide_rect(self.pelota,self.paleta):
			self.pelota.speed[1] = -self.pelota.speed[1]

		# COLISIONES ENTRE PELOTA CON EL MURO
		lista = pygame.sprite.spritecollide(self.pelota,self.muro4,False)
		if lista:
			ladrillo = lista[0]
			cx = self.pelota.rect.centerx
			if cx < ladrillo.rect.left or cx > ladrillo.rect.right:
				self.pelota.speed[0] = -self.pelota.speed[0]
			else:
				self.pelota.speed[1] = -self.pelota.speed[1]
			# SI PELOTA COLISONA CON EL MURO, ELIMINARA ESE MURO COLISIONADO
			self.muro.remove(ladrillo)

			# SI LA PELOTA COLISIONA CON EL MURO SUMA 10 PUNTOS
			puntuacion += 10
			# Y SE GUARDA EN LA PUNTUACION TOTAL
			if puntuacion > total:
				total = puntuacion

		# SI LA PELOTA TOCA LA PARTE DE ABAJO
		if self.pelota.rect.bottom > ALTO:
			time.sleep(1)
			# LE QUITA UNA VIDA
			vida -= 1
			# LA PUNTUACION VUELVE A 0
			puntuacion = 0
			# VUELVE LA PELOTA A LA PALETA
			self.saque = True

		# SI LA VIDA LLEGA A CERO
		if vida < 1:
			# EL JUEGO A TERMINADO
			Funciones.juego_terminado(ventana)
			time.sleep(2)
			# Y MOSTRARA SI QUIERES VOLVER A JUGAR O SALIR
			if self.final:
				self.cambiar_escena("Fin")
				self.final = False

		# CAMBIAMOS LOS MUROS A NUMERO O LONGITUD
		nivel_siguien = len(self.muro4)
		# Y LE DECIMOS QUE SI MURO ES MENOR A 1
		if nivel_siguien < 1:
			numero += 1
			# ENTONCES QUE ME MUESTRE EL SIGUIENTE NIVEL
			Funciones.mostrar_nivelup(ventana,numero)
			time.sleep(3)
			# NIVEL SIGUIENTE
			self.cambiar_escena("Fin")

	# RELLENAR LA PANTALLA
	def dibujar(self,ventana,fondo):
		#PANTALLA DE FONDO
		ventana.blit(fondo,(0,0))
		# PUNTUACION ACTUAL
		Funciones.mostrar_puntuacion(ventana,puntuacion)
		# VIDA ACTUAL
		Funciones.mostrar_vida(ventana,vida)
		# PELOTA
		ventana.blit(self.pelota.image,self.pelota.rect)
		# PALETA
		ventana.blit(self.paleta.image,self.paleta.rect)
		# MUROS
		self.muro4.draw(ventana)
#-----------------------------------------
# CLASES DE PELOTA,PALETA,LADRILLO Y MUROS
#-----------------------------------------
class Pelota(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# CARGAR IMAGEN
		self.image = Funciones.cargar_imag("ball.png",alpha=True)
		# OBTENER RECTANGULO DE LA IMAGEN
		self.rect = self.image.get_rect()
		# POSICION INICIAL DE LA PELOTA EN EJE X & Y
		self.rect.centery = ALTO / 2
		self.rect.centerx = ANCHO / 2
		# VELOCIDAD INICIAL
		self.speed = [3,3]
	
	def update(self):
		# COLISION DE PELOTA DE IZQUIERDA A DERECHA
		if self.rect.left <= 0 or self.rect.right > ANCHO:
			self.speed[0] = -self.speed[0]
		# COLISION DE PELOTA DE ARRIBA A BAJO
		elif self.rect.top <= 30:
			self.speed[1] = -self.speed[1]
			
		# MOVER EN BASE A POSICION ACTUAL Y VELOCIDAD
		self.rect.move_ip(self.speed)
				
class Paleta(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		# CARGAR IMAGEN
		self.image = Funciones.cargar_imag("paleta.png",alpha=True)
		# OBTENER RECTANGULO DE LA IMAGEN
		self.rect = self.image.get_rect()
		# POSICION INCIAL CENTRADA EN PANTALLA EN X
		self.rect.midbottom = (ANCHO / 2, ALTO -20)
		# ESTABLECEMOS LA VELOCIDAD INICIAL
		self.speed = [0,0]
		
	def update(self,evento):
		# BUSCAR SI SE PRESIONO FLECHA IZQUIERDA
		if evento.key == pygame.K_LEFT and self.rect.left > 0:
			self.speed = [-8,0]
		# BUSCAR SI SE PRECIONO FLECHA DERECHA
		elif evento.key == pygame.K_RIGHT and self.rect.right < ANCHO:
			self.speed = [8,0]
		else:
			self.speed = [0,0]
		# MOVER EN BASE A POSICION ACTUAL Y VELOCIDAD
		self.rect.move_ip(self.speed)
		
class Ladrillo(pygame.sprite.Sprite):
	def __init__(self,posicion):
		pygame.sprite.Sprite.__init__(self)
		# CARGAR IMAGEN
		self.image = Funciones.cargar_imag("ladrillo.png",alpha=True)
		# OBTENER RECTANGULO DE LA IMAGEN
		self.rect = self.image.get_rect()
		# POSICION INICIAL, PROVISTA EXTERNAMENTE
		self.rect.topleft = posicion

class Muro(pygame.sprite.Group):
	def __init__(self,cantidaLadrillo):
		pygame.sprite.Group.__init__(self)
		# POSICION DE NUESTROS LADRILLOS
		px = 10
		py = 30
		# CICLO PARA COLOCAR LAS CANTIDADES DE LADRILLOS REQUERIDAS
		for i in range(cantidaLadrillo):
			# INSTANCIA
			ladrillo = Ladrillo((px,py))
			# ENLAZAR MUROS CON LADRILLOS
			self.add(ladrillo)
			# ANCHO Y LARGO DE LADRILLOS
			px += ladrillo.rect.width + 2
			if px >= ANCHO -40:
				px = 10
				py += ladrillo.rect.height +2

class Muro2(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
		px = 10
		py = 30
		self.muros = []
		self.mapa = [
			"XXXXXXXXXXXXXXX",
			"X             X",
			"X             X",
			"X             X",
			"X             X",
			"X             X",
			"X             X",
			"X             X",
			"XXXXXXXXXXXXXXX"
		]
		self.muros.append(self.mapa)
		for fila in self.mapa:
			for muro in fila:
				if muro == "X":
					ladrillo = Ladrillo((px,py))
					self.add(ladrillo)
				px += ladrillo.rect.width + 2
			if px >= ANCHO -40:
				px = 10
				py += ladrillo.rect.height + 2

class Muro3(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
		px = 10
		py = 30
		self.muros = []
		self.mapa = [
			"XXXXXXXXXXXXXXX",
			"XX     XXXXXXXX",
			"X X     X     X",
			"X  X     X    X",
			"X   X  X  X   X",
			"X    X     x  X",
			"X     X     X X",
			"XXXXXXX      XX",
			"XXXXXXXXXXXXXXX"
		]
		self.muros.append(self.mapa)
		for fila in self.mapa:
			for muro in fila:
				if muro == "X":
					ladrillo = Ladrillo((px,py))
					self.add(ladrillo)
				px += ladrillo.rect.width + 2
			if px >= ANCHO -40:
				px = 10
				py += ladrillo.rect.height + 2

class Muro4(pygame.sprite.Group):
	def __init__(self):
		pygame.sprite.Group.__init__(self)
		px = 10
		py = 30
		self.muros = []
		self.mapa = [
			"XXXXXXXXXXXXXXX",
			"XXX   XXX   XXX",
			"X    XXXXX    X",
			"X  XXX   XXX  X",
			"X     XXX     X",
			"X XXXX   XXXX X",
			"XXXXX     XXXXX",
			"XX X       X XX",
			"X             X"
		]
		self.muros.append(self.mapa)
		for fila in self.mapa:
			for muro in fila:
				if muro == "X":
					ladrillo = Ladrillo((px,py))
					self.add(ladrillo)
				px += ladrillo.rect.width + 2
			if px >= ANCHO -40:
				px = 10
				py += ladrillo.rect.height + 2
#--------------------------------
# CLASES DE INTRO Y FIN DEL JUEGO
#--------------------------------
class EscenaFin(Escena):
	def __init__(self):
	 Escena.__init__(self)
	 self.boton = Boton()

	def dibujar(self,ventana,fondo):
		Funciones.mostrar_fin(ventana)
		Funciones.mostrar_total(ventana,total)
		ventana.blit(self.boton.image,self.boton.rect)

	def leer_eventos(self,eventos):
		global vida,total,puntuacion
		for evento in eventos:
			if evento.type == pygame.KEYDOWN:
				self.boton.botones(evento)
				if self.boton.rect.centerx == 450 and evento.key == pygame.K_RETURN:
					sys.exit()
				if self.boton.rect.centerx == 200 and evento.key == pygame.K_RETURN:
					self.cambiar_escena("Nivel1")
					vida = 3
					puntuacion = 0
					total = 0

class EscenaInicio(Escena):
	def __init__(self):
		Escena.__init__(self)
		
	def dibujar(self, ventana,fondo):
		Funciones.mostrar_inicio(ventana)
	
	def leer_eventos(self, eventos):
		for evento in eventos:
			if evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_RETURN:
					time.sleep(1)
					self.cambiar_escena("Nivel1")
#-----------------------------------
# CLASE DE BOTONES PARA INTRO Y FIN
#-----------------------------------
class Boton(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = Funciones.cargar_imag("control.png",alpha=True)
		self.rect = self.image.get_rect()
		self.rect.centerx = 200
		self.rect.centery = 400
	
	def botones(self,evento):
		if evento.key == pygame.K_RIGHT:
			self.rect.centerx = 450
		elif evento.key == pygame.K_LEFT:
			self.rect.centerx = 200

#---------------------------------
# INSTANCIAS DE DIRECTOR PRINCIPAL
#---------------------------------
director = Director("CrazyBallV.0.1",(ANCHO,ALTO))
director.agregarEscena("Inicio")
director.ejecutar("Inicio")