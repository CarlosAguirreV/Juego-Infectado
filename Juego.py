# Importar librerias
import pygame, sys, random, time, Menu, OperacionesArchivo
from pygame.locals import *

# Colores
colorNegro = (0,0,0)
colorBlanco = (255,255,255)
colorNaranja = (250,250,50)
colorRojo = (170,40,40)

# Colecciones de imagenes
imagenFondoPausa = pygame.image.load("recursos/imgMenuPausa.png")
imagenFondoFinJuego = pygame.image.load("recursos/imgFondoFin.png")
imagenesVirus = (pygame.image.load("recursos/imgVirus1.png"), pygame.image.load("recursos/imgVirus2.png"), pygame.image.load("recursos/imgVirus3.png"), pygame.image.load("recursos/imgVirus4.png"))
imagenGlobuloBlancoInfectado = pygame.image.load("recursos/imgBi1.png")
imagenesGlobulosBlancos = (pygame.image.load("recursos/imgB1.png"), pygame.image.load("recursos/imgB2.png"), pygame.image.load("recursos/imgB3.png"))
imagenesGlobulosRojos = (pygame.image.load("recursos/imgC1.png"), pygame.image.load("recursos/imgC2.png"), pygame.image.load("recursos/imgC3.png"))
imagenesGlobulosRojosInfectados = (pygame.image.load("recursos/imgCi1.png"), pygame.image.load("recursos/imgCi2.png"), pygame.image.load("recursos/imgCi3.png"))
imagenesInfectado = (pygame.image.load("recursos/imgInfectado1.png"), pygame.image.load("recursos/imgInfectado2.png"))

# Mensajes
mensajePillado = ("Oh no!", "Que faena...", "Te pillaron", "Que mal", "O_O", "Noooooo", "Sin comentarios...", "Valla #!&%*@!!!", "Como es posible!", ":(", ":O")

