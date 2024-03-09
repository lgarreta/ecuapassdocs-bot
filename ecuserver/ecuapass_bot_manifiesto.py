
import os, sys 
import pyautogui as py
from ecuapass_bot import EcuBot
from traceback import format_exc as traceback_format_exc

from ecuapassdocs.utils.ecuapass_utils import Utils

#----------------------------------------------------------
# Globals
#----------------------------------------------------------
sys.stdout.reconfigure(encoding='utf-8')

def main ():
	args = sys.argv 
	jsonFilepath = args [1]
	runningDir   = os.getcwd()
	mainBotManifiesto (jsonFilepath, runningDir)

#----------------------------------------------------------
# Main function for testing
#----------------------------------------------------------
def mainBotManifiesto (jsonFilepath, runningDir):
	try:
		Utils.runningDir = runningDir
		
		ecubotMNF = EcuBotManifiesto (jsonFilepath, runningDir)
		ecubotMNF.initEcuapassWindow ()
		ecubotMNF.fillEcuapass (jsonFilepath)

		Utils.printx (ecubotMNF.createResultsMessage ())
	except Exception as ex:
		Utils.printx (f"Exception: {ex}")

#--------------------------------------------------------------------
# self for filling Ecuapass cartaporte web form (in flash)
#--------------------------------------------------------------------
class EcuBotManifiesto (EcuBot):
	def __init__(self, jsonFilepath, runningDir):
		super().__init__ (jsonFilepath, runningDir, "manifiesto")

	def fillEcuapass (self, jsonFilepath):
		try:
			py.sleep (0.01)
			py.press ("Tab"); py.press ("Tab")

			print ("\n>>>>>> Identificacion del Transportista Autorizado <<<")
			self.fillBox      ("01_Tipo_Procedimiento"); py.press ("Tab")
			self.fillBox      ("02_Sector"); py.press ("Tab")
			self.fillDate     ("03_Fecha_Emision"); py.press ("Tab")
			self.fillBoxSimpleIteration  ("04_Distrito"); py.press ("Tab")
			self.fillText     ("05_MCI"); py.press ("Tab"); 
			self.selFirstItemFromBox (); py.press ("Tab"); 

			print (">>> Identificación Permisos")
			[py.press ("left") for i in range (3)]
			self.fillRButton  ("07_TipoPermiso_CI")
			self.fillRButton  ("08_TipoPermiso_PEOTP")
			self.fillRButton  ("09_TipoPermiso_PO")

			print ("\n>>>>>> Identificacion del Transportista Autorizado <<<")
			self.fillText     ("10_PermisoOriginario", self.SLOW_PAUSE); py.press ("Tab"); 
			self.fillText     ("11_PermisoServicios1"); py.press ("Tab"); 
			self.fillText     ("12_PermisoServicios2"); py.press ("Tab"); 
			self.fillText     ("13_PermisoServicios3"); py.press ("Tab"); 
			self.fillText     ("14_PermisoServicios4"); py.press ("Tab"); 
			#self.fillText     ("15_NombreTransportista"); py.press ("Tab"); 
			#self.fillText     ("16_DirTransportista"); py.press ("Tab"); 
			py.press ("Tab")
			py.press ("Tab")

			Utils.scrollN (15)

			print ("\n>>>>>> Identificacion del Vehículo Habilitado <<<")
			self.fillText     ("17_Marca_Vehiculo"); py.press ("Tab");
			self.fillText     ("18_Ano_Fabricacion"); py.press ("Tab");
			self.fillBox      ("19_Pais_Vehiculo"); py.press ("Tab");
			self.fillText     ("20_Placa_Vehiculo", PAUSE=0.3); py.press ("Tab");
			self.fillText     ("21_Nro_Chasis"); py.press ("Tab");
			self.fillText     ("22_Nro_Certificado", PAUSE=0.3); py.press ("Tab");
			self.fillBox      ("23_Tipo_Vehiculo"); py.press ("Tab");


			print ("\n>>>>>> Identificacion de la Unidad de Carga (Remolque) <<<")
			self.fillText     ("24_Marca_remolque"); py.press ("Tab");
			self.fillText     ("25_Ano_Fabricacion"); py.press ("Tab");
			self.fillText     ("26_Placa_remolque"); py.press ("Tab");
			self.fillBox      ("27_Pais_remolque"); py.press ("Tab");
			self.fillText     ("28_Nro_Certificado"); py.press ("Tab");
			self.fillText     ("29_Otra_Unidad"); py.press ("Tab");

			print ("\n>>>>>> Identificacion de la Tripulacion <<<")
			self.fillBox      ("30_Pais_Conductor"); py.press ("Tab");
			self.fillBox      ("31_TipoId_Conductor"); py.press ("Tab");
			self.fillText     ("32_Id_Conductor"); py.press ("Tab");
			self.fillBox      ("33_Sexo_Conductor"); py.press ("Tab");
			self.fillDate     ("34_Fecha_Conductor"); py.press ("Tab");
			self.fillText     ("35_Nombre_Conductor"); py.press ("Tab");
			self.fillText     ("36_Licencia_Conductor"); py.press ("Tab");
			self.fillText     ("37_Libreta_Conductor"); py.press ("Tab");

			self.fillBox      ("38_Pais_Auxiliar"); py.press ("Tab");
			self.fillBox      ("39_TipoId_Auxiliar"); py.press ("Tab");
			self.fillText     ("40_Id_Auxiliar"); py.press ("Tab");
			self.fillBox      ("41_Sexo_Auxiliar"); py.press ("Tab");
			self.fillText     ("42_Fecha_Auxiliar"); py.press ("Tab");
			self.fillText     ("43_Nombre_Auxiliar"); py.press ("Tab");
			self.fillText     ("44_Apellido_Auxiliar"); py.press ("Tab");
			self.fillText     ("45_Licencia_Auxiliar"); py.press ("Tab");
			self.fillText     ("46_Libreta_Auxiliar"); py.press ("Tab");


			Utils.scrollN (15)
			print ("\n>>>>>> Datos Sobre la Carga <<<")
			self.fillBox      ("47_Pais_Carga"); py.press ("Tab"); py.press ("Tab")
			self.fillBox      ("49_Pais_Descarga"); py.press ("Tab"); py.press ("Tab")
			self.fillBox      ("51_Tipo_Carga"); py.press ("Tab")
			self.fillText     ("52_Descripcion_Carga"); 

			[py.hotkey ("shift", "Tab") for i in range (4)]
			self.fillBox      ("48_Ciudad_Carga"); py.press ("Tab"); py.press ("Tab")
			self.fillBox      ("50_Ciudad_Descarga")
			[py.press ("Tab") for i in range (3)]

			print ("\n>>>>>> Datos Sobre la Mercancia <<<")
			self.fillText     ("53_Precio_Mercancias"); py.press ("Tab")
			self.fillBox      ("54_Incoterm"); py.press ("Tab");
			self.fillBox      ("55_Moneda"); py.press ("Tab");
			self.fillBox      ("56_Pais_Moneda"); py.press ("Tab"); py.press ("Tab")
			# Not yet ciudad: 57_Ciudad_Moneda
			self.fillBox      ("58_AduanaDest_Pais"); py.press ("Tab"); py.press ("Tab")
			# Not yet ciudad: 59_AduanaDest_Ciudad
			self.fillText     ("60_Peso_NetoTotal"); py.press ("Tab");
			self.fillText     ("61_Peso_BrutoTotal"); py.press ("Tab");
			self.fillText     ("62_Volumen"); py.press ("Tab");
			self.fillText     ("63_OtraUnidad")

			# Jump to 64_AduanaCruce_Pais
			[py.press ("Tab") for i in range (4)]
			self.fillBox      ("64_AduanaCruce_Pais"); 
			# Not yet ciudad: 65_AduanaCruce_Ciudad

			# Back to 57_Ciudad_Moneda, 59_AduanaDest_Ciudad
			[py.hotkey ("shift", "Tab") for i in range (10)]
			self.fillBox      ("57_Ciudad_Moneda"); py.press ("Tab"); py.press ("Tab")
			self.fillBox      ("59_AduanaDest_Ciudad")

			# Jump to 65_AduanaCruce_Ciudad
			[py.press ("Tab") for i in range (9)]
			py.sleep (0.5)
			self.fillBox    ("65_AduanaCruce_Ciudad"); py.press ("Tab");

			Utils.scrollN (10)
			print ("\n>>>>>> Agregando aduanas de cruce y de destino <<<<<<")
			# Aduana(s) de Cruce de Fronteras
			py.press ("space"); py.sleep (0.1); py.press ("space");
			[py.hotkey ("shift", "Tab") for i in range (2)]
			# Aduana destino
			self.fillBox      ("58_AduanaDest_Pais"); py.press ("Tab"); 
			py.sleep (0.5)
			self.fillBox      ("59_AduanaDest_Ciudad"); py.press ("Tab"); 
			py.press ("space"); py.sleep (0.1); py.press ("space");

			[py.press ("Tab") for i in range (6)]

			Utils.scrollN (20)
			#[py.press ("Tab") for i in range (14)]
			#[py.hotkey ("shift", "Tab") for i in range (13)]

			print ("\n>>>>>> Detalles finales <<<")
			self.fillText     ("66_Secuencia"); py.press ("Tab")
			py.press ("Tab"); #self.fillText     ("67_MRN"); py.press ("Tab");
			py.press ("Tab"); #self.fillText     ("68_MSN"); py.press ("Tab");
			py.press ("Tab"); #self.fillText     ("69_CPIC"); py.press ("Tab");
			py.press ("Tab")  # Search button

			self.fillText     ("70_TotalBultos"); py.press ("Tab");
			self.fillBox      ("71_Embalaje"); py.press ("Tab");
			self.fillText     ("72_Marcas"); py.press ("Tab");
			self.fillText     ("73_Peso_Neto"); py.press ("Tab");
			self.fillText     ("74_Peso_Bruto"); py.press ("Tab");
			self.fillText     ("75_Volumen"); py.press ("Tab");
			self.fillText     ("76_OtraUnidad"); py.press ("Tab");
			self.fillText     ("77_Nro_UnidadCarga"); py.press ("Tab");
			self.fillBox      ("78_Tipo_UnidadCarga"); py.press ("Tab");
			self.fillBox      ("79_Cond_UnidadCarga"); py.press ("Tab");
			self.fillText     ("80_Tara"); py.press ("Tab");
			self.fillText     ("81_Descripcion"); py.press ("Tab");

			Utils.scrollN (10)
			[py.press ("Tab") for i in range (4)]
			self.fillText     ("82_Precinto"); py.press ("Tab");

			print ("\n>>>>>> Buscando/Seleccionando cartaporte <<<<<<")
			[py.hotkey ("shift", "Tab") for i in range (18)]
			py.press ("space")    # Search button
			py.sleep (2)
			[py.press ("Tab") for i in range (3)]
			#py.press ("down")     # "Hoy": Time range
			[py.press ("Tab") for i in range (3)]
			py.press ("down")
			py.press ("down")
			py.press ("down")     # Search for CPIC
			[py.press ("Tab") for i in range (3)]
			py.press ("space")    # "Consultar"
			py.sleep (2)
			[py.hotkey ("shift", "Tab") for i in range (2)]
			self.fillText     ("69_CPIC"); 

			[py.press ("Tab") for i in range (4)]      # Go to found cartaportes
			py.press ("down")
			self.clickSelectedCartaporte ("69_CPIC")
			py.press ("Tab")
			py.press ("space")

		except Exception as ex:
			Utils.printx (f"EXCEPCION: Problemas al llenar documento '{self.jsonFilepath}'")
			print (traceback_format_exc())
			return (str(ex))

		return (f"Ingresado exitosamente el documento {self.jsonFilepath}")


#--------------------------------------------------------------------
# Call to main
#--------------------------------------------------------------------
if __name__ == "__main__":
	main()

