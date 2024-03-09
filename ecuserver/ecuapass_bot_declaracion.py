
import os, sys 
import pyautogui as py
from traceback import format_exc as traceback_format_exc

from ecuapass_bot import EcuBot
from ecuapassdocs.utils.ecuapass_utils import Utils

#----------------------------------------------------------
# Globals
#----------------------------------------------------------
win   = None	 # Global Ecuapass window  object
GLOBAL_PAUSE = 0.03
SLOW_PAUSE   = 0.05

def main ():
	args = sys.argv 
	jsonFilepath = args [1]
	runningDir   = os.getcwd()
	mainBotDeclaracion (jsonFilepath, runningDir)

#----------------------------------------------------------
# Main function for testing
#----------------------------------------------------------
def mainBotDeclaracion (jsonFilepath, runningDir):
	Utils.printx (f"Versión0.96. Iniciando digitación de documento '{jsonFilepath}'")
	Utils.printx (f"Directorio actual: ", os.getcwd())
	Utils.runningDir = runningDir
	result = EcuBotDeclaracion.fillEcuapass (jsonFilepath)
	return result

#--------------------------------------------------------------------
# EcuBot for filling Ecuapass cartaporte web form (in flash)
#--------------------------------------------------------------------
class EcuBotDeclaracion:
	def fillEcuapass (jsonFilepath):
		try:
			py.PAUSE = GLOBAL_PAUSE

			global win
			fieldsConfidence = Utils.readJsonFile (jsonFilepath)
			fields = Utils.removeConfidenceString (fieldsConfidence)
			
			win    = Utils.activateEcuapassWindow ()
			Utils.scrollWindowToBeginning ()
			Utils.detectEcuapassDocumentWindow ("declaracion")
			Utils.clearWebpageContent ()
			py.press ("Tab"); py.press ("Tab")

			print ("\n>>>>>> Declaración de Tránsito Aduanero Internacional <<<")
			EcuBot.fillBoxSimpleIteration  (fields, "01_Distrito"); py.press ("Tab")
			EcuBot.fillDate     (fields, "02_Fecha_Emision"); py.press ("Tab")
			EcuBot.fillBox      (fields, "03_Procedimiento"); py.press ("Tab")
			EcuBot.fillText     (fields, "04_Numero_DTAI"); py.press ("Tab")
			EcuBot.fillBox      (fields, "05_Pais_Origen"); py.press ("Tab");

			# Aduana de carga
			EcuBot.fillBox      (fields, "06_Pais_Carga"); py.press ("Tab");
			EcuBot.fillBox      (fields, "07_Aduana_Carga"); py.press ("Tab");

			# Aduana de partida
			EcuBot.fillBox      (fields, "08_Pais_Partida"); py.press ("Tab");
			EcuBot.fillBox      (fields, "09_Aduana_Partida"); py.press ("Tab");

			# Aduana de destino
			EcuBot.fillBox      (fields, "10_Pais_Destino"); py.press ("Tab");
			EcuBot.fillBox      (fields, "11_Aduana_Destino"); py.press ("Tab");

			py.press ("Tab")

		except Exception as ex:
			Utils.printx (f"EXCEPCION: Digitando documento '{jsonFilepath}'")
			Utils.printx (traceback_format_exc())
			return (str(ex))

		return (f"Ingresado exitosamente el documento {jsonFilepath}")

#--------------------------------------------------------------------
# Call to main
#--------------------------------------------------------------------
if __name__ == "__main__":
	main()

