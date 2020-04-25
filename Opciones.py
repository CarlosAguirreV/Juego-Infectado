# Importar librerias
import pygame, sys, os, Juego, OperacionesArchivo, Menu, time, random
from pygame.locals import *

# Colores
colorBlanco = (255,255,255)
colorRojo = (170,40,40)
colorFondoRojizo = (68,8,9)

# Imagenes
imgIconoTitulo = pygame.image.load("recursos/imgB0.png")
imgOpcionMenuNormal = pygame.image.load("recursos/imgOpMenu3.png")
imgOpcionMenuInfectado = pygame.image.load("recursos/imgOpMenu4.png")

class Opciones():

	def __init__(self, ventana, dimensiones):
		# Datos de guardado
		self.__archivo = OperacionesArchivo.OperacionesArchivo()
		self.__recordAnterior = 0
		self.__personasAntesInfectadas = 0
		self.__musica = 1
		self.__efectos = 1
		self.__pantallaCompleta = 0
		
		# Iniciar elementos
		self.__salir = False
		pygame.init()
		self.__ventana = ventana
		self.__dimensiones = dimensiones
		self.__crearSpritesMenu()
		self.__crearFuentesTexto()
		self.__reloj = pygame.time.Clock()
		self.__unaVez = True
		self.__sonidoUnaVez = True
		
		# Sonidos
		self.__sndSeleccion = pygame.mixer.Sound("recursos/sndSeleccion.ogg")
		
	# Recibe los datos
	def setDatos(self, record, personasInfectadas, musica, efectos, pantallaCompleta):
		self.__recordAnterior = record
		self.__personasAntesInfectadas = personasInfectadas
		self.__musica = musica
		self.__efectos = efectos
		self.__pantallaCompleta = pantallaCompleta
	
	def __crearFuentesTexto(self):
		self.__titulo = pygame.font.Font("recursos/fntBitwise.ttf", 80)
		self.__fuenteTexto = pygame.font.Font("recursos/fntBitwise.ttf", 40)
		self.__fuenteTexto2 = pygame.font.Font("recursos/fntBitwise.ttf", 29)
		
	def __crearSpritesMenu(self):
		# Jugar, Opciones, Salir
		self.__coleccionSpritesMenuOpciones = [pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite()]
		
		# Definir coordenadas forma
		self.__coleccionSpritesMenuOpciones[0].rect = pygame.Rect(215, 150, 370, 50)
		self.__coleccionSpritesMenuOpciones[1].rect = pygame.Rect(215, 230, 370, 50)
		self.__coleccionSpritesMenuOpciones[2].rect = pygame.Rect(215, 310, 370, 50)
		self.__coleccionSpritesMenuOpciones[3].rect = pygame.Rect(215, 390, 370, 50)
		self.__coleccionSpritesMenuOpciones[4].rect = pygame.Rect(215, 470, 370, 50)
		
		self.__coleccionSpritesMenuOpciones[0].image = imgOpcionMenuNormal
		self.__coleccionSpritesMenuOpciones[1].image = imgOpcionMenuNormal
		self.__coleccionSpritesMenuOpciones[2].image = imgOpcionMenuNormal
		self.__coleccionSpritesMenuOpciones[3].image = imgOpcionMenuNormal
		self.__coleccionSpritesMenuOpciones[4].image = imgOpcionMenuNormal
		
		self.__spriteMouse = pygame.sprite.Sprite()
		self.__spriteMouse.image = pygame.image.load("recursos/imgPunteroMenu.png")
		self.__spriteMouse.rect = pygame.Rect(0,0,4,4)

	def empezar(self):
		while(not self.__salir):
			# Control frecuencia
			self.__reloj.tick(60)
			
			# Eventos
			self.__eventos()
		
		# Salir		
		pygame.quit()
		sys.exit()
	
	def __eventos(self):
		self.__refrescar()
	
		for evento in pygame.event.get():
			# Detectar si se ha pulsado sobre el boton cerrar de la ventana
			if evento.type == QUIT:
				self.__salir = True
				
			# Solo se va a refrescar la pantalla y actualizar las coordenadas del sprite del mouse si este se mueve
			if evento.type == MOUSEMOTION:
				self.__spriteMouse.rect.left, self.__spriteMouse.rect.top = pygame.mouse.get_pos()
				self.__refrescar()
			
			# Permite que solo detecte un clic
			if evento.type == MOUSEBUTTONUP:
				self.__unaVez = True
				
			# Detectar si esta pausado y se pulsa ESC
			if evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					self.__volver()
		
		# Detectar colisiones del menu
		self.i = 0
		self.hayColisiones = False
		
		for sprite in self.__coleccionSpritesMenuOpciones:
			if pygame.sprite.collide_rect(self.__spriteMouse, sprite):
				self.hayColisiones = True
			
				# Cambiar imagen
				sprite.image = imgOpcionMenuInfectado
				
				# Sonido
				if self.__efectos and self.__sonidoUnaVez:
					self.__sonidoUnaVez = False
					self.__sndSeleccion.play()
			
				# Saber si se esta pulsando el boton izquierdo del mouse
				if pygame.mouse.get_pressed()[0]:
					if self.__unaVez:
						self.__unaVez = False
						self.__accionesMenu(self.i)
				
			else:
				sprite.image = imgOpcionMenuNormal
				
			self.i += 1
			
		if not self.hayColisiones:
			self.__sonidoUnaVez = True
	
	def __cambiarModoPantalla(self):
		if self.__pantallaCompleta:
			self.__ventana = pygame.display.set_mode((self.__dimensiones[0], self.__dimensiones[1]), pygame.FULLSCREEN | pygame.HWSURFACE)
		else:
			self.__ventana = pygame.display.set_mode((self.__dimensiones[0], self.__dimensiones[1]))
			
			# Poner icono a la ventana
			pygame.display.set_icon(pygame.image.load("recursos/imgIcono.png"))
	
	# Estas son las acciones que se realizaran al hacer clic en algun elemento
	def __accionesMenu(self, valor):

		# Musica
		if valor == 0:
			if self.__musica:
				self.__musica = 0
			else:
				self.__musica = 1
		
		# Efectos
		elif valor == 1:
			if self.__efectos:
				self.__efectos = 0
			else:
				self.__efectos = 1
			
		# Pantalla completa
		elif valor == 2:
			if self.__pantallaCompleta:
				self.__pantallaCompleta = 0
				self.__cambiarModoPantalla()
			else:
				self.__pantallaCompleta = 1
				self.__cambiarModoPantalla()
		
		# Borrar datoss
		elif valor == 3:
			self.__musica = 1
			self.__efectos = 1
			self.__pantallaCompleta = 0
			self.__recordAnterior = 0
			self.__personasAntesInfectadas = 0
		
			self.__borrarDatos()
			
			self.__textoJugar = self.__fuenteTexto.render("*Datos borrados", 0, colorBlanco)
			self.__ventana.blit(self.__textoJugar, (20, self.__dimensiones[1] - 50))
			
			# Refrescar imagenes
			pygame.display.update()
			
			# Espera un poco
			time.sleep(0.5)
			
			# Poner la ventana en el estado correspondiente
			self.__cambiarModoPantalla()
			
		# Volver
		elif valor == 4:
			self.__volver()
			
	def __volver(self):
		# Guarda las opciones
		self.__guardarCambios()
	
		# Carga el menu principal
		Menu.Menu()
	
	def __guardarCambios(self):
		archivo = OperacionesArchivo.OperacionesArchivo()
		archivo.guardar(self.__recordAnterior, self.__personasAntesInfectadas, self.__musica, self.__efectos, self.__pantallaCompleta)
		
	def __borrarDatos(self):
		archivo = OperacionesArchivo.OperacionesArchivo()
		archivo.borrar()
	
	# Pinta todos los elementos en pantalla
	def __refrescar(self):
		# Pintar pantalla
		self.__ventana.fill(colorFondoRojizo)
		
		# Pintar los elementos en la pantalla
		self.__dibujarElementos()
		
		# Refrescar imagenes
		pygame.display.update()

	def __getTextoOnOff(self, valor):
		if valor:
			return "On"
		else:
			return "Off"
	
	# Dibuja todos los elementos
	def __dibujarElementos(self):
	
		# Recuadros opciones menu
		for sprite in self.__coleccionSpritesMenuOpciones:
			self.__ventana.blit(sprite.image, (sprite.rect.left, sprite.rect.top))
			
		# Esquinas
		pygame.draw.polygon(self.__ventana, colorRojo, ((0,0),(80,0), (0,80)))
		pygame.draw.polygon(self.__ventana, colorRojo, ((800,600),(720,600), (800,520)))
	
		# Imagen titulo
		self.__ventana.blit(imgIconoTitulo, (180, 10))
	
		# Textos
		self.__textoTitulo = self.__titulo.render("Opciones", 0, colorBlanco)
		self.__ventana.blit(self.__textoTitulo, (300, 20))
		
		self.__textoJugar = self.__fuenteTexto.render("Musica " + self.__getTextoOnOff(self.__musica), 0, colorBlanco)
		self.__ventana.blit(self.__textoJugar, (250, 159))
		
		self.__textoEfectos = self.__fuenteTexto.render("Efectos " + self.__getTextoOnOff(self.__efectos), 0, colorBlanco)
		self.__ventana.blit(self.__textoEfectos, (250, 239))
		
		self.__textoPantCompleta = self.__fuenteTexto2.render("Pantalla completa " + self.__getTextoOnOff(self.__pantallaCompleta), 0, colorBlanco)
		self.__ventana.blit(self.__textoPantCompleta, (250, 320))
		
		self.__textoBorrar = self.__fuenteTexto.render("Borrar datos", 0, colorBlanco)
		self.__ventana.blit(self.__textoBorrar, (250, 399))
		
		self.__textoVolver = self.__fuenteTexto.render("Volver", 0, colorBlanco)
		self.__ventana.blit(self.__textoVolver, (250, 479))
		
		# Cursor
		self.__ventana.blit(self.__spriteMouse.image, (pygame.mouse.get_pos()))