class Juego():
	# Inicializar todos los componentes del juego
	def __init__(self, ventana):
		self.__colorRojo = [170,40,40]
		self.__colorFondoRojizo = [68,8,9]
	
		self.__sonidosInfectado = (pygame.mixer.Sound("recursos/sndCi1.ogg"), pygame.mixer.Sound("recursos/sndCi2.ogg"), pygame.mixer.Sound("recursos/sndCi3.ogg"), pygame.mixer.Sound("recursos/sndBi.ogg"))
		self.__sonidoComido = pygame.mixer.Sound("recursos/sndComido.ogg")
		self.__sonidoFin = (pygame.mixer.Sound("recursos/sndFin1.ogg"), pygame.mixer.Sound("recursos/sndFin2.ogg"))
		self.__sonidoTodoInfectado = (pygame.mixer.Sound("recursos/sndVictoria1.ogg"))
		self.__salud = 50 # Cantidad de salud
		self.__puntosTotales = 0 # Puntos totales
		self.__puntosCuerpo = 0 # Los puntos del cuerpo delimitan cuando un cuerpo esta completamente infectado
		self.__nivel = 1 # El nivel aumenta por cada 500 puntos logrados, incrementa en Nv los elementos en pantalla 
		self.__metaNivel = 500 # Puntos necesarios para subir de nivel
		self.__metaInfectado = 1000 # Representa el 100% de infectado
		self.__infectado = 0 # Porcentaje de infeccion
		self.__personasInfectadas = 0 # Cantidad de personas infectadas
		self.__salir = False # Define si se va a cerrar la aplicacion
		self.__pausado = False # Define si el juego esta pausado o no
		self.__posAnteriorMouse = (0,0) # Almacena la posicion anterior del mouse
		self.__limiteX = 800 # Define el ancho de la ventana
		self.__limiteY = 600 # Define el alto de la ventana
		self.__altoPanelSuperior = 50 # Alto que ocupa el panel de los contadores
		self.__direccionAbajo = True # Indica la direccion del torrente sanguineo
		self.__lugarApariciones = self.__limiteY * 2 - 100 # Lugar en el cual empezaran a aparecer los elementos
		self.__comienzoApariciones = 0 # Donde empiezan las apariciones
		self.__lugarDesapariciones = 0 # Donde terminan las desapariciones
		self.__limiteRandomXobjetos = self.__limiteX - 100 # Lugar limite de la coordenada X en donde pueden aparecer los elementos
		
		# Propiedades de la partida
		self.__musica = True
		self.__efectos = True
		self.__pantallaCompleta = False
		self.__recordAnterior = 0
		self.__personasAntesInfectadas = 0
		
		# Paredes venosas
		self.__generarParedesVenosas()
		
		# Colecciones de elementos
		self.__coleccionGlobulosRojos = []
		self.__coleccionGlobulosRojosInfectados = []
		self.__coleccionGlobulosBlancos = []
		self.__coleccionGlobulosBlancosInfectados = []

		# Inicializar y crear elementos
		self.__ventana = ventana
		self.__crearSpriteProta()
		self.__crearFuentesTexto()
		self.__calcularLugarDesaparicionAparicion()
		self.__reloj = pygame.time.Clock()

		# Ocultar mouse
		pygame.mouse.set_visible(False)

		# Centrar mouse
		self.__centrarMouse()

	# Calcula el lugar donde apareceran y desapareceran los elementos
	def __calcularLugarDesaparicionAparicion(self):
		if self.__direccionAbajo:
			self.__lugarDesapariciones = self.__limiteY + 100
			self.__comienzoApariciones = 0
		else:
			self.__lugarDesapariciones = -100
			self.__comienzoApariciones = self.__limiteY

	# Paredes venosas aleatorias
	def __generarParedesVenosas(self):
		self.__paredIzquierda = (random.randint(25, 56), random.randint(25, 56), random.randint(25, 56))
		self.__paredDerecha = (random.randint(744, self.__limiteX - 25), random.randint(744, self.__limiteX - 25), random.randint(744, self.__limiteX - 25))

	# Centra el raton en la pantalla de juego
	def __centrarMouse(self):
		pygame.mouse.set_pos(self.__limiteX / 2 - 50, self.__limiteY / 2 - 20)

	# Crea el Sprite del protagonista
	def __crearSpriteProta(self):
		self.__spriteProta = pygame.sprite.Sprite()
		self.__virusSeleccionado = random.randint(0, len(imagenesVirus)-1)
		self.__spriteProta.image = imagenesVirus[self.__virusSeleccionado]
		self.__spriteProta.rect = pygame.Rect(0,0,50,50)

	# Crea los tipos de letra que se usaran
	def __crearFuentesTexto(self):
		self.__fuenteTexto = pygame.font.Font("recursos/fntBitwise.ttf", 30)
		self.__fuenteTextoGrande = pygame.font.Font("recursos/fntBitwise.ttf", 60)

	# Recibe los datos
	def setDatos(self, record, personasInfectadas, musica, efectos, pantallaCompleta):
		self.__recordAnterior = record
		self.__personasAntesInfectadas = personasInfectadas
		self.__musica = musica
		self.__efectos = efectos
		self.__pantallaCompleta = pantallaCompleta

	# Empieza el juego
	def empezar(self):
	
		# Musica de fondo
		if self.__musica:
			pygame.mixer.music.load("recursos/sndJerryFive.ogg")
			pygame.mixer.music.play(-1)
	
		while self.__salir == False:
			# Frecuencia de reloj (max 60 Hz)
			self.__reloj.tick(60)

			# Eventos
			self.__eventos()

		# Salir
		pygame.quit()
		sys.exit()

	# Controla todos los eventos
	def __eventos(self):
		for evento in pygame.event.get():
			# Detectar si se ha pulsado sobre el boton cerrar de la ventana
			if evento.type == QUIT:
				self.__salir = True

			# Detectar si se ha pulsado algun boton del raton
			if evento.type == MOUSEBUTTONDOWN:
				if pygame.mouse.get_pressed()[0]:
					self.__pausar()
				
			# Detectar si esta pausado y se pulsa ESC
			if self.__pausado and evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					# Carga el menu principal
					Menu.Menu()
				
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

	# Pausar y despausar el juego
	def __pausar(self):
		self.__pausado = not self.__pausado

		if self.__pausado:
			if self.__musica:
				# Pausar musica
				pygame.mixer.music.pause()
		
			# Almacenar la posicion anterior del mouse, centrar el mouse y mostrarlo
			self.__posAnteriorMouse = pygame.mouse.get_pos()
			self.__centrarMouse()
			pygame.mouse.set_visible(True)
			
			# Mostrar fondo
			self.__ventana.blit(imagenFondoPausa, (125, 270))

			# Mostrar por pantalla el texto juego pausado y pausar la musica
			textoPausa = self.__fuenteTexto.render("- JUEGO PAUSADO -", 0, (colorBlanco))
			self.__ventana.blit(textoPausa, (245, 300))
			
			# Mostrar texto si se quiere volver al menu
			textoPausa = self.__fuenteTexto.render("Para volver al menu pulsa (ESC)", 0, (colorBlanco))
			self.__ventana.blit(textoPausa, (185, 350))
			
			# Refrescar imagen
			pygame.display.update()

		else:
			# Situar el raton en la posicion anterior, ocultarlo y continuar con la musica
			pygame.mouse.set_pos(self.__posAnteriorMouse)
			pygame.mouse.set_visible(False)
			
			if self.__musica:
				pygame.mixer.music.unpause()

	# Pinta todos los elementos en pantalla
	def refrescar(self):
	
		# Pintar todo de color
		self.__ventana.fill(self.__colorFondoRojizo)

		# Pintar paredes venosas
		pygame.draw.polygon(self.__ventana, self.__colorRojo, ((0,0),(self.__paredIzquierda[0],106), (self.__paredIzquierda[1],377), (self.__paredIzquierda[2],477), (0, self.__limiteY)))
		pygame.draw.polygon(self.__ventana, self.__colorRojo, ((self.__limiteX,0),(self.__paredDerecha[0],106), (self.__paredDerecha[1],377), (self.__paredDerecha[2],477), (self.__limiteX, self.__limiteY)))

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
		pygame.draw.rect(self.__ventana, colorNegro, pygame.Rect(0, 0, self.__limiteX, self.__altoPanelSuperior))

		# Puntos juego
		self.__contadorPuntos = self.__fuenteTexto.render("Puntos: " + str(self.__puntosTotales), 0, (colorBlanco))
		self.__ventana.blit(self.__contadorPuntos, (30,12))

		# Nivel juego
		self.__contadorPuntos = self.__fuenteTexto.render("Infectado: " + str(self.__infectado) + "%", 0, (255, 255-self.__infectado, 255-self.__infectado))
		self.__ventana.blit(self.__contadorPuntos, (315,12))

		# Vidas protagonista
		self.__contadorPuntos = self.__fuenteTexto.render("Salud: " + str(self.__salud), 0, (colorBlanco))
		self.__ventana.blit(self.__contadorPuntos, (625, 12))

		# Pintar personaje
		self.__ventana.blit(self.__spriteProta.image, (self.__spriteProta.rect.left, self.__spriteProta.rect.top))

		# Actualizar todo
		pygame.display.update()

	# Crea un elemento nuevo que puede ser una celula o un globulo blanco (aleatorio)
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

	# Detecta las colisiones con los distintos elementos del juego
	def __colisionesMovimientoObjetos(self):
		## Globulos rojos
		for sprite in self.__coleccionGlobulosRojos:
			if pygame.sprite.collide_rect(self.__spriteProta, sprite):

				# Sonido
				if self.__efectos:
					self.__sonidosInfectado[random.randint(0, 2)].play()

				# Eliminar de la coleccion de globulos rojos el globulo infectado
				self.__coleccionGlobulosRojos.remove(sprite)

				# Cambiar imagen en funcion de la imagen anterior
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

		## Globulos rojos infectados
		for sprite in self.__coleccionGlobulosRojosInfectados:
			for spriteGlobuloBlanco in self.__coleccionGlobulosBlancos:
				if pygame.sprite.collide_rect(sprite, spriteGlobuloBlanco):
					self.__coleccionGlobulosBlancos.remove(spriteGlobuloBlanco)

					# Sonido
					if self.__efectos:
						self.__sonidosInfectado[3].play()

					# Crear ilusion globulo blanco infectado
					spriteGlobuloBlanco.image = imagenGlobuloBlancoInfectado
					self.__coleccionGlobulosBlancosInfectados.append(spriteGlobuloBlanco)
					self.__sumarPuntos(7)
					break

			self.__moverSprite(sprite, 4, self.__coleccionGlobulosRojosInfectados)

		## Globulos blancos
		for sprite in self.__coleccionGlobulosBlancos:
			if pygame.sprite.collide_rect(self.__spriteProta, sprite):
			
				self.__salud -= 10
				
				if self.__salud <= 0:
				
					# FIN DEL JUEGO
					self.__finJuego()
					break
				
				self.refrescar()
				
				# Sonido fin 0
				if self.__musica:
					# Pausar musica
					pygame.mixer.music.pause()
					
					self.__sonidoFin[1].play()

				# Mostrar mensaje faena
				textoPillado = self.__fuenteTexto.render(mensajePillado[random.randint(0, len(mensajePillado) - 1)], 0, (colorNaranja), (colorNegro))
				self.__ventana.blit(textoPillado, (self.__spriteProta.rect.left, self.__spriteProta.rect.top + 50))
				pygame.display.update()
				time.sleep(0.5)
				
				if self.__musica:
					# Despausar musica
					pygame.mixer.music.unpause()

				self.__centrarMouse()
				self.__vaciarTodo()
				break

			else:
				self.__moverSprite(sprite, 3, self.__coleccionGlobulosBlancos)

		## Globulos blancos infectados
		for sprite in self.__coleccionGlobulosBlancosInfectados:
			if pygame.sprite.collide_rect(self.__spriteProta, sprite):
				self.__coleccionGlobulosBlancosInfectados.remove(sprite)
				self.__sumarPuntos(15)
				
				# Aniadir vida
				if self.__salud < 100:
					self.__salud += 1
				
				# Sonido
				if self.__efectos:
					self.__sonidoComido.play()
				
				break
			else:
				self.__moverSprite(sprite, 1, self.__coleccionGlobulosBlancosInfectados)

	# Esto es lo que ocurrira cuando se acabe la partida
	def __finJuego(self):
		self.__salud = 0
		
		# Sonido fin 0
		if self.__musica:
			self.__sonidoFin[0].play()
	
		# Refrescar pantalla
		self.refrescar()
		
		# Para la musica
		pygame.mixer.music.stop()
		
		# Crear objeto para guardar
		archivo = OperacionesArchivo.OperacionesArchivo()
		cuentaPersInf = self.__personasAntesInfectadas + self.__personasInfectadas
		
		# Mostrar fondo
		self.__ventana.blit(imagenFondoFinJuego, (100, 175))
		
		# Crear texto Fin del juego
		textoFin = self.__fuenteTextoGrande.render("Fin del juego", 0, (colorBlanco))
		
		# Crear texto infectados
		textoInfectados = self.__fuenteTexto.render(str(self.__personasInfectadas) + " Infectados", 0, (colorBlanco))
		
		# Comprueba si se han batido records
		if self.__puntosTotales > self.__recordAnterior:	
			archivo.guardar(self.__puntosTotales, cuentaPersInf, self.__musica, self.__efectos, self.__pantallaCompleta)
			
			# Mostrar mensaje de Nuevo record
			textoNuevoRecord = self.__fuenteTextoGrande.render("NUEVO RECORD", 0, (colorBlanco))
			self.__ventana.blit(textoNuevoRecord, (170, 355))
			self.__ventana.blit(textoFin, (230, 240))
			
		elif self.__personasInfectadas > 0:
			archivo.guardar(self.__recordAnterior, cuentaPersInf, self.__musica, self.__efectos, self.__pantallaCompleta)
			self.__ventana.blit(textoFin, (230, 295))
		
		else:
			self.__ventana.blit(textoFin, (230, 295))
			
		if self.__personasInfectadas > 0:
			self.__ventana.blit(textoInfectados, (130, 195))
		
		# Refrescar imagen
		pygame.display.update()

		# Espera un poco
		time.sleep(2.0)

		# Carga el menu principal
		Menu.Menu()

	# Mueve todos los elementos de la pantalla exceptuando el personaje
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

	# Mueve el personaje por la pantalla
	def __moverProta(self):
		# Obtener movimiento del mouse y actualizar posicion del sprite del personaje
		mousePosX, mousePosY = pygame.mouse.get_pos()
		if mousePosX < self.__limiteX - self.__spriteProta.rect.size[0]:
			self.__spriteProta.rect.left = mousePosX
		if mousePosY < self.__limiteY - self.__spriteProta.rect.size[1] and mousePosY > self.__altoPanelSuperior:
			self.__spriteProta.rect.top = mousePosY

	# Suma los puntos pasados por parametro
	def __sumarPuntos(self, puntos):
		self.__puntosTotales += puntos
		self.__puntosCuerpo += puntos

		self.__nivel = int(self.__puntosCuerpo / self.__metaNivel)

		self.__calcularPorcentajeInfeccion()

	# Calcula el porcentaje de infeccion del cuerpo actual
	def __calcularPorcentajeInfeccion(self):
		self.__infectado = int(self.__puntosCuerpo * 100 / self.__metaInfectado)
		
		if self.__infectado > 60:
			self.__colorRojo[1] = self.__infectado - 20
			self.__colorFondoRojizo[1] = self.__infectado - 52
		
		if self.__infectado >= 100:
			self.__infectado = 0
			self.__puntosCuerpo = 0
			self.__personasInfectadas += 1
			self.__metaInfectado += 500
			self.__puntosTotales += 200;
			self.__cambiarDireccion()
			
			self.__colorRojo = [170,40,40]
			self.__colorFondoRojizo = [68,8,9]
			
			# Musica victoria
			if self.__musica:
				pygame.mixer.music.stop()
				self.__sonidoTodoInfectado.play()
			
			# Animacion infectado
			self.__mostrarAnimacionInfectado()
			
			if self.__musica:
				pygame.mixer.music.play(-1)
	
	def __mostrarAnimacionInfectado(self):
		self.__ventana.fill(self.__colorFondoRojizo)
		self.__ventana.blit(imagenesInfectado[0], (200, 120))
		self.__ventana.blit(imagenesVirus[self.__virusSeleccionado], (428, 195))
		pygame.draw.polygon(self.__ventana, colorRojo, ((0,0),(160,0),(0,160)))
		pygame.draw.polygon(self.__ventana, colorRojo, ((800,600),(640,600),(800,440)))
		
		pygame.display.update()
		time.sleep(1.25)
		
		self.__ventana.fill(self.__colorFondoRojizo)
		self.__ventana.blit(imagenesInfectado[1], (200, 120))
		self.__ventana.blit(imagenesVirus[self.__virusSeleccionado], (278, 241))
		pygame.draw.polygon(self.__ventana, colorRojo, ((0,0),(160,0),(0,160)))
		pygame.draw.polygon(self.__ventana, colorRojo, ((800,600),(640,600),(800,440)))
		pygame.display.update()
		time.sleep(1.25)

	# Cambia la direccion del torrente sanguineo
	def __cambiarDireccion(self):
		self.__direccionAbajo = not self.__direccionAbajo
		self.__generarParedesVenosas()
		self.__calcularLugarDesaparicionAparicion()
		self.__centrarMouse()
		self.__vaciarTodo()

	# Vacia todas las colecciones
	def __vaciarTodo(self):
		del self.__coleccionGlobulosBlancos[:]
		del self.__coleccionGlobulosBlancosInfectados[:]
		del self.__coleccionGlobulosRojos[:]
		del self.__coleccionGlobulosRojosInfectados[:]
