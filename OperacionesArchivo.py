# Sistema para guardar y cargar

class OperacionesArchivo():
	def __init__(self):
		self.__nombreArchivo = "save.sav"
		self.__record = 0
		self.__personasInfectadas = 0
		self.__musica = 0
		self.__efectos = 0
		self.__pantallaCompleta = 0

	def guardar(self, record, personasInfectadas, musica, efectos, pantallaCompleta):
		cadenaRecord = str(format(record, '#04X')) + "\n"
		cadenaPersonasInfectadas = str(format(personasInfectadas, '#04X')) + "\n"
		cadenaMusica = str(format(musica, '#04X')) + "\n"
		cadenaEfectos = str(format(efectos, '#04X')) + "\n"
		cadenaPantallaCompleta = str(format(pantallaCompleta, '#04X'))
	
		try:
			archivo = open(self.__nombreArchivo, "w")
			archivo.write(cadenaRecord)
			archivo.write(cadenaPersonasInfectadas)
			archivo.write(cadenaMusica)
			archivo.write(cadenaEfectos)
			archivo.write(cadenaPantallaCompleta)
			archivo.close()
			return True

		except:
			print("*No se ha podido guardar en el archivo " + self.__nombreArchivo)
			return False

	def cargar(self):
		try:
			archivo = open(self.__nombreArchivo, "r")
			self.__record = int(archivo.readline()[0:-1], 16)
			self.__personasInfectadas = int(archivo.readline()[0:-1], 16)
			self.__musica = int(archivo.readline()[0:-1], 16)
			self.__efectos = int(archivo.readline()[0:-1], 16)
			self.__pantallaCompleta =  int(archivo.readline(), 16)
			# El [0:-1] omite el ultimo caracter de la
			# linea que corresponde al salto de linea.
			
			archivo.close()
			return True

		except:
			print("*No se han encontrado datos de guardado")
			return False
			
	def borrar(self):
		try:
			archivo = open(self.__nombreArchivo, "w")
			archivo.write("")
			archivo.close()
		except:
			print("*No se ha podido borrar")
		

	def getDatos(self):
		return (self.__record, self.__personasInfectadas, self.__musica, self.__efectos, self.__pantallaCompleta)
		