#	#--------------------------------------------------------------------
#	#-- fill text field
#	#--------------------------------------------------------------------
#	def fillText (fields, fieldName, imageName=None):
#		value = fields [fieldName]
#		Utils.printx (f"Llenando TextField '{fieldName}' : '{value}'...")
#		if value == None:
#			return
#
#		pyperclip_copy (value)
#		if imageName == None:
#			#py.write (value)
#			py.hotkey ("ctrl", "v")
#
#	#--------------------------------------------------------------------
#	#-- Fill combo box pasting text and selecting first value.
#	#-- Without check. Default value, if not found.
#	#--------------------------------------------------------------------
#	def fillBox (fields, fieldName):
#		py.PAUSE = SLOW_PAUSE
#		try:
#			while (True):
#				fieldValue = fields [fieldName]
#				if fieldValue == None:
#					break
#
#				Utils.printx (f"Llenando fillBox '{fieldName}' : '{fieldValue}'...")
#				pyperclip_copy (fieldValue)
#				py.hotkey ("ctrl", "v")
#				#py.sleep (0.5)
#				py.press ("down")
#				#py.sleep (0.5)
#
#				# Check if selection is null
#				pyperclip_copy ("")
#				py.hotkey ("ctrl", "c")
#				formValue = pyperclip_paste () 
#				print (f">>> FORM VALUE IS: '{formValue}'")
#
#				if formValue != "" and fieldValue.upper() in formValue.upper():
#					pyperclip_copy (fieldValue)
#					py.hotkey ("ctrl", "v")
#				else:
#					Utils.printx (f"No encontrado '{fieldValue}' en '{fieldName}'. Se encontró: '{formValue}'")
#					py.sleep (1)
#					continue
#					##py.press ("--")
#
#				py.press ("down")
#				py.press ("enter")
#				break
#		finally:
#			py.PAUSE = GLOBAL_PAUSE
#
#	#-- Fill Date box widget (month, year, day)
#	def fillDate (fields, fieldName):
#		#py.PAUSE = SLOW_PAUSE
#		try:
#			Utils.printx (f"Llenando campo Fecha '{fieldName}' : {fields [fieldName]}'...")
#			fechaText = fields [fieldName]
#			if (fechaText == None):
#				return
#
#			items = fechaText.split("-")
#			day, month, year = int (items[0]), int (items[1]), int (items[2])
#
#			boxDate    = EcuBot.getBoxDate ()
#			dayBox	   = boxDate [0]
#			monthBox   = boxDate [1]
#			yearBox    = boxDate [2]
#
#			py.hotkey ("ctrl", "down")
#			EcuBot.setYear  (year, yearBox)
#			EcuBot.setMonth (month, monthBox)
#			EcuBot.setDay (day)
#		finally:
#			py.PAUSE = GLOBAL_PAUSE
#
#	#-- Get current date fron date box widget
#	def getBoxDate ():
#		while True:
#			py.hotkey ("ctrl", "down")
#			py.press ("home")
#			py.hotkey ("ctrl", "a")
#			py.hotkey ("ctrl", "c")
#			text	 = pyperclip_paste ()
#			print (">>> DATE TEXT: ", text)
#			reFecha = r'\d{1,2}/\d{1,2}/\d{4}'
#			if re.match (reFecha, text):
#				boxDate  = text.split ("/") 
#				boxDate  = [int (x) for x in boxDate]
#				return (boxDate)
#			else:
#				continue
#
#	#-- Set year
#	def setYear (yearDoc, yearOCR):
#		diff = yearDoc - yearOCR
#		pageKey = "pageup" if diff < 0 else "pagedown"
#		Utils.printx (f"Localizando año. Doc: {yearDoc}. OCR: {yearOCR}. Diff: {diff}...")
#
#		for i in range (abs(diff)):
#			Utils.printx (f"Año %.2d: " % (i+1), end="")
#			for k in range (12):
#				Utils.printx (f">%.2d " % (k+1), end="")
#				py.press (pageKey)
#			Utils.printx ("")
#		Utils.printx ("")
#
#	#-- Set month
#	def setMonth (monthDoc, monthOCR):											 
#		diff = monthDoc - monthOCR
#		pageKey = "pageup" if diff < 0 else "pagedown"
#		Utils.printx (f"Localizando mes. Doc: {monthDoc}. OCR: {monthOCR}. Diff: {diff}...")
#
#		for i in range (abs(diff)):
#			Utils.printx (f"> %.2d " % (i+1), end="")
#			py.press (pageKey)
#
#	#-- Set day
#	def setDay (dayDoc):
#		try:
#			nWeeks = dayDoc // 7
#			nDays  = dayDoc % 7 - 1
#			Utils.printx (f"Localizando dia {dayDoc}. Semanas: {nWeeks}, Dias: {nDays}...")
#
#			py.press ("home")
#			[py.press ("down") for i in range (nWeeks)]
#			[py.press ("right") for i in range (nDays)]
#
#			py.press ("enter")
#		except:
#			Utils.printx (f"EXCEPTION: Al buscar el dia '{dayDoc}'")
#			raise
#
#	#------------------------------------------------------------------
#	#-- Fill box iterating, copying, comparing.
#	#------------------------------------------------------------------
#	def fillBoxSimpleIteration (fields, fieldName):
#		fieldValue = fields [fieldName].upper()
#		Utils.printx (f"Llenando simple CBox '{fieldName} : {fieldValue}'...")
#
#		lastText = "XXXYYYZZZ"
#		while True:
#			py.hotkey ("ctrl", "a");py.hotkey ("ctrl","c"); 
#			text = pyperclip_paste().upper()
#			if fieldValue in text:
#				Utils.printx (f"\t\t Encontrado {fieldValue} en {text}") 
#				py.press ("enter"); 
#				break
#
#			if (text == lastText):
#				Utils.printx (f"\t\t No se pudo encontrar '{fieldValue}'!")
#				break
#
#			py.press ("down");
#			lastText = text 
#
#	#-- fill text field with selection
#	def fillTextSelection (fields, fieldName, imageName=None):
#		EcuBot.fillText (fields, fieldName, imageName)
#		py.press ("Enter")
#
#	#-- fill combo box iterating over all values (Ctrl+x+v+a+back)
#	def fillCBoxFieldByIterating (fields, fieldName):
#		#py.pause = 0.05
#		fieldValue = fields [fieldName].lower()
#		Utils.printx (f"> >> Llenando CBox iterando uno a uno '{fieldName} : {fieldValue}'...")
#
#		py.hotkey ("ctrl","c"); py.hotkey ("ctrl","v"); py.hotkey ("ctrl","a");
#		py.press ("backspace");
#		py.press ("down");
#
#		lastText = "XXXYYYZZZ"
#		while True:
#			py.hotkey ("ctrl","c"); py.hotkey ("ctrl","v")
#			text = pyperclip_paste().lower()
#			value = Utils.strCompare (fieldValue, text) 
#			Utils.printx (f"\t\t Comparando texto campo '{fieldValue}' con texto CBox '{text}', valor: {value}")
#			#if value > 0.8:
#			if fieldValue in text:
#				Utils.printx (f"\t\t Encontrado!") 
#				py.press ("enter"); py.press ("enter")
#				break
#
#			if (text == lastText):
#				Utils.printx (f"\t\tERROR: No se pudo encontrar '{fieldValue}'!")
#				break
#
#			py.hotkey ("ctrl","a"); py.press ("backspace"); py.press ("down");
#			lastText = text 
#
#
#
#
#if __name__ == "__main__":
#	main()
