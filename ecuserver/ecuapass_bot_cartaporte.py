
import os, time, sys

import pyautogui as py

from ecuapass_bot import EcuBot
from traceback import format_exc as traceback_format_exc

from ecuapassdocs.utils.ecuapass_utils import Utils

#----------------------------------------------------------
# Globals
#----------------------------------------------------------
sys.stdout.reconfigure(encoding='utf-8')
PAUSE = 0

def main ():
	args = sys.argv 
	jsonFilepath = args [1]
	runningDir   = os.getcwd()
	mainBotCartaporte (jsonFilepath, runningDir)

#----------------------------------------------------------
# Main function for testing
#----------------------------------------------------------
def mainBotCartaporte (jsonFilepath, runningDir):
	try:
		Utils.runningDir = runningDir

		ecubotCPT = EcuBotCartaporte (jsonFilepath, runningDir)
		ecubotCPT.initEcuapassWindow ()
		ecubotCPT.fillEcuapass ()
		Utils.printx (f"ALERTA: Finalizada la digitación")
	except Exception as ex:
		Utils.printx (f"Exception: {ex}")

#--------------------------------------------------------------------
# self for filling Ecuapass cartaporte web form (in flash)
#--------------------------------------------------------------------
class EcuBotCartaporte (EcuBot):
	def __init__(self, jsonFilepath, runningDir):
		super().__init__ (jsonFilepath, runningDir, "cartaporte")

	#-- Main function for testing
	def fillEcuapass (self):
		try:
			py.press ("Tab"); py.press ("Tab")
			# Encabezado
			time.sleep (PAUSE)
			self.fillBoxSimpleIteration ("01_Distrito"); py.press ("Tab")
			self.fillText ("02_NumeroCPIC"); py.press ("Tab")
			self.fillText ("03_MRN"); py.press ("Tab"); 
			self.fillText ("04_MSN"); py.press ("Tab")
			self.fillBox ("05_TipoProcedimiento"); py.press ("Tab")
			#self.fillTextSelection ("06_EmpresaTransporte") # Selected by default
			py.press ("Tab")
			self.fillBox ("07_DepositoMercancia"); py.press ("Tab")

			self.fillText ("08_DirTransportista"); py.press ("Tab");
			self.fillText ("09_NroIdentificacion"); py.press ("Tab")

			Utils.scrollN (5)

			# Remitente
			self.fillSubject ("REMITENTE", "05_TipoProcedimiento", "10_PaisRemitente", 
			                  "11_TipoIdRemitente", "12_NroIdRemitente", "14_NombreRemitente",
			                  "15_DireccionRemitente", "13_NroCertSanitario")
			# Destinatario
			self.fillSubject ("DESTINATARIO", "05_TipoProcedimiento", "16_PaisDestinatario",
			                  "17_TipoIdDestinatario", "18_NroIdDestinatario", 
			                  "19_NombreDestinatario", "20_DireccionDestinatario")
			# Consignatario
			self.fillSubject ("CONSIGNATARIO", "05_TipoProcedimiento", "21_PaisConsignatario", 
			                  "22_TipoIdConsignatario", "23_NroIdConsignatario", 
			                  "24_NombreConsignatario", "25_DireccionConsignatario")

			Utils.scrollN (10)

			# Notificado
			time.sleep (PAUSE)
			self.fillText ("26_NombreNotificado"); py.press ("Tab")
			self.fillText ("27_DireccionNotificado"); py.press ("Tab")
			self.fillBox ("28_PaisNotificado"); py.press ("Tab")

			# Paises y fechas: Recepcion, Embarque, Entrega
			Utils.scrollN (5)
			self.fillBox ("29_PaisRecepcion"); py.press ("Tab"); py.press ("Tab"); 
			self.fillDate ("31_FechaRecepcion"); py.press ("Tab")
			self.fillBox ("32_PaisEmbarque"); py.press ("Tab"); py.press ("Tab"); 
			self.fillDate ("34_FechaEmbarque"); py.press ("Tab")
			self.fillBox ("35_PaisEntrega"); py.press ("Tab"); py.press ("Tab"); 
			self.fillDate ("37_FechaEntrega"); 

			[py.hotkey ("shift", "Tab") for i in range (7)]

			# Ciudades: Recepcion, Embarque, Entrega
			self.fillBox ("30_CiudadRecepcion"); py.press ("Tab"); py.press ("Tab"); py.press ("Tab"); 
			self.fillBox ("33_CiudadEmbarque"); py.press ("Tab"); py.press ("Tab"); py.press ("Tab"); 
			self.fillBox ("36_CiudadEntrega"); py.press ("Tab"); py.press ("Tab");

			Utils.scrollN (5)
			# Condiciones
			time.sleep (PAUSE)
			self.fillBox ("38_CondicionesTransporte"); py.press ("Tab")
			self.fillBox ("39_CondicionesPago"); py.press ("Tab")

			# Mercancia
			time.sleep (PAUSE)
			self.fillText ("40_PesoNeto"); py.press ("Tab")
			self.fillText ("41_PesoBruto"); py.press ("Tab")
			self.fillText ("42_TotalBultos"); py.press ("Tab")
			self.fillText ("43_Volumen"); py.press ("Tab")
			self.fillText ("44_OtraUnidad"); py.press ("Tab")
			self.fillText ("45_PrecioMercancias"); py.press ("Tab")

			# INCOTERM
			Utils.scrollN (5)
			time.sleep (PAUSE)
			self.fillBox ("46_INCOTERM"); py.press ("Tab")
			self.fillBox ("47_TipoMoneda"); py.press ("Tab")
	
			# Pais INCOTERM
			self.fillBox ("48_PaisMercancia"); 
			[py.press ("Tab") for i in range (14)]
			# Pais Emision
			self.fillBox ("62_PaisEmision"); 
			[py.hotkey ("shift", "Tab") for i in range (13)]

			# Ciudad INCOTERM
			self.fillBox ("49_CiudadMercancia"); py.press ("Tab")

			# Gastos
			time.sleep (PAUSE)
			self.fillText ("50_GastosRemitente"); py.press ("Tab")
			self.fillBox ("51_MonedaRemitente"); py.press ("Tab")
			self.fillText ("52_GastosDestinatario"); py.press ("Tab")
			self.fillBox ("53_MonedaDestinatario"); py.press ("Tab")
			self.fillText ("54_OtrosGastosRemitente"); py.press ("Tab")
			self.fillBox ("55_OtrosMonedaRemitente"); py.press ("Tab")
			self.fillText ("56_OtrosGastosDestinatario"); py.press ("Tab")
			self.fillBox ("57_OtrosMonedaDestinataio"); py.press ("Tab")
			self.fillText ("58_TotalRemitente"); py.press ("Tab")
			self.fillText ("59_TotalDestinatario"); py.press ("Tab")

			# Documentos
			self.fillText ("60_DocsRemitente"); py.press ("Tab")

			# Emision
			self.fillDate ("61_FechaEmision"); py.press ("Tab"); py.press ("Tab")
			self.fillBox ("63_CiudadEmision"); py.press ("Tab")

			Utils.scrollN (17)
			# Instrucciones
			self.fillText ("64_Instrucciones"); py.press ("Tab")
			self.fillText ("65_Observaciones"); py.press ("Tab")

			py.press ("Tab"); py.press ("Tab"); py.press ("Tab"); 
			# Detalles
			#py.sleep (3)
			self.fillText ("66_Secuencia"); py.press ("Tab")
			self.fillText ("67_TotalBultos"); py.press ("Tab")
			self.fillBox ("68_Embalaje"); py.press ("Tab")
			self.fillText ("69_Marcas"); py.press ("Tab")
			self.fillText ("70_PesoNeto"); py.press ("Tab")
			self.fillText ("71_PesoBruto"); py.press ("Tab")
			self.fillText ("72_Volumen"); py.press ("Tab")
			self.fillText ("73_OtraUnidad"); py.press ("Tab")

			# IMOs
			time.sleep (PAUSE)
			self.fillText ("74_Subpartida"); py.press ("Tab"); py.press ("Tab")
			self.fillBox ("75_IMO1"); py.press ("Tab")
			self.fillBox ("76_IMO2"); py.press ("Tab")
			self.fillBox ("77_IMO2"); py.press ("Tab")
			self.fillText ("78_NroCertSanitario"); py.press ("Tab")
			self.fillText ("79_DescripcionCarga"); py.press ("Tab")

			# Valid RUC ID with find button in 'Remitente', 'Destinatario', 'Consignatario'
			#if "IMPORTACION" in self.fields ["05_TipoProcedimiento"]:
				

		except Exception as ex:
			Utils.printx (f"EXCEPCION: Problemas al llenar documento '{self.jsonFilepath}'")
			print (traceback_format_exc())
			return (str(ex))

		return (f"Ingresado exitosamente el documento {self.jsonFilepath}")

if __name__ == "__main__":
	main()


