import unittest
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.carrera import TipoCarrera
from src.modelo.declarative_base import Session, engine, Base
from src.modelo.declarative_base import session
from src.logica.Logica_Eporra import Logica_Eporra
from faker import Faker
import random

class CrudCarreraTestCase(unittest.TestCase):

    def setUp(self):
        # Crea la BD
        Base.metadata.create_all(engine)
        '''Crea una isntancia de Faker'''
        self.data_factory = Faker()

    def test_crear_carrera(self):
        self.logica_crud = Logica_Eporra()
        self.logica_crud.aniadir_competidor(nombre="Viafara", probabilidad=round(random.uniform(0, 1), 2))
        self.logica_crud.aniadir_competidor(nombre="Montoya", probabilidad=round(random.uniform(0, 1), 2))
        resultado_crear_carrera = self.logica_crud.crear_carrera("Formula 1")
        
        self.logica_crud.aniadir_competidor(nombre="Viafara2", probabilidad=round(random.uniform(0, 1), 2))
        self.logica_crud.aniadir_competidor(nombre="Montoya2", probabilidad=round(random.uniform(0, 1), 2))
        resultado_crear_carrera2 = self.logica_crud.crear_carrera("Formula 2")
        print("se va evaluar: Crear Carrera.()")
        self.assertTrue(resultado_crear_carrera)

    def test_crear_carrera_nombre_vacio(self):
        print("se va evaluar: test_crear_carrera_sin_nombre():")
        nombre_carrera = None
        self.logica_crud = Logica_Eporra()
        self.logica_crud.aniadir_competidor(nombre="Viafara", probabilidad=round(random.uniform(0, 1), 2))
        self.logica_crud.aniadir_competidor(nombre="Montoya", probabilidad=round(random.uniform(0, 1), 2))
        resultado_crear_carrera = self.logica_crud.crear_carrera(nombre_carrera)
        # si es falso no se pudo guardar la carrera, prueba OK
        self.assertFalse(resultado_crear_carrera)

        nombre_carrera = ""
        self.logica_crud = Logica_Eporra()
        listCompetidores = []
        self.logica_crud.aniadir_competidor(nombre="Ford", probabilidad=round(random.uniform(0, 1), 2))
        self.logica_crud.aniadir_competidor(nombre="Mustang", probabilidad=round(random.uniform(0, 1), 2))
        resultado_crear_carrera = self.logica_crud.crear_carrera(nombre_carrera)
        # si es falso no se pudo guardar la carrera, prueba OK
        self.assertFalse(resultado_crear_carrera)


    def test_crear_carrera_nombre_duplicado(self):
        self.logica_crud = Logica_Eporra()
        # Se intenta crear carrera con nombre de carrera ya generado en 'test_crear_carrera'
        carrera1 = self.logica_crud.crear_carrera('Formula 1')
        carrera2 = self.logica_crud.crear_carrera('Formula 1')
        print("Se va a evaluar: Crear Carrera sin duplicar nombre.")
        self.assertFalse(carrera2)
        
    def test_crear_carrera_competidores(self):
        nombre_carrera="Formula 2"
        self.logica_crud = Logica_Eporra()
        self.logica_crud.aniadir_competidor("Pombo", round(random.uniform(0, 1), 2))
        self.logica_crud.aniadir_competidor("McQueen", round(random.uniform(0, 1), 2))
        resultado_crear_carrera = self.logica_crud.crear_carrera(nombre_carrera)
        print("se va evaluar: Crear carrera con competidores.()")
        self.assertTrue(resultado_crear_carrera)
    
    def test_crear_carrera_sin_competidores(self):
        print("se va evaluar: test_crear_carrera_sin_competidores():")
        self.logica_crud = Logica_Eporra()
        self.logica_crud.glbListCompetidores = None
        nombre_carrera = "5000 millas"
        resultado_crear_carrera = self.logica_crud.crear_carrera(nombre_carrera)
        # si es falso no se pudo guardar la carrera, prueba OK
        self.assertFalse(resultado_crear_carrera)
        
        self.logica_crud.glbListCompetidores = []
        nombre_carrera = "5000 millas"
        resultado_crear_carrera = self.logica_crud.crear_carrera(nombre_carrera)
        # si es falso no se pudo guardar la carrera, prueba OK
        self.assertFalse(resultado_crear_carrera)
    
    def test_crear_carrera_min_dos_competidores(self):
        print("se va evaluar: test_crear_carrera_sin_competidores():")
        self.logica_crud = Logica_Eporra()
        self.logica_crud.aniadir_competidor("Tommy", round(random.uniform(0, 1), 2))
        resultado_crear_carrera = self.logica_crud.crear_carrera("2000 yardas")
        print("se va evaluar: Crear carrera con minimo 2 competidores.()")
        self.assertFalse(resultado_crear_carrera)
        
        
    def test_crear_carrera_competidores_validos(self):
        print("se va evaluar: test_crear_carrera_competidores_validos():")
        self.logica_crud = Logica_Eporra()
        self.logica_crud.aniadir_competidor("McQueen", round(random.uniform(0, 1), 2))
        self.logica_crud.aniadir_competidor("Swchumaher", 1.3)
        self.logica_crud.aniadir_competidor("Montoya", "1")     
        self.logica_crud.aniadir_competidor("", round(random.uniform(0, 1), 2))
        self.logica_crud.aniadir_competidor(None, round(random.uniform(0, 1), 2)) 
        self.logica_crud.aniadir_competidor(" ", "234")   
        resultado_crear_carrera = self.logica_crud.crear_carrera("Formula 100")
        #si es falso no se pudo guardar la carrera, prueba OK
        self.assertFalse(resultado_crear_carrera)
    
    def test_verificar_almacenamiento_agregar_carrera(self):
        print("se va evaluar: test_verificar_almacenamiento_agregar_carrera():")
        self.logica_crud = Logica_Eporra()
        self.logica_crud.aniadir_competidor("Pombo", round(random.uniform(0, 1), 2))
        self.logica_crud.aniadir_competidor("McQueen", round(random.uniform(0, 1), 2))
        self.logica_crud.crear_carrera("Formula 3")
        
    
        carrera = session.query(Carrera).filter(Carrera.titulo == "Formula 3").first()        
        self.assertEqual(carrera.titulo, "Formula 3")
        
    def test_listar_carrera(self):
        print("se va evaluar: test_listar_carrera():")
        self.logica_crud = Logica_Eporra()
        self.logica_crud.aniadir_competidor("Pombo", round(random.uniform(0, 1), 2))
        self.logica_crud.aniadir_competidor("McQueen", round(random.uniform(0, 1), 2))
        self.logica_crud.crear_carrera("Formula 4")
        
        carrera_listada = self.logica_crud.dar_carreras()[-1]
        self.assertEqual("Formula 4", carrera_listada['Nombre'])
        
    
    def tearDown(self):
        print("tearDown")
        self.logica_crud.glbListCompetidores= []
        '''Abre la sesión'''
        '''Consulta todos las carreras'''
        busqueda = session.query(Carrera).all()
        '''Borra todas las carreras'''
        for carrera in busqueda:
            session.delete(carrera)
        session.commit()
        session.close()


    