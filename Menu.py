# Importar librerias
import pygame, sys, os, Juego, OperacionesArchivo, Opciones
from pygame.locals import *

# Colores
colorBlanco = (255,255,255)
colorRojo = (170,40,40)
colorFondoRojizo = (68,8,9)
colorVerde = (0, 150, 75)

# Imagenes
imgLogo1 = pygame.image.load("recursos/imgLogo1.png")
imgLogo2 = pygame.image.load("recursos/imgLogo2.png")
imgOpcionMenuNormal = pygame.image.load("recursos/imgOpMenu1.png")
imgOpcionMenuInfectado = pygame.image.load("recursos/imgOpMenu2.png")
imgPortada = pygame.image.load("recursos/imgPortada.png")

class Menu():

	def __init__(self):
		# Datos de guardado
		self.__archivo = OperacionesArchivo.OperacionesArchivo()
		self.__record = 0
		self.__personasInfectadas = 0
		self.__musica = 1
		self.__efectos = 1
		self.__pantallaCompleta = 0
		self.__sonidoUnaVez = True
		
		# Cargar datos si los hay, si no crear nuevos
		if(self.__archivo.cargar()):
			datos = self.__archivo.getDatos();
			self.__record = datos[0]
			self.__personasInfectadas = datos[1]
			self.__musica = datos[2]
			self.__efectos = datos[3]
			self.__pantallaCompleta = datos[4]
			
		else:
			print("*Se han creado datos de guardado")
			self.__archivo.guardar(self.__record, self.__personasInfectadas, self.__musica, self.__efectos, self.__pantallaCompleta)
		
		# Iniciar elementos
		self.__salir = False
		pygame.init()
		self.__dimensionesVentana = (800, 600)
		self.__crearVentana(self.__dimensionesVentana)
		self.__crearSpritesMenu()
		self.__crearFuentesTexto()
		self.__reloj = pygame.time.Clock()
		
		# Sonidos
		self.__sndSeleccion = pygame.mixer.Sound("recursos/sndSeleccion.ogg")
		
		# Situar mouse
		self.__situarMouse()
		
		# Ocultar mouse
		pygame.mouse.set_visible(False)
		
		# Empezar
		self.__empezar()
		
	def __situarMouse(self):
		pygame.mouse.set_pos(388, 279)
	
	def __crearFuentesTexto(self):
		self.__titulo = pygame.font.Font("recursos/fntBitwise.ttf", 140)
		self.__fuenteTexto = pygame.font.Font("recursos/fntBitwise.ttf", 40)
		self.__fuenteRecords = pygame.font.Font("recursos/fntBitwise.ttf", 45)
		
		self.__textoTitulo = self.__titulo.render("Infectado", 0, colorBlanco)
		self.__textoJugar = self.__fuenteTexto.render("Jugar", 0, colorBlanco)
		self.__textoOpciones = self.__fuenteTexto.render("Opciones", 0, colorBlanco)
		self.__textoSalir = self.__fuenteTexto.render("Salir", 0, colorBlanco)
		if(self.__record > 0):
			self.__textoInfectados = self.__fuenteRecords.render("Infectados: " + str(self.__personasInfectadas), 0, colorVerde)
			self.__textoRecord = self.__fuenteRecords.render("Record: " + str(self.__record), 0, colorBlanco)
		else:
			self.__textoInfectados = self.__fuenteRecords.render("", 0, colorVerde)
			self.__textoRecord = self.__fuenteRecords.render("Aun no hay records", 0, colorBlanco)		
	
	def __crearVentana(self, dimensiones):
		# Posicionar ventana
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)
	
		# Poner icono a la ventana
		pygame.display.set_icon(pygame.image.load("recursos/imgIcono.png"))
	
		# Poner titulo a la ventana
		pygame.display.set_caption("Infectado")
	
		# Crear ventana
		if self.__pantallaCompleta:
			self.__ventana = pygame.display.set_mode((dimensiones[0], dimensiones[1]), pygame.FULLSCREEN | pygame.HWSURFACE)
		else:
			self.__ventana = pygame.display.set_mode((dimensiones[0], dimensiones[1]))
		
	def __crearSpritesMenu(self):
		# Jugar, Opciones, Salir
		self.__coleccionSpritesMenu = [pygame.sprite.Sprite(), pygame.sprite.Sprite(), pygame.sprite.Sprite()]
		
		# Definir coordenadas forma
		self.__coleccionSpritesMenu[0].rect = pygame.Rect(30, 200, 253, 50)
		self.__coleccionSpritesMenu[1].rect = pygame.Rect(30, 280, 253, 50)
		self.__coleccionSpritesMenu[2].rect = pygame.Rect(30, 360, 253, 50)
		
		self.__coleccionSpritesMenu[0].image = imgOpcionMenuNormal
		self.__coleccionSpritesMenu[1].image = imgOpcionMenuNormal
		self.__coleccionSpritesMenu[2].image = imgOpcionMenuNormal
		
		self.__spriteMouse = pygame.sprite.Sprite()
		self.__spriteMouse.image = pygame.image.load("recursos/imgPunteroMenu.png")
		self.__spriteMouse.rect = pygame.Rect(0,0,4,4)

	def __empezar(self):
		while(not self.__salir):
			# Control frecuencia
			self.__reloj.tick(60)
			
			# Eventos
			self.__eventos()
		
		# Salir		
		pygame.quit()
		sys.exit()
	
	def __eventos(self):
		for evento in pygame.event.get():
			# Detectar si se ha pulsado sobre el boton cerrar de la ventana o si se ha pulsado la tecla ESC
			if evento.type == QUIT:
				self.__salir = True
				
			if evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					self.__salir = True
				
			# Solo se va a refrescar la pantalla y actualizar las coordenadas del sprite del mouse si este se mueve
			if evento.type == MOUSEMOTION:
				self.__spriteMouse.rect.left, self.__spriteMouse.rect.top = pygame.mouse.get_pos()
				self.__refrescar()
		
		# Detectar colisiones del menu
		self.i = 0
		self.hayColisiones = False
		
		for sprite in self.__coleccionSpritesMenu:
			if pygame.sprite.collide_rect(self.__spriteMouse, sprite):
				self.hayColisiones = True
				
				# Cambiar imagen menu
				sprite.image = imgOpcionMenuInfectado
			
				# Sonido
				if self.__efectos and self.__sonidoUnaVez:
					self.__sonidoUnaVez = False
					self.__sndSeleccion.play()
			
				# Saber si se esta pulsando el boton izquierdo del mouse
				if pygame.mouse.get_pressed()[0]:
					self.__accionesMenu(self.i)
				
			else:
				sprite.image = imgOpcionMenuNormal
				
			self.i += 1
		
		if not self.hayColisiones:
			self.__sonidoUnaVez = True
	
	# Estas son las acciones que se realizaran al hacer clic en algun elemento
	def __accionesMenu(self, valor):
		# Juego
		if valor == 0:
			juego = Juego.Juego(self.__ventana)
			juego.setDatos(self.__record, self.__personasInfectadas, self.__musica, self.__efectos, self.__pantallaCompleta)
			juego.empezar()
		
		# Opciones
		elif valor == 1:
			opciones = Opciones.Opciones(self.__ventana, self.__dimensionesVentana)
			opciones.setDatos(self.__record, self.__personasInfectadas, self.__musica, self.__efectos, self.__pantallaCompleta)
			opciones.empezar()
		
		# Salir
		elif valor == 2:
			self.__salir = True
	
	# Pinta todos los elementos en pantalla
	def __refrescar(self):
		# Pintar pantalla
		self.__ventana.fill(colorFondoRojizo)
		
		# Pintar los elementos en la pantalla
		self.__dibujarElementos()
		
		# Actualizar todo
		pygame.display.update()

	# Dibuja todos los elementos
	def __dibujarElementos(self):
		# Pintar imagen portada
		self.__ventana.blit(imgPortada, (360, 156))
		
		# Recuadros opciones menu
		for sprite in self.__coleccionSpritesMenu:
			self.__ventana.blit(sprite.image, (sprite.rect.left, sprite.rect.top))
			
		# Esquinas
		pygame.draw.polygon(self.__ventana, colorRojo, ((0,0),(80,0), (0,80)))
		pygame.draw.polygon(self.__ventana, colorRojo, ((800,600),(720,600), (800,520)))
	
		# Pintar logos
		self.__ventana.blit(imgLogo1, (620, 540))
		self.__ventana.blit(imgLogo2, (690, 540))
	
		# Textos
		self.__ventana.blit(self.__textoTitulo, (110, 10))
		self.__ventana.blit(self.__textoJugar, (87, 206))
		self.__ventana.blit(self.__textoOpciones, (48, 286))
		self.__ventana.blit(self.__textoSalir, (99, 368))
		self.__ventana.blit(self.__textoInfectados, (20, 490))
		self.__ventana.blit(self.__textoRecord, (20, 540))
		
		# Cursor
		self.__ventana.blit(self.__spriteMouse.image, (pygame.mouse.get_pos()))
