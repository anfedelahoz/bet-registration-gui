from pickle import FALSE, NONE
from re import I
from turtle import done

from sqlalchemy import false, true
from src.modelo.apuesta import Apuesta
from src.modelo.carrera import Carrera
from src.modelo.competidor import Competidor
from src.modelo.apostador import Apostador
from src.modelo.declarative_base import session

from src.modelo.declarative_base import Session, engine, Base

# grupo 76
session = Session()
class ApostadorValorGanado:
  def __init__(self, apostador, valor):
    self.apostador = apostador
    self.valor = valor


class Logica_Eporra():

    def __init__(self):
        # Este constructor contiene los datos falsos para probar la interfaz
        self.glbListCompetidores = []


#region carreras

    def dar_carreras(self):
        carreras_registradas = session.query(Carrera).all()
        if carreras_registradas:
            self.carreras = [
                {"id":item.id_carrera,"Nombre": item.titulo, "Competidores": [], "Abierta": item.abierta}
                for item in carreras_registradas
            ]        
        else:
            self.carreras = []
        return self.carreras.copy()

    def dar_carrera(self, id_carrera):
        print("logica eporras dar_carrera")
        self.session = Session()
        #self.session.query(Carrera).filter(Carrera.id_carrera == id_carrera).all()
        return self.session.query(Carrera).filter(Carrera.id_carrera == id_carrera).all()


    def crear_carrera(self, nombre):
    
        competidores = self.glbListCompetidores	
        
        nombre_carrera_esvalido=self.validarCadenaIsNoneEmptyWhithSpace(nombre)
        esValidaListaCompetidores=self.validarListaArrayIsNoneEmptyWhithSpace(competidores)

        print("nombre_carrera_esvalido->" + str(nombre_carrera_esvalido ))
        print("esValidaListaCompetidores->" + str(esValidaListaCompetidores ))
        resultado_crear_carrera=False
       
        
        # si existe un nombre duplicado en alguna carrera
        if(nombre_carrera_esvalido and esValidaListaCompetidores and len(competidores)>1):

            #Valida los atributos de cada competidor
            todosCompetidoresAtributosOK=self.validarCompetidores(competidores)
            print("todosCompetidoresAtributosOK->" + str(todosCompetidoresAtributosOK ))
            if(todosCompetidoresAtributosOK==True):

                # busca nombre duplicado en carreras
                buscar_carrera_nombre = session.query(Carrera).filter(Carrera.titulo == nombre).first()
                if  len(nombre) > 0:
                    '''Crea los objetos'''
                    
                    self.carrera1 = Carrera(titulo = nombre)
                    '''Adiciona los objetos a la sesión'''
                    print("Competidores interfaz", self.glbListCompetidores)
                    self.carrera1.competidores=competidores
                    session.add(self.carrera1)
                    session.commit()
                    session.close()
                    resultado_crear_carrera=True
                    self.glbListCompetidores = [] 
                else:              
                    resultado_crear_carrera=False
            else:#retorna False por que nloc competidores no cumplen con criterios en sus propiedades       
                resultado_crear_carrera=False

        return resultado_crear_carrera


    def eliminar_carrera(self, id_carrera):
        "elmina la carrera , asi como sus competidores y apuestas asociadas"
        resultado_eliminar_carrera=False
        validateid=False
        if(isinstance(id_carrera, int) and id_carrera>0):
            validateid=True
        try:
            if(validateid):
                _carrera = session.query(Carrera).filter(Carrera.id_carrera == id_carrera).first()
                session.delete(_carrera)
                session.commit()
                session.close()
                resultado_eliminar_carrera= True
        except:
            resultado_eliminar_carrera= False

        return resultado_eliminar_carrera


   
    
          
           
        

