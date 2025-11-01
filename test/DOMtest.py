import unittest
import datetime
import bcrypt

from app.models.Elector import Elector

class TestElector(unittest.TestCase):

    def setUp(self):
        self.nombres = "Juan"
        self.apellido_paterno = "Pérez"
        self.apellido_materno = "Gómez"
        self.fecha_nacimiento = datetime.date(1990, 5, 15)
        self.usuario = "jperez"
        self.contrasena_plana = "claveSecreta123"
        self.correo = "jperez@correo.com"

        # (Arrange) Inicializar la clase Elector para usarla en varias pruebas
        self.elector = Elector(
            nombres=self.nombres,
            apellido_paterno=self.apellido_paterno,
            apellido_materno=self.apellido_materno,
            fecha_nacimiento=self.fecha_nacimiento,
            usuario=self.usuario,
            contrasena=self.contrasena_plana,
            correo=self.correo
        )

    def test_creacion_elector_y_hash_init(self):
        """
        Prueba que el constructor (__init__) almacene los valores
        y hashee la contraseña correctamente.
        """
        # (Arrange) - La inicialización se hizo en setUp
        
        # (Act) - La acción fue la creación del objeto en setUp
        elector = self.elector

        # (Assert) - Verificar los resultados
        self.assertEqual(elector.nombres, self.nombres)
        self.assertEqual(elector.apellido_paterno, self.apellido_paterno)
        self.assertEqual(elector.usuario, self.usuario)
        self.assertEqual(elector.fecha_nacimiento, self.fecha_nacimiento)
        
        # Verificar que la contraseña almacenada NO es la contraseña plana
        self.assertNotEqual(elector.contrasena, self.contrasena_plana)
        
        # Verificar que la contraseña almacenada SÍ corresponde a la plana
        self.assertTrue(
            bcrypt.checkpw(self.contrasena_plana.encode('utf-8'), elector.contrasena.encode('utf-8'))
        )

    def test_revisar_contrasena_correcta(self):
        """
        Prueba que revisar_contrasena retorne True con la contraseña correcta.
        """
        # (Arrange) - elector creado en setUp
        contrasena_correcta = self.contrasena_plana
        
        # (Act)
        resultado = self.elector.revisar_contrasena(contrasena_correcta)
        
        # (Assert)
        self.assertTrue(resultado, "La revisión de contraseña correcta falló.")

    def test_revisar_contrasena_incorrecta(self):
        """
        Prueba que revisar_contrasena retorne False con una contraseña incorrecta.
        """
        # (Arrange)
        contrasena_incorrecta = "claveErronea999"
        
        # (Act)
        resultado = self.elector.revisar_contrasena(contrasena_incorrecta)
        
        # (Assert)
        self.assertFalse(resultado, "La revisión de contraseña incorrecta no retornó False.")

    def test_revisar_contrasena_vacia(self):
        """
        Prueba que revisar_contrasena retorne False con una contraseña vacía.
        """
        # (Arrange)
        contrasena_vacia = ""
        
        # (Act)
        resultado = self.elector.revisar_contrasena(contrasena_vacia)
        
        # (Assert)
        self.assertFalse(resultado, "La revisión de contraseña vacía no retornó False.")

    def test_revisar_contrasena_sensible_mayusculas(self):
        """
        Prueba que la revisión sea sensible a mayúsculas y minúsculas.
        """
        # (Arrange)
        contrasena_con_mayuscula = "ClaveSecreta123" # Diferente a "claveSecreta123"
        
        # (Act)
        resultado = self.elector.revisar_contrasena(contrasena_con_mayuscula)
        
        # (Assert)
        self.assertFalse(resultado, "La revisión de contraseña no fue sensible a mayúsculas.")

    def test_hash_constrasena_metodo(self):
        """
        Prueba el método independiente 'hash_constrasena'.
        """
        # (Arrange)
        nueva_contrasena = "nuevaClave456"
        
        # (Act)
        nuevo_hash = self.elector.hash_constrasena(nueva_contrasena)
        
        # (Assert)
        # Verificar que el hash no es la clave plana
        self.assertNotEqual(nuevo_hash, nueva_contrasena)
        
        # Verificar que el hash generado es válido
        self.assertTrue(
            bcrypt.checkpw(nueva_contrasena.encode('utf-8'), nuevo_hash.encode('utf-8'))
        )

if __name__ == '__main__':
    unittest.main()

