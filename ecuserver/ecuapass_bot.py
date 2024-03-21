import re, os, sys, json
import pyautogui as py
import keyboard as kb

import pyperclip
from pyperclip import copy as pyperclip_copy
from pyperclip import paste as pyperclip_paste

from traceback import format_exc as traceback_format_exc
from ecuapassdocs.utils.ecuapass_utils import Utils

#----------------------------------------------------------
# Globals
#----------------------------------------------------------
win   = None	 # Global Ecuapass window  object

# Deprecated: Declared as attributes
#GLOBAL_PAUSE = 0.05
#SLOW_PAUSE   = 0.1

#----------------------------------------------------------
# General Bot class with basic functions of auto completing
#----------------------------------------------------------
class EcuBot:
	# Load data, check/clear browser page
	def __init__(self, jsonFilepath, runningDir, docType):
		Utils.printx (f"Versión0.981. Iniciando ingreso de documento '{jsonFilepath}'")
		Utils.printx (f"Directorio actual: ", os.getcwd())

		self.jsonFilepath = jsonFilepath   
		self.runningDir   = runningDir     
		self.docType      = docType

		fieldsConfidence    = Utils.readJsonFile (self.jsonFilepath)
		self.fields         = Utils.removeConfidenceString (fieldsConfidence)
		self.notFilledFields = []     # List of fields not filled by the bot

		# Read settings 
		settingsPath       = os.path.join (runningDir, "settings.txt")
		settings           = json.load (open (settingsPath, encoding="utf-8")) 
		self.empresa       = settings ["empresa"]
		self.GLOBAL_PAUSE  = float (settings ["global_pause"])
		self.SLOW_PAUSE    = float (settings ["slow_pause"])
		#self.FILL_PAUSE   = float (settings ["fill_pause"])
		py.PAUSE           = self.GLOBAL_PAUSE

		Utils.printx (">>> BOT Settings:")
		Utils.printx (f"\t>>> Company: <{settings ['empresa']}>")
		Utils.printx (f"\t>>> Global pause: <{settings ['global_pause']}>")
		Utils.printx (f"\t>>> Slow pause: <{settings ['slow_pause']}>")

	#-- Check/init Ecuapass window
	def initEcuapassWindow (self):
		Utils.printx ("Iniciando ventana de ECUAPASS...")
		
		self.win    = self.activateEcuapassWindow ()
		self.maximizeWindow (self.win)
		self.scrollWindowToBeginning ()
		self.detectEcuapassDocumentWindow (self.docType)
		self.clearWebpageContent ()

	#-- Select first item from combo box
	def selFirstItemFromBox  (self):
		py.press ("down")
		py.press ("enter")

	#--------------------------------------------------------------------
	# Detects if cursor is over find button
	#--------------------------------------------------------------------
	def isOnFindButton_usingTextCopyPaste (self):
		py.press ("X")
		pyperclip.copy(''); py.hotkey ("ctrl", "a"); py.hotkey ("ctrl","c"); 
		text   = pyperclip.paste()
		if text == "X":
			print ("-- Not, in find button")
			py.hotkey ("ctrl", "a"); py.press ("del"); 
			return False
		else:
			print ("-- Yes, in find button")
			return True
			
	#-- Detect if is on find button using image icon
	def isOnFindButton (self):
		Utils.printx ("Localizando botón de búsqueda...")
		filePaths = Utils.imagePath ("image-button-FindRUC")
		for fpath in filePaths:
			print (">>> Probando: ", os.path.basename (fpath))
			xy = py.locateCenterOnScreen (fpath, confidence=0.90, grayscale=False)
			if (xy):
				print (">>> Detectado")
				return True


	#--------------------------------------------------------------------
	# fill subject fields taking into account RUC info, if exists.
	#--------------------------------------------------------------------
	def fillSubject (self, subjectType, fieldProcedimiento, fieldPais, fieldTipoId, 
	                 fieldNumeroId, fieldNombre, fieldDireccion, fieldCertificado=None):
		procedimiento = self.fields [fieldProcedimiento]
		for i in range (2):
			self.fillBox (fieldPais); py.press ("Tab")
			self.fillBox (fieldTipoId); py.press ("Tab")
			self.fillText (fieldNumeroId); py.press ("Tab")
			if self.empresa == "NTA":
				if procedimiento == "IMPORTACION" and subjectType == "REMITENTE":
					break                
				elif procedimiento == "EXPORTACION" and subjectType != "REMITENTE":
					break                
			[py.hotkey ("shift", "Tab") for k in range (3) if i < 1]
			py.sleep (0.5)

		if self.isOnFindButton ():
			py.press ("space"); 
			while self.isOnFindButton ():
				print ("... in find RUC button ...")
				py.sleep (0.1)
		else:
			if subjectType == "REMITENTE":
				self.fillText (fieldCertificado); py.press ("Tab")
			self.fillText (fieldNombre); py.press ("Tab")

		self.fillText (fieldDireccion); py.press ("Tab")

	#--------------------------------------------------------------------
	# Fill one of three radio buttons (PO, CI, PEOTP) according to input info
	#--------------------------------------------------------------------
	def fillRButton (self, fieldName):
		value = self.fields [fieldName]
		if (value == "1"):
			py.press ("Tab")
		else:
			py.press ("right")

	#--------------------------------------------------------------------
	#-- fill text field
	#--------------------------------------------------------------------
	def fillText (self, fieldName, PAUSE=None):
		value = None
		py.PAUSE = self.SLOW_PAUSE
		try:
			value = self.fields [fieldName]
			Utils.printx (f"Llenando TextField '{fieldName}' : '{value}'...")
			if value == None:
				return

			pyperclip_copy (value)
			py.hotkey ("ctrl", "v")
			py.sleep (self.SLOW_PAUSE)
		finally:
			py.PAUSE = self.GLOBAL_PAUSE
		return value

	#--------------------------------------------------------------------
	#-- Fill combo box pasting text and selecting first value.
	#-- Without check. Default value, if not found.
	#-- Using keyboard library instead pyautogui
	#--------------------------------------------------------------------
	def fillBox (self, fieldName, PAUSE=None):
		py.PAUSE = self.SLOW_PAUSE
		try:
			fieldValue = self.fields [fieldName]
			Utils.printx (f"Llenando CombolBox '{fieldName}' : '{fieldValue}'...")
			if fieldValue == None:
				return

			pyperclip_copy (fieldValue)
			py.hotkey ("ctrl", "v")
			py.sleep (self.SLOW_PAUSE)
			py.press ("down")
			py.sleep (self.SLOW_PAUSE)
			return
		finally:
			py.PAUSE = self.GLOBAL_PAUSE

	#------------------------------------------------------------------
	#-- Fill box iterating, copying, comparing.
	#------------------------------------------------------------------
	def fillBoxSimpleIteration (self, fieldName):
		fieldValue = self.fields [fieldName]
		Utils.printx (f"Llenando simple CBox '{fieldName} : {fieldValue}'...")

		lastText = "XXXYYYZZZ"
		nLastText = 0
		while True:
			py.sleep (0.05)
			py.hotkey ("ctrl", "a", "c");
			py.sleep (0.05)
			text = pyperclip_paste().upper()
			print (f">>> Buscando valor:'{fieldValue}' en texto de CBOX: '{text}'")
			if fieldValue.upper() in text:
				Utils.printx (f"\t\t Encontrado {fieldValue} en {text}") 
				py.press ("enter"); 
				break

			if (text == lastText):
				nLastText += 1
				if nLastText > 2:
					Utils.printx (f"\t\t No se pudo encontrar '{fieldValue}'!")
					self.notFilledFields.append ((fieldName, fieldValue))
					py.press ("home")
					break

			py.press ("down");
			lastText = text 

	#-- fill text field with selection
	def fillTextSelection (self, fieldName, imageName=None):
		self.fillText (self.fields, fieldName, imageName)
		py.press ("Enter")

	#-- fill combo box iterating over all values (Ctrl+x+v+a+back)
	def fillCBoxFieldByIterating (self, fieldName):
		#py.pause = 0.05
		fieldValue = self.fields [fieldName].lower()
		Utils.printx (f"> >> Llenando CBox iterando uno a uno '{fieldName} : {fieldValue}'...")

		py.hotkey ("ctrl","c"); py.hotkey ("ctrl","v"); py.hotkey ("ctrl","a");
		py.press ("backspace");
		py.press ("down");

		lastText = "XXXYYYZZZ"
		while True:
			py.hotkey ("ctrl","c"); py.hotkey ("ctrl","v")
			text = pyperclip_paste().lower()
			value = Utils.strCompare (fieldValue, text) 
			Utils.printx (f"\t\t Comparando texto campo '{fieldValue}' con texto CBox '{text}', valor: {value}")
			#if value > 0.8:
			if fieldValue in text:
				Utils.printx (f"\t\t Encontrado!") 
				py.press ("enter"); py.press ("enter")
				break

			if (text == lastText):
				Utils.printx (f"\t\tERROR: No se pudo encontrar '{fieldValue}'!")
				break

			py.hotkey ("ctrl","a"); py.press ("backspace"); py.press ("down");
			lastText = text 

	#-------------------------------------------------------------------
	#-- Fill Date box widget (month, year, day)
	#-------------------------------------------------------------------
	def fillDate (self, fieldName):
		#py.PAUSE = self.SLOW_PAUSE
		try:
			Utils.printx (f"Llenando campo Fecha '{fieldName}' : {self.fields [fieldName]}'...")
			fechaText = self.fields [fieldName]
			if (fechaText == None):
				return

			items = fechaText.split("-")
			day, month, year = int (items[0]), int (items[1]), int (items[2])

			boxDate    = self.getBoxDate ()
			dayBox	   = boxDate [0]
			monthBox   = boxDate [1]
			yearBox    = boxDate [2]

			py.hotkey ("ctrl", "down")
			self.setYear  (year, yearBox)
			self.setMonth (month, monthBox)
			self.setDay (day)
		finally:
			py.PAUSE = self.GLOBAL_PAUSE

	#-- Get current date fron date box widget
	def getBoxDate (self):
		while True:
			py.hotkey ("ctrl", "down")
			py.press ("home")
			py.hotkey ("ctrl", "a")
			py.hotkey ("ctrl", "c")
			text	 = pyperclip_paste ()
			reFecha = r'\d{1,2}/\d{1,2}/\d{4}'
			if re.match (reFecha, text):
				boxDate  = text.split ("/") 
				boxDate  = [int (x) for x in boxDate]
				return (boxDate)
			else:
				continue

	#-- Set year
	def setYear (self, yearDoc, yearOCR):
		diff = yearDoc - yearOCR
		pageKey = "pageup" if diff < 0 else "pagedown"
		pageSign = "-" if diff < 0 else "+"
		Utils.printx (f"Localizando año. Doc: {yearDoc}. OCR: {yearOCR}. Diff: {diff}...")

		for i in range (abs(diff)):
			py.hotkey ("shift", pageSign)

	#-- Set month
	def setMonth (self, monthDoc, monthOCR):											 
		diff = monthDoc - monthOCR
		pageKey = "pageup" if diff < 0 else "pagedown"
		Utils.printx (f"Localizando mes. Doc: {monthDoc}. OCR: {monthOCR}. Diff: {diff}...")

		for i in range (abs(diff)):
			Utils.printx (f"> %.2d " % (i+1), end="")
			py.press (pageKey)

	#-- Set day
	def setDay (self, dayDoc):
		try:
			nWeeks = dayDoc // 7
			nDays  = dayDoc % 7 - 1
			Utils.printx (f"Localizando dia {dayDoc}. Semanas: {nWeeks}, Dias: {nDays}...")

			py.press ("home")
			[py.press ("down") for i in range (nWeeks)]
			[py.press ("right") for i in range (nDays)]

			py.press ("enter")
		except:
			Utils.printx (f"EXCEPTION: Al buscar el dia '{dayDoc}'")
			raise


	#----------------------------------------------------------------
	#-- Function for windows management
	#----------------------------------------------------------------
	#-- Detect ECUAPASS window
	def detectWindowByTitle (self, titleString):
		Utils.printx (f"Detectando ventana '{titleString}'...")
		windows = py.getAllWindows ()
		for win in windows:
			if titleString in win.title:
				return win

		raise Exception (f"ALERTA: No se detectó ventana '{titleString}' ")

	#-- Maximize window by minimizing and maximizing
	def maximizeWindow (self, win):
		SLEEP=0.2
		win.minimize (); py.sleep (SLEEP)
		win.maximize (); py.sleep (SLEEP)
		#win.activate (); #py.sleep (SLEEP)
		win.resizeTo (py.size()[0], py.size()[1]); py.sleep (SLEEP)

	def activateWindowByTitle (self, titleString):
		SLEEP=0.2
		ecuWin = self.detectWindowByTitle (titleString)
		Utils.printx (f"Activando ventana '{titleString}'...")
		
		if ecuWin.isMinimized:
			ecuWin.restore (); py.sleep (SLEEP)

		return (ecuWin)

	#-- Detect and activate ECUAPASS-browser/ECUAPASS-DOCS window
	def activateEcuapassWindow (self):
		return self.activateWindowByTitle ('ECUAPASS - SENAE browser')

	def activateEcuapassDocsWindow (self):
		return self.activateWindowByTitle ('Ecuapass-Docs')

	#-- Clear previous webpage content clicking on "ClearPage" button
	def clearWebpageContent (self):
		Utils.printx ("Localizando botón de borrado...")
		filePaths = Utils.imagePath ("image-button-ClearPage")
		for fpath in filePaths:
			print (">>> Probando: ", os.path.basename (fpath))
			xy = py.locateCenterOnScreen (fpath, confidence=0.80, grayscale=True)
			if (xy):
				print (">>> Detectado")
				py.click (xy[0], xy[1], interval=1)    
				return True

		raise Exception ("ALERTA: No se detectó botón de borrado")
		
	#-- Scroll to the page beginning 
	def scrollWindowToBeginning (self):
		Utils.printx ("Desplazando página hasta el inicio...")
		filePaths = Utils.imagePath ("image-button-ScrollUp")
		for fpath in filePaths:
			print (">>> Probando: ", os.path.basename (fpath))
			xy = py.locateCenterOnScreen (fpath, confidence=0.80, grayscale=True)
			if (xy):
				print (">>> Detectado")
				py.mouseDown (xy[0], xy[1])
				py.sleep (3)
				py.mouseUp (xy[0], xy[1])
				return True

		raise Exception ("ALERTA: No se detectó botón de scroll-up")

	#-- Check if active webpage contains correct text 
	def detectEcuapassDocumentWindow (self, docName):
		Utils.printx (f"Detectando página de '{docName}' activa...")
		docFilename = "";
		if docName == "cartaporte":
			docFilename = "image-text-Cartaporte"; 
		elif docName == "manifiesto":
			docFilename = "image-text-Manifiesto"; 
		elif docName == "declaracion":
			docFilename = "image-text-DeclaracionTransito.png"; 

		filePaths = Utils.imagePath (docFilename)
		for fpath in filePaths:
			print (">>> Probando: ", os.path.basename (fpath))
			xy = py.locateCenterOnScreen (fpath, confidence=0.80, grayscale=True)
			if (xy):
				print (">>> Detectado")
				return True

		raise Exception (f"ALERTA: No se detectó la página de '{docName}' ")

	#-- Click on selected cartaporte
	def clickSelectedCartaporte (self, fieldName):
		Utils.printx ("Localizando cartaporte...")
		xy = py.locateCenterOnScreen (Utils.imagePath ("image-text-blue-TERRESTRE-manifiesto.png"), 
				confidence=0.7, grayscale=False)
		if (xy):
			print (">>> Cartaporte detectada")
			py.click (xy[0], xy[1], interval=1)    
			return True

		fieldValue = self.fields [fieldName]
		self.notFilledFields.append ((fieldName, fieldValue))
		Utils.printx ("ALERTA: No se detectó cartaporte seleccionada")

	#-- Create message with fields not filled
	def createResultsMessage (self):
		msgs = [f"ALERTA: Finalizada la digitación"]
		if self.notFilledFields != []:
			msgs.append ("Los siguientes campos no se pudieron llenar:")
			for field in self.notFilledFields:
				msgs.append (f"{field [0]} : {field [1]}")

		message = "\\".join (msgs)
		return (message)

if __name__ == "__main__":
	main()