#endregion

    def aniadir_competidor(self, nombre, probabilidad):
        self.glbListCompetidores.append(Competidor(nombre = nombre, probabilidad = probabilidad))
        print("Competidores recibidos: ", self.glbListCompetidores)
        print(len(self.glbListCompetidores))
        for i in self.glbListCompetidores:
            print(i.nombre)

    def dar_competidores_carrera(self, id_carrera):
        #TODO:PUPO
        print("dar_competidores_carrera(id_carrera)" +  str(id_carrera))
        self.session = Session()
        competidores_carrera = self.session.query(Competidor).filter(Competidor.carrera == id_carrera).all()
        print("encontro x competidores x carrera  " +  str(len(competidores_carrera)))
        # id_carrera=id
        return competidores_carrera

    def dar_competidor(self, id_carrera, id_competidor):
        return self.carreras[id_carrera]['Competidores'][id_competidor].copy()

    
    # Metodos para validacion 
    def validarCadenaIsNoneEmptyWhithSpace(self,pCadena):
        esValidaCadena=True
      
        if (type(pCadena) ==str)==False:
            esValidaCadena=False
            return esValidaCadena           
        # check if string is empty or not
        if not pCadena:
            esValidaCadena=False
            return esValidaCadena
        if len(pCadena.strip()) == 0:
            esValidaCadena=False
            return esValidaCadena
        if len(pCadena) == 0:
            esValidaCadena=False
            return esValidaCadena
        return esValidaCadena

    #Valida si lista es vacia,None o tipo lista
    def validarListaArrayIsNoneEmptyWhithSpace(self,pLista):
        esValidaLista=True
      
        if type(pLista) is not list:
            esValidaLista=False
            return esValidaLista           

        # check if list is empty or not
        if not pLista:
            esValidaLista=False
            return esValidaLista

        if len(pLista) == 0:
            esValidaLista=False
            return esValidaLista

        return esValidaLista

    def validarCompetidores(self,listCompetidores):
        es_valida_lista=False
        es_valida_lista= self.validarListaArrayIsNoneEmptyWhithSpace(listCompetidores)
        if es_valida_lista==True :
            esValidoNombreCompetidor=False
            esValidoProbabilidad=False
            for _competidor in listCompetidores:
                esValidoNombreCompetidor=self.validarCadenaIsNoneEmptyWhithSpace(_competidor.nombre)
                probabilidad=_competidor.probabilidad
                #valida si el valor de probabilidad es es numero 
                try:
                    float(probabilidad)
                    esValidoProbabilidad= True
                except ValueError:
                    esValidoProbabilidad= False

                if(esValidoProbabilidad==True ):
                    if ((float(probabilidad) <= 1 and float(probabilidad)>0)==False):
                        esValidoProbabilidad=false
                
                if(esValidoNombreCompetidor==False or esValidoProbabilidad ==False):
                    return False
            #Todos los elementos fueorn validados con exito, return True
            return True
        else:
            #el valor de la lista en None o Vacio
            return False


#region Apostadores

    def dar_apostadores(self):
        apostador_registrados = session.query(Apostador).all()       
        return apostador_registrados



    def aniadir_apostador(self, nombre):

        resultado_crear_apostador=False

        nombre_apostador_esvalido=self.validarCadenaIsNoneEmptyWhithSpace(nombre)
        print("nombre_apostador_esvalido->" + str(nombre_apostador_esvalido ))
        if(nombre_apostador_esvalido ):
            nombre=nombre.strip()
            self.session = Session()
            # busca nombre duplicado en carreras
            buscar_apostador_nombre = self.session.query(Apostador).filter(Apostador.nombre == nombre).all()
            if  len(buscar_apostador_nombre) == 0:        
                self.apostador1 = Apostador(nombre = nombre)
                '''Adiciona los objetos a la sesión'''
                self.session.add(self.apostador1)
                self.session.commit()
                self.session.close()
                resultado_crear_apostador=True
        
        return resultado_crear_apostador

      


    def eliminar_apostador(self, id):
        pass

    
    


