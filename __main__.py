import sys
from PyQt5.QtWidgets import QApplication
from src.vista.InterfazEPorra import App_EPorra
from src.logica.Logica_Eporra import Logica_Eporra
from src.logica.Logica_mock import Logica_mock
from src.modelo.declarative_base import engine, Base

if __name__ == '__main__':
    # Punto inicial de la aplicación
    Base.metadata.create_all(engine)
    logica = Logica_Eporra()
    app = App_EPorra(sys.argv, logica)
    sys.exit(app.exec_())
