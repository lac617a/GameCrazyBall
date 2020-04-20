import os 
import pygame
import sys
import time

#-----------
# CONSTANTES
#-----------
ANCHO = 640
ALTO = 480
colorBlanco = (255,255,255)
colorRojo = (255,93,93)

#----------------------
# FUNCIONES SEGUNDARIAS
#----------------------
# CON ESTA FUNCION CARGAREMOS TODAS LAS IMAGENES DEL JUEGO
def cargar_imag(nombre,alpha=False):
	# RUTA DE NUESTRA IMAGEN
	ruta = os.path.join("imagenes",nombre)
	# SI LA RUTA ES VERDADERA CARGARA
	try:
		image = pygame.image.load(ruta)
	# SI NO ES VERDADERA MANDARA UN ERROR
	except:
		print("Error, la imagen",ruta,"no se pudo subir")
		sys.exit()
	# SI LA IMAGEN CONTIENE ALPHA 
	if alpha == True:
		image = image.convert_alpha()
	# SI LA IMAGEN NO CONTIENE, PERO IGUAL SE EJECUTARA UNA IMAGEN
	else:
		image = image.convert()
	return image

# ENTRADA DE TEXTO EN NUESTRO JUEGO FINILIZADO
def juego_terminado(ventana):
	fuente = pygame.font.SysFont("Arial", 72)
	texto = fuente.render("Juego terminado",True,colorBlanco)
	texto_rect = texto.get_rect()
	texto_rect.center = [ANCHO /2,ALTO/2]
	ventana.blit(texto,texto_rect)
	pygame.display.flip()

# MOSTRARA LA PUNTUACION ACTUAL DEL JUEGO EN PANTALLA
def mostrar_puntuacion(ventana,puntuacion):
	fuente = pygame.font.SysFont("Consolas", 30)
	cadena = "PUNTOS: "+str(puntuacion).zfill(5)
	texto = fuente.render(cadena,True, colorBlanco)
	texto_rect = texto.get_rect()
	texto_rect.topleft = [0,0]
	ventana.blit(texto,texto_rect)

# MOSTRARA LA VIDA ACTUAL DEL JUEGO EN PANTALLA	
def mostrar_vida(ventana,vida):
	fuente = pygame.font.SysFont("Consolas", 30)
	cadena = "Vida: "+str(vida).zfill(2)
	texto = fuente.render(cadena,True, colorBlanco)
	texto_rect = texto.get_rect()
	texto_rect.midtop = [ANCHO /2,0]
	ventana.blit(texto,texto_rect)

# MOSTRARA LA PUNTUACION TOTAL AL MORIR O ACABAR EL JUEGO
def mostrar_total(ventana,total):
	fuente = pygame.font.SysFont("Consolas", 30)
	cadena = "PUNTOS MAXIMO: "+str(total).zfill(5)
	texto = fuente.render(cadena,True, colorRojo)
	texto_rect = texto.get_rect()
	texto_rect.center = [ANCHO/2,200]
	ventana.blit(texto,texto_rect)

# MOSTRARA CUANDO GANES O FINALICES EL JUEGO
def mostrar_ganaste(ventana):
	fuente = pygame.font.SysFont("Consolas", 50)
	texto = fuente.render("GANASTE",True, colorBlanco)
	texto_rect = texto.get_rect()
	texto_rect.center = [ANCHO/2, ALTO/2]
	ventana.blit(texto,texto_rect)
	pygame.display.flip()

def mostrar_fin(ventana):
	fondo = cargar_imag("final.png",alpha=True)
	fuente = pygame.font.SysFont("Consolas", 20)
	texto = fuente.render("Salir",True,colorBlanco)
	texto_rect = texto.get_rect()
	texto_rect.centerx = 450
	texto_rect.centery = 400
	fuente2 = pygame.font.SysFont("Consolas", 20)
	texto2 = fuente2.render("Volver",True,colorBlanco)
	texto_rect2 = texto2.get_rect()
	texto_rect2.centerx = 200
	texto_rect2.centery = 400
	ventana.blit(fondo,(0,0))
	ventana.blit(texto,texto_rect)
	ventana.blit(texto2,texto_rect2)

def mostrar_inicio(ventana):
	fondo = cargar_imag("intro.png",alpha=True)
	fuente = pygame.font.SysFont("Consolas",50)
	texto = fuente.render("Press Enter",True,colorRojo)
	texto_rect = texto.get_rect()
	texto_rect.centerx = ANCHO/2
	texto_rect.centery = ALTO/2
	ventana.blit(fondo,(0,0))
	ventana.blit(texto,texto_rect)

def mostrar_nivelup(ventana,numero):
	fondo = cargar_imag("nivelup.png",alpha=True)
	fuente = pygame.font.SysFont("Consolas",50)
	cadena = "Nivel "+str(numero).zfill(2)
	texto = fuente.render(cadena,True,colorRojo)
	texto_rect = texto.get_rect()
	texto_rect.centerx = ANCHO/2
	texto_rect.centery = ALTO/2
	ventana.blit(fondo,(0,0))
	ventana.blit(texto,texto_rect)
	pygame.display.flip()

def mostrar_contador(ventana):
	fuente = pygame.font.SysFont("Consolas",20)
	contador = 5
	for contador1 in range(0,contador+1):
		cadena = str(contador).zfill(2)
		contador1 -= 1
		if contador1 <= 0:
			sys.exit()
		time.sleep(3)
	texto = fuente.render(cadena,True,colorRojo)
	texto_rect = texto.get_rect()
	texto_rect.centerx = ANCHO/2
	texto_rect.centery = 280
	ventana.blit(texto,texto_rect)
	pygame.display.flip()