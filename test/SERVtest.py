import unittest
import datetime
import logging
from types import SimpleNamespace
from unittest.mock import patch, MagicMock

# La importación de la clase del servicio (¡esta estaba bien!)
from app.services.PersonaServicioImpl import ElectorServiceImpl

# Importar la excepción que vamos a simular
from sqlalchemy.exc import IntegrityError

class TestElectorServiceImpl(unittest.TestCase):

    def setUp(self):
        """Inicializar antes de CADA prueba."""
        
        # 1. Creamos la instancia del servicio que vamos a probar
        self.elector_service = ElectorServiceImpl()

        # 2. Deshabilitamos los logs para no ensuciar la salida de las pruebas
        logging.disable(logging.CRITICAL)

        # 3. Creamos un "Doble" (un objeto falso) para simular el 'elector_modelo'
        self.mock_elector_modelo = SimpleNamespace(
            nombres="Ana",
            apellido_paterno="Soto",
            apellido_materno="Paz",
            fecha_nacimiento=datetime.date(2000, 1, 1),
            usuario="asoto",
            correo="ana@soto.com"
        )
        
        # 4. Creamos un "Doble" para simular una instancia real de Elector
        self.mock_elector_instancia = MagicMock(id=1, usuario="asoto")

    def tearDown(self):
        """Habilitar los logs de nuevo después de las pruebas."""
        logging.disable(logging.NOTSET)

    # --- Pruebas para get_elector_by_id ---

    # Esta prueba estaba CORRECTA y por eso pasaba
    @patch('app.services.PersonaServicioImpl.Elector')
    def test_get_elector_by_id_encontrado(self, mock_elector_class):
        """Prueba obtener un elector que SÍ existe (Caso Feliz)"""
        mock_elector_class.query.get.return_value = self.mock_elector_instancia
        
        elector_id = 1
        resultado = self.elector_service.get_elector_by_id(elector_id)
        
        self.assertEqual(resultado, self.mock_elector_instancia)
        mock_elector_class.query.get.assert_called_with(elector_id)

    # Esta prueba estaba INCORRECTA (ElectorServiceImpl)
    @patch('app.services.PersonaServicioImpl.Elector')
    def test_get_elector_by_id_no_encontrado(self, mock_elector_class):
        """Prueba obtener un elector que NO existe"""
        # (Arrange)
        mock_elector_class.query.get.return_value = None
        
        # (Act)
        elector_id = 99
        resultado = self.elector_service.get_elector_by_id(elector_id)
        
        # (Assert)
        self.assertIsNone(resultado)
        mock_elector_class.query.get.assert_called_with(elector_id)

    # --- Pruebas para create_elector ---

    # Estas pruebas estaban INCORRECTAS (ElectorServiceImpl)
    @patch('app.services.PersonaServicioImpl.logger')
    @patch('app.services.PersonaServicioImpl.Elector')
    @patch('app.services.PersonaServicioImpl.db')
    def test_create_elector_exitoso(self, mock_db, mock_elector_constructor, mock_logger):
        """Prueba la creación exitosa de un elector (Caso Feliz)"""
        contrasena_plana = "claveSegura123"
        mock_elector_constructor.return_value = self.mock_elector_instancia

        resultado = self.elector_service.create_elector(self.mock_elector_modelo, contrasena_plana)

        mock_elector_constructor.assert_called_with(
            nombres="Ana",
            apellido_paterno="Soto",
            apellido_materno="Paz",
            fecha_nacimiento=datetime.date(2000, 1, 1),
            usuario="asoto",
            contrasena=contrasena_plana,
            correo="ana@soto.com"
        )
        mock_db.session.add.assert_called_with(self.mock_elector_instancia)
        mock_db.session.commit.assert_called_once()
        mock_db.session.rollback.assert_not_called()
        mock_logger.info.assert_called_once()
        self.assertEqual(resultado, self.mock_elector_instancia)

    # Estas pruebas estaban INCORRECTAS (ElectorServiceImpl)
    @patch('app.services.PersonaServicioImpl.logger')
    @patch('app.services.PersonaServicioImpl.Elector')
    @patch('app.services.PersonaServicioImpl.db')
    def test_create_elector_falla_integridad(self, mock_db, mock_elector_constructor, mock_logger):
        """Prueba la creación de un elector que falla (ej. usuario duplicado)"""
        mock_db.session.commit.side_effect = IntegrityError("Error de duplicado", None, None)
        mock_elector_constructor.return_value = self.mock_elector_instancia

        with self.assertRaises(ValueError) as contexto:
            self.elector_service.create_elector(self.mock_elector_modelo, "clave")
        
        self.assertIn("Error al crear el elector:", str(contexto.exception))
        mock_db.session.rollback.assert_called_once()
        mock_logger.error.assert_called_once()

    # --- Pruebas para update_elector ---

    # Estas pruebas estaban INCORRECTAS (ElectorServiceImpl)
    @patch('app.services.PersonaServicioImpl.logger')
    @patch('app.services.PersonaServicioImpl.db')
    def test_update_elector_exitoso(self, mock_db, mock_logger):
        """Prueba la actualización exitosa de un elector"""
        self.elector_service.update_elector(self.mock_elector_instancia)
        
        mock_db.session.merge.assert_called_with(self.mock_elector_instancia)
        mock_db.session.commit.assert_called_once()
        mock_db.session.rollback.assert_not_called()
        mock_logger.info.assert_called_once()

    # --- Pruebas para delete_elector ---
        
    # Estas pruebas estaban INCORRECTAS (ElectorServiceImpl)
    @patch('app.services.PersonaServicioImpl.logger')
    @patch('app.services.PersonaServicioImpl.db')
    def test_delete_elector_exitoso(self, mock_db, mock_logger):
        """Prueba la eliminación exitosa de un elector"""
        self.elector_service.delete_elector(self.mock_elector_instancia)
        
        mock_db.session.delete.assert_called_with(self.mock_elector_instancia)
        mock_db.session.commit.assert_called_once()
        mock_db.session.rollback.assert_not_called()
        mock_logger.info.assert_called_once()

    # --- Pruebas para get_elector_by_email ---

    # Esta prueba estaba INCORRECTA (ElectorServiceImpl)
    @patch('app.services.PersonaServicioImpl.Elector')
    def test_get_elector_by_email_encontrado(self, mock_elector_class):
        """Prueba obtener un elector por email que SÍ existe"""
        mock_query = mock_elector_class.query.filter_by.return_value
        mock_query.first.return_value = self.mock_elector_instancia
        
        email_buscado = "ana@soto.com"
        resultado = self.elector_service.get_elector_by_email(email_buscado)
        
        self.assertEqual(resultado, self.mock_elector_instancia)
        mock_elector_class.query.filter_by.assert_called_with(correo=email_buscado)
        mock_query.first.assert_called_once()

if __name__ == '__main__':
    unittest.main()