#endregion
#region Apuestas 
    def crear_apuesta(self, id_apostador, id_carrera,id_competidor, valor):
        resultado_crear_apuesta = False   
        if all([isinstance(id_apostador, (int)),isinstance(id_carrera, (int)) ,isinstance(id_competidor, (int))  , isinstance(valor, (int,float))]):        
            print(id_apostador)
            print(id_carrera)
            print(id_competidor)
            print(valor)

            resultado_crear_apuesta=True
            self.apuesta1 = Apuesta(apostador = id_apostador, carrera = id_carrera, competidor = id_competidor, valor = valor)
            '''Adiciona los objetos a la sesión'''
            session.add(self.apuesta1)
            session.commit()
            session.close()
        else:
            print("error en la validacion de parametro en crear apuesta")
        
        return resultado_crear_apuesta
    
    def dar_apuestas_carrera(self, id_carrera):
        if ([isinstance(id_carrera, (int))]):
            #self.session = Session()
            print ("id carrera a buscar->" + str(id_carrera))
            apuestas_carreras = session.query(Apuesta).filter(Apuesta.carrera == id_carrera).all()                                     
            #print("Apuestas en dar_apuestas_carrera->" + str(len(apuestas_carreras)))        
            return apuestas_carreras
        else:
            print("else")
            return []

    def dar_apuesta(self, id_apuesta):
            if ([isinstance(id_apuesta, (int))]):
                #self.session = Session()
                print ("id apuesta a buscar->" + str(id_apuesta))
                apuesta_busqueda = session.query(Apuesta).filter(Apuesta.id_apuesta == id_apuesta ).first()                                     
                #print("Apuestas en dar_apuestas_carrera->" + str(len(apuestas_carreras)))        
                return apuesta_busqueda
            else:
                print("Parametros no numeicos")
                return []
        
        
        

    def terminar_carrera(self):
        return 'Ganador'
    
    def dar_reporte_ganancias(self,id_carrera,id_ganador,ganacia_casa=None):
        
        #termina carrera y genra reporte de ganacia
        _list_apostador_ganacia=[]
        buscar_carrera_update = session.query(Carrera).filter(Carrera.id_carrera == id_carrera).first()
        print(f"buscar_carrera_update id:{buscar_carrera_update.id_carrera}")
        buscar_carrera_update.abierta = False
        buscar_carrera_update.ganador = id_ganador            
        session.commit()
        if buscar_carrera_update !=  None:
            #obtiene los competidores de la carrea
            apuesta_carrera=self.dar_apuestas_carrera(id_carrera)
            competidoes_carrera=self.dar_competidores_carrera(id_carrera)
            _total_apuesta=0
            _sumatoria_apuesta_pagada=0
            for apuesta in apuesta_carrera:

                _id_apostador=apuesta.apostador
                _apostador=session.query(Apostador).filter(Apostador.id_apostador == _id_apostador).first()
                _nombre_apostador=_apostador.nombre
                _competidor_apuesta=[x for x in competidoes_carrera if x.id_competidor == apuesta.competidor]
                print(_competidor_apuesta)
                _probabilidad_competidor = _competidor_apuesta[0].probabilidad
                _valor_apostado=apuesta.valor
                _couta=0
                _ganancia_apostador=0
                if(apuesta.competidor==id_ganador):
                    _couta=_probabilidad_competidor/(1-_probabilidad_competidor)
                    _ganancia_apostador= _valor_apostado + (_valor_apostado/_couta)

                
                _apostador_valor=ApostadorValorGanado(_nombre_apostador,_ganancia_apostador)
                _list_apostador_ganacia.append(_apostador_valor)
                _total_apuesta=_total_apuesta + _valor_apostado
                _sumatoria_apuesta_pagada += _ganancia_apostador

        _ganacia_casa=_total_apuesta-_sumatoria_apuesta_pagada

        if (len(_list_apostador_ganacia)<=0 or _list_apostador_ganacia ==None):
            print("No se encontraron apuesta, para esta carrera")
        else:
            print(f"Ganacia apostador 1:{_list_apostador_ganacia[0].__dict__}")
        
        print(f"Ganacia Casa :,{_ganacia_casa}")

        return _list_apostador_ganacia, _ganacia_casa


    def editar_apuesta(self, id_apuesta, id_apostador,  id_competidor,valor):

        resulta_editar = False   
        if all([isinstance(id_apostador, (int)),isinstance(id_apuesta, (int)) ,isinstance(id_competidor, (int))  , isinstance(valor, (int,float))]):      
        
            resulta_editar=False
            buscar_apuesta_update = session.query(Apuesta).filter(Apuesta.id_apuesta == id_apuesta).first()
            buscar_apuesta_update.apostador  = id_apostador
            buscar_apuesta_update.competidor = id_competidor   
            buscar_apuesta_update.valor=valor         
            session.commit()
            resulta_editar=True
        else:
            resulta_editar=False

        return resulta_editar
      



#endregion

    def inicializar_competidores(self):
        self.glbListCompetidores = []    


 