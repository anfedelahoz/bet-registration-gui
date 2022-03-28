import unittest
from wsgiref.handlers import IISCGIHandler

from sqlalchemy import false
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.carrera import TipoCarrera
from src.modelo.apostador import Apostador
from src.modelo.apuesta import Apuesta
from src.modelo.declarative_base import session, engine, Base
from src.modelo.declarative_base import Session
from src.logica.Logica_Eporra import Logica_Eporra
from faker import Faker
import random
from random import seed
from random import randint


# seed random number generator
class CrudApuestaTestCase(unittest.TestCase):
    def setUp(self):
        # Crea la BD
        Base.metadata.create_all(engine)
        '''Crea una instancia de Faker'''
        self.data_factory = Faker('es_ES')
        self.nombre_competidor_1 = self.data_factory.name()
        self.nombre_competidor_2 = self.data_factory.name()
        self.probabilidad_1 = round(random.uniform(0, 1), 2)
        self.probabilidad_2 = round(random.uniform(0, 1), 2)
        
        self.region = self.data_factory.state_name()
        tipos_carrera = ['Circuito', 'Carrera', 'Formula', 'Maraton']
        self.nombre_carrera = f"{random.choice(tipos_carrera)} {self.region} {randint(1, 20)}"
        '''Guarda apostador en base de datos'''
        nombre_apostador = self.data_factory.name()
        self.nuevo_apostador = Apostador(nombre = nombre_apostador)
        session.add(self.nuevo_apostador)
        session.commit()
        
        '''Crea los competidores que seran anadidos al crear la carrera'''
        self.logica_crud = Logica_Eporra()
        self.logica_crud.aniadir_competidor(nombre = self.nombre_competidor_1, probabilidad = self.probabilidad_1)
        self.logica_crud.aniadir_competidor(nombre = self.nombre_competidor_2, probabilidad = self.probabilidad_2)
        '''Busca la carrera creada'''
        self.resultado_crear_carrera = self.logica_crud.crear_carrera(self.nombre_carrera)
        nueva_carrera = session.query(Carrera).filter(Carrera.titulo == self.nombre_carrera).first()
        self.id_carrera = nueva_carrera.id_carrera
        competidor_apostado = session.query(Competidor).filter(Competidor.nombre == self.nombre_competidor_1).first()
        self.id_competidor_apostado = competidor_apostado.id_competidor
        self.id_apostador = self.nuevo_apostador.id_apostador
        self.valor_apuesta = self.data_factory.random_int(5000, 500000)
        
        
    def test_crear_apuesta(self):
        self.logica_crud = Logica_Eporra()
        resultado_crear_apuesta = self.logica_crud.crear_apuesta(self.id_apostador, self.id_carrera, self.id_competidor_apostado, self.valor_apuesta)
        # id_apostador, id_carrera, id_conmpetidor, valor
        print("resultado_crear_apuesta->" + str(resultado_crear_apuesta))
        print(self.nombre_competidor_1,"/n" , self.nombre_competidor_2, "/n", self.nombre_carrera)
        self.assertEqual(True, resultado_crear_apuesta)
        
    def test_crear_apuesta_campos_no_vacios(self):
        self.logica_crud = Logica_Eporra()
        resultado_crear_apuesta = self.logica_crud.crear_apuesta(None, None, None, None)
        # id_apostador, id_carrera, id_conmpetidor, valor
        print("resultado_crear_apuesta->" + str(resultado_crear_apuesta))
        print(self.nombre_competidor_1,"/n" , self.nombre_competidor_2, "/n", self.nombre_carrera)
        self.assertEqual(False, resultado_crear_apuesta)

    def test_crear_apuesta_campo_valor_valido(self):
        self.logica_crud = Logica_Eporra()
        resultado_crear_apuesta = self.logica_crud.crear_apuesta(self.id_apostador, self.id_carrera, self.id_competidor_apostado, "Cartagena")
        # id_apostador, id_carrera, id_conmpetidor, valor
        print("resultado_crear_apuesta->" + str(resultado_crear_apuesta))
        print(self.nombre_competidor_1,"/n" , self.nombre_competidor_2, "/n", self.nombre_carrera)
        self.assertEqual(False, resultado_crear_apuesta)

        
    def test_dar_apuestas_carrera(self):        
        self.logica_crud = Logica_Eporra()
        self.logica_crud.crear_apuesta(self.id_apostador, self.id_carrera, self.id_competidor_apostado, self.valor_apuesta)
        carrera = session.query(Carrera).first()
        '''Obtiene la 1era apuesta de carrera'''
        apuesta_carrera = session.query(Apuesta).filter(Carrera.id_carrera == carrera.id_carrera).first()
        id_apuesta_origen=apuesta_carrera.id_apuesta
        '''Consulta las apuestas de la carrera 'resultado_apuestas_carreras'''
        resultado_apuestas_carreras = self.logica_crud.dar_apuestas_carrera(carrera.id_carrera)
        '''Busca coincidencia de apuestas que contengas el id de apuesta de la 1era carrea'''
        existe_apuesta=[x for x in resultado_apuestas_carreras if x.id_apuesta == id_apuesta_origen]
        id_apuesta_busqueda = existe_apuesta[0].id_apuesta
        print("id_apuesta_origen->" + str(id_apuesta_origen))
        print("existe_apuesta->" + str(existe_apuesta[0].id_apuesta))        
        self.assertEqual(id_apuesta_origen, id_apuesta_busqueda)

    
    def test_terminar_carrera(self):
        self.logica_crud = Logica_Eporra()
        self.logica_crud.crear_apuesta(self.id_apostador, self.id_carrera, self.id_competidor_apostado, self.valor_apuesta)
        # calcula reporte de ganancia y cierra carrera , cambia el estado de la columna Abierta a False
        self.logica_crud.dar_reporte_ganancias(self.id_carrera,self.id_competidor_apostado)
        carrera =  session.query(Carrera).filter(Carrera.id_carrera == self.id_carrera).first()
        estado_carrera = carrera.abierta
        print("estado_carrera->"+ str(estado_carrera))
        self.assertEqual(estado_carrera,False)
    
    def test_editar_apuesta(self):
        self.logica_crud = Logica_Eporra()
        self.logica_crud.crear_apuesta(self.id_apostador, self.id_carrera, self.id_competidor_apostado, self.valor_apuesta)
        print("Valor Apostado nueva carrera" + str(self.valor_apuesta))
        apuestaLista= self.logica_crud.dar_apuestas_carrera(self.id_carrera)
        apuesta = apuestaLista[-1]
        _id_apuesta=apuesta.id_apuesta
        print("id_apuesta amodificar"+  str(_id_apuesta))
        print("resultado_crear_apuesta creado->idApuesta,valor" + str(apuesta.id_apuesta)+ "," + str(apuesta.valor))
        print(self.nombre_competidor_1,"/n" , self.nombre_competidor_2, "/n", self.nombre_carrera)
        valor_modificado = self.data_factory.random_int(10000, 800000)
        self.logica_crud.editar_apuesta(apuesta.id_apuesta, self.id_apostador, self.id_competidor_apostado, float(valor_modificado))
        apuestaLista= self.logica_crud.dar_apuestas_carrera(self.id_carrera)
        apuesta = apuestaLista[-1]
        print("resultado_crear_apuesta modificado->idApuesta,valor" + str(apuesta.id_apuesta)+ "," + str(apuesta.valor))
        print("comparativa valores->" + str(valor_modificado) +","+ str(apuesta.valor))
        self.assertEqual(valor_modificado, apuesta.valor)
        
    def test_editar_apuesta_valores_validos(self):
        self.logica_crud = Logica_Eporra()
        self.logica_crud.crear_apuesta(self.id_apostador, self.id_carrera, self.id_competidor_apostado, self.valor_apuesta)
        print("Valor Apostado nueva carrera" + str(self.valor_apuesta))
        apuestaLista= self.logica_crud.dar_apuestas_carrera(self.id_carrera)
        apuesta = apuestaLista[-1]
        _id_apuesta=apuesta.id_apuesta
        print("id_apuesta amodificar"+  str(_id_apuesta))
        print("resultado_crear_apuesta creado->idApuesta,valor" + str(apuesta.id_apuesta)+ "," + str(apuesta.valor))
        print(self.nombre_competidor_1,"/n" , self.nombre_competidor_2, "/n", self.nombre_carrera)
        valor_modificado = "No valido"
        resultado_editar_apuesta = self.logica_crud.editar_apuesta(apuesta.id_apuesta, self.id_apostador, self.id_competidor_apostado, valor_modificado)
        apuestaLista= self.logica_crud.dar_apuestas_carrera(self.id_carrera)
        apuesta = apuestaLista[-1]
        print("resultado_crear_apuesta modificado->idApuesta,valor" + str(apuesta.id_apuesta)+ "," + str(apuesta.valor))
        print("comparativa valores->" + str(valor_modificado) +","+ str(apuesta.valor))
        self.assertFalse(resultado_editar_apuesta)
    
    def test_crear_apostador(self):
        self.logica_crud = Logica_Eporra()
        nombre_apostador = self.data_factory.name()
        self.logica_crud.aniadir_apostador(nombre_apostador)
        nuevo_apostador =  session.query(Apostador).filter(Apostador.nombre == nombre_apostador).first()
        self.assertEqual(nuevo_apostador.nombre, nombre_apostador)
        
    def test_crear_apostador_campos_validos(self):
        self.logica_crud = Logica_Eporra()
        nombre_apostador = None
        result_crea_apostador=self.logica_crud.aniadir_apostador(nombre_apostador)
        nuevo_apostador =  session.query(Apostador).filter(Apostador.nombre == nombre_apostador).first()
        self.assertFalse(result_crea_apostador)
    
    def test_listar_apostadores(self):
        self.logica_crud = Logica_Eporra()
        nombre_1 = self.data_factory.name()
        nombre_2 = self.data_factory.name()
        self.logica_crud.aniadir_apostador(nombre_1)
        self.logica_crud.aniadir_apostador(nombre_2)
        apostadores =  self.logica_crud.dar_apostadores()
        nombre_apostadores = [apostador.nombre for apostador in apostadores]
        apostadores_en_lista = nombre_1 in nombre_apostadores and nombre_2 in nombre_apostadores
        self.assertTrue(apostadores_en_lista)
        
    def test_eliminar_carrera(self):
        self.logica_crud = Logica_Eporra()
        self.logica_crud.aniadir_competidor(nombre = self.nombre_competidor_1, probabilidad = self.probabilidad_1)
        self.logica_crud.aniadir_competidor(nombre = self.nombre_competidor_2, probabilidad = self.probabilidad_2)
        nombre_carrera = self.data_factory.name()
        self.logica_crud.crear_carrera(nombre_carrera)
        carrera =  session.query(Carrera).filter(Carrera.titulo == nombre_carrera).first()
       
        self.logica_crud = Logica_Eporra()
        result_elimiar=self.logica_crud.eliminar_carrera(carrera.id_carrera)

        self.logica_crud = Logica_Eporra()
        consulta=self.logica_crud.dar_carrera(carrera.id_carrera)
        
        self.assertEqual(0,len(consulta))
        
    def tearDown(self):
        print("tearDown")
        self.logica_crud.glbListCompetidores= []
        '''Abre la sesión'''
        '''Consulta todos las carreras'''
        carreras = session.query(Carrera).all()
        '''Borra todas las carreras'''
        for carrera in carreras:
            session.delete(carrera)
        '''Consulta todos los apostadores'''
        apostadores = session.query(Apostador).all()
        '''Borra todas las apostadores'''
        for apostador in apostadores:
            session.delete(apostador)
        session.commit()
        session.close()
