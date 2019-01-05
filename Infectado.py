# Importar librerías
import pygame, sys, os, random, time
from pygame.locals import *

# Créditos
print("\n*Créditos\n - Juego creado por Carlos Aguirre (Codigo Base)")
print(" - Agradecimientos a la gente de 'Código facilito' por enseñarme a usar Python y Pygame")
print(" - Agradecimientos a la comunidad Pygame por haber hecho este juego posible")
print(" - Música de Kevin Mac Leod - Jerry Five")

# Colores
colorBlanco = (255,255,255)
colorNegro = (0,0,0)
colorRojo = (170,40,40)
colorNaranja = (250,250,50)
colorFondoRojizo = (68,8,9)

# Colecciones de imagenes
imagenesVirus = (pygame.image.load("recursos/virus1.png"), pygame.image.load("recursos/virus2.png"), pygame.image.load("recursos/virus3.png"), pygame.image.load("recursos/virus4.png"))
imagenGlobuloBlancoInfectado = pygame.image.load("recursos/bi1.png")
imagenesGlobulosBlancos = (pygame.image.load("recursos/b1.png"), pygame.image.load("recursos/b2.png"), pygame.image.load("recursos/b3.png"))
imagenesGlobulosRojos = (pygame.image.load("recursos/c1.png"), pygame.image.load("recursos/c2.png"), pygame.image.load("recursos/c3.png"))
imagenesGlobulosRojosInfectados = (pygame.image.load("recursos/ci1.png"), pygame.image.load("recursos/ci2.png"), pygame.image.load("recursos/ci3.png"))

# Mensajes
mensajePillado = ("Oh no!", "Que faena...", "Te pillaron", "Que mal", "O_O", "Noooooo", "Sin comentarios...", "Valla #!&%*@!!!")

# Sonidos
	#sonido1 = pygame.mixer.sound.load("recursos/IndustriousFerret.mp3")
	#sonido1.play()

class Juego():
	def __init__(self):
		self.__vidas = 3
		self.__puntosTotales = 0
		self.__puntosCuerpo = 0
		self.__nivel = 1
		self.__infectado = 0
		self.__personasInfectadas = 0
		self.__salir = False
		self.__pausado = False
		self.__posAnteriorMouse = (0,0)
		self.__limiteX = 800
		self.__limiteY = 600
		self.__metaNivel = 500
		self.__metaInfectado = 3500
		self.__reloj = pygame.time.Clock()
		self.__anchoPanelSuperior = 50
		self.__direccionAbajo = True
		self.__lugarApariciones = self.__limiteY * 2 - 100
		self.__comienzoApariciones = 0
		self.__lugarDesapariciones = 0
		self.__limiteRandomXobjetos = self.__limiteX - 100
		self.__coleccionGlobulosRojos = []
		self.__coleccionGlobulosRojosInfectados = []
		self.__coleccionGlobulosBlancos = []
		self.__coleccionGlobulosBlancosInfectados = []
		
		pygame.init()
		self.__crearVentana()
		self.__crearSpriteProta()
		self.__crearFuentesTexto()
		self.__calcularLugarDesaparicionAparicion()
		
		# Música de fondo
		pygame.mixer.music.load("recursos/JerryFive.mp3")
		pygame.mixer.music.play(-1)
	
		# Ocultar mouse
		pygame.mouse.set_visible(False)
		
		# Centrar mouse
		self.__centrarMouse()
	
	def __calcularLugarDesaparicionAparicion(self):
		if self.__direccionAbajo:
			self.__lugarDesapariciones = self.__limiteY + 100
			self.__comienzoApariciones = 0
		else:
			self.__lugarDesapariciones = -100
			self.__comienzoApariciones = self.__limiteY
	
	def __centrarMouse(self):
		pygame.mouse.set_pos(self.__limiteX / 2 - 50, self.__limiteY / 2 - 20)
	
	def __crearVentana(self):
		# Posicionar ventana
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50,50)
		
		# Poner icono a la ventana
		pygame.display.set_icon(pygame.image.load("recursos/icono.png"))
		
		# Crear ventana
		self.__ventana = pygame.display.set_mode((self.__limiteX,self.__limiteY))
		
		# Poner un titulo a la ventana
		pygame.display.set_caption("Infectado")
		
	def __crearSpriteProta(self):
		self.__spriteProta = pygame.sprite.Sprite()
		self.__spriteProta.image = imagenesVirus[random.randint(0, len(imagenesVirus)-1)]
		self.__spriteProta.rect = pygame.Rect(0,0,50,50)
	
	def __crearFuentesTexto(self):
		self.__fuenteTexto = pygame.font.Font("recursos/bitwise.ttf", 30)
		self.__fuenteTextoGrande = pygame.font.Font("recursos/bitwise.ttf", 60)
	
	def empezar(self):
		while self.__salir == False:
			# Frecuencia de reloj (max 60 Hz)
			self.__reloj.tick(60)
			
			# Eventos
			for evento in pygame.event.get():
				if evento.type == QUIT:
					self.__salir = True
				if evento.type == MOUSEBUTTONDOWN:
					self.__pausado = not self.__pausado
					if self.__pausado:
						self.__posAnteriorMouse = pygame.mouse.get_pos()
						self.__centrarMouse()
						pygame.mouse.set_visible(True)
						textoPausa = self.__fuenteTexto.render("- JUEGO PAUSADO -", 0, (colorBlanco))
						self.__ventana.blit(textoPausa, (230, 300))
						pygame.display.update()
						pygame.mixer.music.pause()
					else:
						pygame.mouse.set_pos(self.__posAnteriorMouse)
						pygame.mouse.set_visible(False)
						pygame.mixer.music.unpause()
			
			if not self.__pausado:
				# Mover protagonista
				self.__moverProta()
				
				# Genera objetos
				if (len(self.__coleccionGlobulosBlancos) + len(self.__coleccionGlobulosRojos)) <= self.__nivel + 7:
					self.__crearObjeto()
				
				# Comprueba las colisiones y mueve los objetos
				self.__colisionesMovimientoObjetos()
				
				# Refresca la pantalla
				self.refrescar()
					
		# Salir	
		pygame.quit()
		sys.exit()
		
	def refrescar(self):
		# Pintar todo de color
		self.__ventana.fill(colorFondoRojizo)
		
		# Pintar paredes venosas
		pygame.draw.polygon(self.__ventana, colorRojo, ((0,0),(24,106), (37,377), (56,477), (0, self.__limiteY)))
		pygame.draw.polygon(self.__ventana, colorRojo, ((self.__limiteX,0),(790,106), (737,377), (734,477), (self.__limiteX, self.__limiteY)))
		
		# Pintar objetos dinamicos Globulos blancos e infectados, Globulos rojos e infectados y el protagonista
		for sprite in self.__coleccionGlobulosBlancos:
			self.__ventana.blit(sprite.image, (sprite.rect.left, sprite.rect.top))
			
		for sprite in self.__coleccionGlobulosBlancosInfectados:
			self.__ventana.blit(sprite.image, (sprite.rect.left, sprite.rect.top))
			
		for sprite in self.__coleccionGlobulosRojos:
			self.__ventana.blit(sprite.image, (sprite.rect.left, sprite.rect.top))
			
		for sprite in self.__coleccionGlobulosRojosInfectados:
			self.__ventana.blit(sprite.image, (sprite.rect.left, sprite.rect.top))
		
		# Panel de puntos
		pygame.draw.rect(self.__ventana, colorNegro, pygame.Rect(0, 0, self.__limiteX, self.__anchoPanelSuperior))
		
		# Puntos juego
		self.__contadorPuntos = self.__fuenteTexto.render("Puntos: " + str(self.__puntosTotales), 0, (colorBlanco))
		self.__ventana.blit(self.__contadorPuntos, (30,12))
		
		# Nivel juego
		self.__contadorPuntos = self.__fuenteTexto.render("Infectado: " + str(self.__infectado) + "%", 0, (255, 255-self.__infectado, 255-self.__infectado))
		self.__ventana.blit(self.__contadorPuntos, (350,12))
		
		# Vidas protagonista
		self.__contadorPuntos = self.__fuenteTexto.render("Aliados: " + str(self.__vidas), 0, (colorBlanco))
		self.__ventana.blit(self.__contadorPuntos, (635, 12))
		
		# Pintar personaje
		self.__ventana.blit(self.__spriteProta.image, (self.__spriteProta.rect.left, self.__spriteProta.rect.top))
		
		# Actualizar todo
		pygame.display.update()
		
	def __moverProta(self):
		# Obtener movimiento del mouse y actualizar posicion del sprite del personaje
		mousePosX, mousePosY = pygame.mouse.get_pos()
		if mousePosX < self.__limiteX - self.__spriteProta.rect.size[0]:
			self.__spriteProta.rect.left = mousePosX
		if mousePosY < self.__limiteY - self.__spriteProta.rect.size[1] and mousePosY > self.__anchoPanelSuperior:
			self.__spriteProta.rect.top = mousePosY

	def __crearObjeto(self):
		tipoObjeto = random.randint(0, 1) # 0 celula, 1 globulo blanco
		tipoImagen = random.randint(0, 2) # Forma imagen
		posX = random.randint(0, self.__limiteRandomXobjetos)
		posY = random.randint(self.__comienzoApariciones, self.__lugarApariciones)
		if self.__direccionAbajo:
			posY = posY * -1
		
		# Crear el sprite
		sprite = pygame.sprite.Sprite()
		
		if tipoObjeto == 0:
			sprite.image = imagenesGlobulosRojos[tipoImagen]
			sprite.rect = pygame.Rect(0,0,30,15)
			sprite.rect.left = posX
			sprite.rect.top = posY
			self.__coleccionGlobulosRojos.append(sprite)
		else:
			sprite.image = imagenesGlobulosBlancos[tipoImagen]
			sprite.rect = pygame.Rect(0,0,50,50)
			sprite.rect.left = posX
			sprite.rect.top = posY
			self.__coleccionGlobulosBlancos.append(sprite)
	
	def __colisionesMovimientoObjetos(self):
		# Globulos rojos
		for sprite in self.__coleccionGlobulosRojos:
			if pygame.sprite.collide_rect(self.__spriteProta, sprite):
			
				# Eliminar de la coleccion de globulos rojos el globulo infectado
				self.__coleccionGlobulosRojos.remove(sprite)
				
				# Cambiar imagen en función de la imagen anterior
				for i in range(len(imagenesGlobulosRojos)):
					if sprite.image == imagenesGlobulosRojos[i]:
						sprite.image = imagenesGlobulosRojosInfectados[i]
						sprite.rect = pygame.Rect(sprite.rect.left, sprite.rect.top,80,70)
						break
						
				# Guardar el globulo rojo infectado en otra coleccion
				self.__coleccionGlobulosRojosInfectados.append(sprite)
				
				self.__sumarPuntos(10)
				break
					
			else:
				self.__moverSprite(sprite, 2, self.__coleccionGlobulosRojos)
					
		# Globulos rojos infectados
		for sprite in self.__coleccionGlobulosRojosInfectados:
			for spriteGlobuloBlanco in self.__coleccionGlobulosBlancos:
				if pygame.sprite.collide_rect(sprite, spriteGlobuloBlanco):
					self.__coleccionGlobulosBlancos.remove(spriteGlobuloBlanco)
					
					# Crear ilusion globulo blanco infectado
					spriteGlobuloBlanco.image = imagenGlobuloBlancoInfectado
					self.__coleccionGlobulosBlancosInfectados.append(spriteGlobuloBlanco)
					self.__sumarPuntos(7)
					break
				
			self.__moverSprite(sprite, 4, self.__coleccionGlobulosRojosInfectados)
		
		# Globulos blancos
		for sprite in self.__coleccionGlobulosBlancos:
			if pygame.sprite.collide_rect(self.__spriteProta, sprite):
				
				if self.__vidas -1 < 0:
					self.refrescar()
					
					# Mostrar mensaje Fin del juego
					textoFin = self.__fuenteTextoGrande.render("Fin del juego", 0, (colorBlanco))
					self.__ventana.blit(textoFin, (230, self.__limiteY / 2))
					pygame.display.update()
					time.sleep(1.5)
					self.resetearJuego()
					break
					
				else: 
					self.__vidas -= 1
					self.refrescar()
					
					# Mostrar mensaje faena
					textoPillado = self.__fuenteTexto.render(mensajePillado[random.randint(0, len(mensajePillado) - 1)], 0, (colorNaranja), (colorNegro))
					self.__ventana.blit(textoPillado, (self.__spriteProta.rect.left, self.__spriteProta.rect.top + 50))
					pygame.display.update()
					time.sleep(0.5)
					
					self.vaciarTodo()
					break
			
			else:
				self.__moverSprite(sprite, 3, self.__coleccionGlobulosBlancos)
					
		# Globulos blancos infectados
		for sprite in self.__coleccionGlobulosBlancosInfectados:
			if pygame.sprite.collide_rect(self.__spriteProta, sprite):
				self.__coleccionGlobulosBlancosInfectados.remove(sprite)
				self.__sumarPuntos(15)
				break
			else:
				self.__moverSprite(sprite, 1, self.__coleccionGlobulosBlancosInfectados)
	
	def __moverSprite(self, sprite, valor, coleccion):
		if self.__direccionAbajo:
			if sprite.rect.top > self.__lugarDesapariciones:
				coleccion.remove(sprite)
			else:
				sprite.rect.top += valor
		else:
			if sprite.rect.top < self.__lugarDesapariciones:
				coleccion.remove(sprite)
			else:
				sprite.rect.top -= valor
	
	def __sumarPuntos(self, puntos):
		self.__puntosTotales += puntos
		self.__puntosCuerpo += puntos
		
		self.__nivel = int(self.__puntosCuerpo / self.__metaNivel)
			
		self.__calcularPorcentajeInfeccion()
	
	def __calcularPorcentajeInfeccion(self):
		self.__infectado = int(self.__puntosCuerpo * 100 / self.__metaInfectado)
		if self.__infectado >= 100:
			self.__puntosCuerpo = 0
			self.__personasInfectadas += 1
			self.__metaInfectado += 500
			self.__cambiarDireccion()
			
	def __cambiarDireccion(self):
		self.__direccionAbajo = not self.__direccionAbajo
		self.__calcularLugarDesaparicionAparicion()
		self.vaciarTodo()
			
	def vaciarTodo(self):
		self.__centrarMouse()
		
		# Vaciar colecciones
		del self.__coleccionGlobulosBlancos[:]
		del self.__coleccionGlobulosBlancosInfectados[:]
		del self.__coleccionGlobulosRojos[:]
		del self.__coleccionGlobulosRojosInfectados[:]
		
	def resetearJuego(self):
		self.__init__()
		

juego = Juego()
juego.empezar()
	
	
	
	
	