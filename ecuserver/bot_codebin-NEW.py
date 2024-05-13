#!/usr/bin/env python3

"""
Fill CODEBIN web form from JSON fields document.
"""
import sys, json, re, time, os
import PyPDF2

from threading import Thread as threading_Thread

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from ecuapassdocs.info.ecuapass_utils import Utils
from ecuapassdocs.info.resourceloader import ResourceLoader 
from ecuapassdocs.info.ecuapass_info_cartaporte import CartaporteInfo

#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv
	option = args [1]
	print ("--option:", option)

	if "--getEcudocsValues" in option:
		print (">> Running getEcudocsValues...")
		pdfFilepath = args [2]
		codebinBot = CodebinBot ("BYZA")
		codebinBot.getEcudocsValuesFromCodebinWeb (pdfFilepath)
		
	elif "--getcodebinvalues" in option:
		#---- Extract data from CODEBIN --------------------------------- 
		botCodebin = CodebinBot ()
		botCodebin.getValuesFromRangeCodebinCartaportes ("colombia")

	elif "--cleancodebincartaportes" in option:
		#---- Remove invalid records (e.g. no remitente)
		inDir = args [2]
		cleanCodebinCartaportesFiles (inDir)

#----------------------------------------------------------------
# Bot for filling CODEBIN forms from ECUDOCS fields info
#----------------------------------------------------------------
class CodebinBot:
	def __init__ (self, settings, webdriver, codebinFieldsFile=None):
		self.settings          = settings
		self.empresa           = settings ["empresa"]
		self.codebinUrl        = settings ["codebin_url"]
		self.codebinUser       = settings ["codebin_user"]
		self.codebinPassword   = settings ["codebin_password"]

		self.codebinFieldsFile = codebinFieldsFile

		self.webdriver            = webdriver

	#------------------------------------------------------
	# Start Firefox Web Server for CODEBIN session
	#------------------------------------------------------
	@staticmethod
	def getWebdriver ():
		while not hasattr (CodebinBot, "webdriver"):
			Utils.printx ("...Waiting for Codebin webdriver")
			time.sleep (2)
		return CodebinBot.webdriver

	@staticmethod
	def initCodebinFirefoxWebDriver ():
		Utils.printx (">>>>>>>>>>>>>>>> Iniciando CODEBIN firefox <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
		def funThreadFirefox ():
			options = Options()
			options.add_argument("--headless")
			#CodebinBot.webdriver = webdriver.Firefox (options=options)
			CodebinBot.webdriver = CodebinBot.openCodebinWeb ()
			#CodebinBot.webdriver.get (self.codebinUrl)
			Utils.printx (">>>>>>>>>>>>>>>> CODEBIN firefox is running <<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

		threadFirefox = threading_Thread (target=funThreadFirefox, args=())
		threadFirefox.start ()

	#-----------------------------------------------------------------
	#-----------------------------------------------------------------
	def getValuesFromCodebinWeb (docFilepath, settings):
		webdriver = CodebinBot.getWebdriver ()
		codebinBot = CodebinBot (settings, webdriver)
		fieldsJsonFile = codebinBot.getEcudocsValuesFromCodebinWeb (docFilepath)
		return fieldsJsonFile

	#-------------------------------------------------------------------
	# Get document values from CODEBIN web using PDF file doc number
	#-------------------------------------------------------------------
	def getEcudocsValuesFromCodebinWeb (self, pdfFilepath):
		try:
			ecudocsJsonFile = None

			self.docType = Utils.getDocumentTypeFromFilename (pdfFilepath)
			docNumber    = Utils.getDocumentNumberFromFilename (pdfFilepath)

			if self.docType == "CARTAPORTE":
				linkDocument  = "https://byza.corebd.net/1.cpi/nuevo.cpi.php?modo=3&idunico=%s"
				textMainmenu  = "Carta Porte I"
				textSubmenu   = "1.cpi/lista.cpi.php?todos=todos"
				docPrefix     = "CPI"

			elif self.docType == "MANIFIESTO":
				linkDocument  = "https://byza.corebd.net/2.mci/nuevo.mci.php?modo=3&idunico=%s"
				textMainmenu  = "Manifiesto de Carga"
				textSubmenu   = "2.mci/lista.mci.php?todos=todos"
				docPrefix     = "MCI"
			else:
				print ("Tipo de documento no soportado:", self.docType)

			# Get codebin values from CODEBIN web
			codebinValues = self.getCodebinValuesFromCodebinWeb (docNumber, textMainmenu, textSubmenu, linkDocument)

			# Format to Azure values
			azureValues = Utils.getAzureValuesFromCodebinValues (self.docType, codebinValues, docNumber)
			# Save data
			outCbinFilename = f"{docPrefix}-{self.empresa}-{docNumber}-CBINFIELDS.json"
			outDocFilename  = f"{docPrefix}-{self.empresa}-{docNumber}-DOCFIELDS.json"
			json.dump (codebinValues, open (outCbinFilename, "w"), indent=4)
			json.dump (azureValues, open (outDocFilename, "w"), indent=4, sort_keys=True)

			#self.webdriver.close ()
			return outDocFilename
		except:
			Utils.printException ()
			raise Exception (f"ALERTA: Applicación no pudo conectarse con CODEBIN. Revise URL, usuario y contraseña") 


	#-------------------------------------------------------------------
	#-- Get the CODEBIN id from document number
	#-- List documents, search the number, and get the id of selected
	#-------------------------------------------------------------------
	def getCodebinValuesFromCodebinWeb (self, docNumber, textMainmenu, textSubmenu, linkDocument):
		pais, codigoPais  = Utils.getPaisCodigoFromDocNumber (docNumber)
		
		self.webdriver = CodebinBot.openCodebinWeb ()
		self.login (pais)

		# Select menu Carta Porte I
		cpi = self.webdriver.find_element (By.PARTIAL_LINK_TEXT, textMainmenu)
		cpi.click ()

		# Select submenu 'Lista'
		cpi_lista = self.webdriver.find_element (By.XPATH, f"//a[contains(@href, '{textSubmenu}')]")
		cpi_lista.click ()

		# Get and swithc to frame 'Lista'
		cpi_lista_object = self.webdriver.find_element (By.TAG_NAME, "object")
		wait = WebDriverWait (self.webdriver, 2)
		wait.until (EC.frame_to_be_available_and_switch_to_it (cpi_lista_object))
		time.sleep (1)

		# get and set number into input 'Buscar'
		cpi_lista_container = self.webdriver.find_elements (By.CLASS_NAME, "container")
		container = cpi_lista_container [0]
		time.sleep (1)
		cpi_lista_buscar    = container.find_element (By.TAG_NAME, "input")
		cpi_lista_buscar.send_keys (docNumber)

		# Get table, get row, and extract id
		table   = container.find_element (By.TAG_NAME, "table")
		docLink = table.find_element (By.PARTIAL_LINK_TEXT, docNumber)
		idText  = docLink.get_attribute ("onclick")
		docId   = re.findall (r"\d+", idText)[-1]
		
		# Get CODEBIN link for document with docId
		self.webdriver.get (linkDocument % docId)

		# Get Codebin values from document form
		docForm       = self.webdriver.find_element (By.TAG_NAME, "form")
		codebinValues = self.getCodebinValuesFromCodebinForm (docForm, codigoPais, docNumber)

		# Store the handle of the original window
		original_window = self.webdriver.current_window_handle	

		for handle in self.webdriver.window_handles:
			self.webdriver.switch_to.window (handle)
			current_title = self.webdriver.title

			if "GRUPO BYZA SAS" in current_title:
				self.webdriver.close()  # Close the window with the matching title
				break  # Exit the loop once the target window is closed		

		self.webdriver.switch_to.window (original_window)

		return codebinValues

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	@staticmethod
	def openCodebinWeb ():
		print (f">> Opening CODEBIN web...")
		# Open and click on "Continuar" button
		if not hasattr (CodebinBot, "webdriver"):
			Utils.printx ("Iniciando servidor desde login...")
			#self.webdriver = webdriver.Firefox ()
			CodebinBot.webdriver = webdriver.Firefox ()
			CodebinBot.webdriver.get ("https://byza.corebd.net")
			submit_button = CodebinBot.webdriver.find_element(By.XPATH, "//input[@type='submit']")
			submit_button.click()

			# Open new window with login form, then switch to it
			time.sleep (2)
			winMenu = CodebinBot.webdriver.window_handles [-1]
			CodebinBot.webdriver.switch_to.window (winMenu)

			loginForm = CodebinBot.webdriver.find_element (By.TAG_NAME, "form")
			print ("--", loginForm)
			submit_button = CodebinBot.webdriver.find_element(By.XPATH, "//input[@type='submit']")
			print ("--s", submit_button)

			userInput = loginForm.find_element (By.NAME, "user")

			return CodebinBot.webdriver

	#-------------------------------------------------------------------
	# Returns the web driver after login into CODEBIN
	#-------------------------------------------------------------------
	def login (self, pais):
		# Login Form : fill user / password
		loginForm = CodebinBot.webdriver.find_element (By.TAG_NAME, "form")
		print ("--", loginForm)

		submit_button = CodebinBot.webdriver.find_element(By.XPATH, "//input[@type='submit']")
		print ("--s", submit_button)

		userInput = loginForm.find_element (By.NAME, "user")
		#userInput.send_keys ("GRUPO BYZA")
		userInput.send_keys (self.codebinUser)
		pswdInput = loginForm.find_element (By.NAME, "pass")
		#pswdInput.send_keys ("GrupoByza2020*")
		pswdInput.send_keys (self.codebinPassword)

		# Login Form:  Select pais (Importación or Exportación : Colombia or Ecuador)
		docSelectElement = self.webdriver.find_element (By.XPATH, "//select[@id='tipodoc']")
		docSelect = Select (docSelectElement)
		docSelect.select_by_value (pais)
		submit_button = loginForm.find_element (By.XPATH, "//input[@type='submit']")
		submit_button.click()

		return self.webdriver

		
	#----------------------------------------------------
	# Get codebin fields : {codebinField:value}
	#----------------------------------------------------
	def getCodebinValuesFromCodebinForm (self, docForm, codigoPais, docNumber):
		fields  = self.getParamFields () 
		codebinValues = {}
		for key in fields.keys():
			codebinField = fields [key]["codebinField"]
			try:
				elem = docForm.find_element (By.ID, codebinField)
				value = elem.get_attribute ("value")
				codebinValues [codebinField] = value
			except NoSuchElementException:
				print (f"...Elemento '{codebinField}'  no existe")
				pass

		# For MANIFIESTO: Get selected radio button 
		if self.docType == "CARTAPORTE":
			codebinValues ["nocpic"] = docNumber
		elif self.docType == "MANIFIESTO":
			codebinValues ["no"] = docNumber

			radio_group = docForm.find_elements (By.NAME, "r25")  # Assuming radio buttons have name="size"
			for radio_button in radio_group:
				codebinField = radio_button.get_attribute('id')
				if radio_button.is_selected():
					codebinValues [codebinField] = "X"
				else:
					codebinValues [codebinField] = ""

		return codebinValues

	#-------------------------------------------------------------------
	# Get a list of cartaportes from range of ids
	#-------------------------------------------------------------------
	def getValuesFromRangeCodebinCartaportes (self, pais):
		self.docType = "CARTAPORTE"
		self.login (pais)
		linkCartaporte = "https://byza.corebd.net/1.cpi/nuevo.cpi.php?modo=3&idunico=%s"

		for docId in range (121, 7075):
			docLink = linkCartaporte % docId
			self.webdriver.get (docLink)

			docForm = self.webdriver.find_element (By.TAG_NAME, "form")
			self.createParamsFileFromCodebinForm (docForm)

	#----------------------------------------------------
	# Create params file: 
	#   {paramsField: {ecudocField, codebinField, value}}
	#----------------------------------------------------
	def createParamsFileFromCodebinForm (self, docForm):
		fields  = self.getParamFields () 
		for key in fields.keys():
			codebinField = fields [key]["codebinField"]
			try:
				elem = docForm.find_element (By.NAME, codebinField)
				fields [key]["value"] = elem.get_attribute ("value")
			except NoSuchElementException:
				#print (f"...Elemento '{codebinField}'  no existe")
				pass

		pais, codigo = "NONE", "NO" 
		textsWithCountry = [fields[x]["value"] for x in ["txt02"]]
		if any (["COLOMBIA" in x.upper() for x in textsWithCountry]):
			pais, codigo = "COLOMBIA", "CO"
		elif any (["ECUADOR" in x.upper() for x in textsWithCountry]):
			pais, codigo = "ECUADOR", "EC"
			

		fields ["txt0a"]["value"] = pais

		docNumber = f"{codigo}{fields ['numero']['value']}"
		fields ["numero"]["value"] = docNumber
		fields ["txt00"]["value"]  = docNumber
		jsonFilename = f"CPI-{self.empresa}-{docNumber}-PARAMSFIELDS.json"
		json.dump (fields, open (jsonFilename, "w"), indent=4, default=str)

	#----------------------------------------------------------------
	#-- Create CODEBIN fields from document fields using input parameters
	#-- Add three new fields: idcpic, cpicfechac, ref
	#----------------------------------------------------------------
	def getParamFields (self):
		try:
			inputsParamsFile = self.getInputParametersFile ()
			inputsParams     = ResourceLoader.loadJson ("docs", inputsParamsFile)
			fields           = {}
			for key in inputsParams:
				ecudocsField  = inputsParams [key]["ecudocsField"]
				codebinField = inputsParams [key]["codebinField"]
				fields [key] = {"ecudocsField":ecudocsField, "codebinField":codebinField, "value":""}

			if self.docType == "CARTAPORTE":
				fields ["id"]             = {"ecudocsField":"id", "codebinField":"idcpic", "value":""}
				fields ["numero"]         = {"ecudocsField":"numero", "codebinField":"nocpic", "value":""}
				fields ["fecha_creacion"] = {"ecudocsField":"fecha_creacion", "codebinField":"cpicfechac", "value":""}
				fields ["referencia"]     = {"ecudocsField": "referencia", "codebinField":"ref", "value":""}

			return fields
		except: 
			raise Exception ("Obteniendo campos de CODEBIN")

	#----------------------------------------------------------------
	#----------------------------------------------------------------
	def getEcudocCodebinFields (self):
		try:
			inputsParamsFile = self.getInputParametersFile ()
			inputsParams     = ResourceLoader.loadJson ("docs", self.inputsParams)
			fields           = {}
			for key in inputsParams:
				ecudocsField = inputsParams [key]["ecudocsField"]
				codebinField = inputsParams [key]["codebinField"]
				if codebinField:
					fields [ecudocsField]  = {"codebinField":codebinField, "value":""}

			if self.docType == "CARTAPORTE":
				fields ["id"]             = {"codebinField":"idcpic", "value":""}
				fields ["fecha_creacion"] = {"codebinField":"cpicfechac", "value":""}
				fields ["referencia"]     = {"codebinField":"ref", "value":""}

			return fields
		except: 
			raise Exception ("Obteniendo campos de CODEBIN")

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	def transmitFileToCodebin (self, codebinFieldsFile):
		docType = Utils.getDocumentTypeFromFilename (codebinFieldsFile)
		Utils.printx (f">> Transmitiendo '{docType}' a codebin")
		codebinFields = json.load (open (codebinFieldsFile))
		pais = codebinFields.pop ("pais")

		self.login (pais)
		if docType == "CARTAPORTE":
			docFrame = self.getDocumentFrame ("frame", "Carta Porte", "1", "cpi", "nuevo")
		elif docType == "MANIFIESTO":
			docFrame = self.getDocumentFrame ("frame", "Manifiesto de Carga", "2", "mci", "nuevo")

		self.fillForm (docFrame, codebinFields)

	#-----------------------------------------------
	# Get links elements from document
	#-----------------------------------------------
	def printLinksFromDocument (self, docFrame):
		elements = docFrame.find_elements (By.XPATH, "//a")
		for elem in elements:
			print ("--", elem)
			print ("----", elem.get_attribute ("text"))

	#-------------------------------------------------------------------
	# Click "Cartaporte"|"Manifiesto" then "Nuevo" returning document frame
	#-------------------------------------------------------------------
	def getDocumentFrame (self, tagName, menuStr, optionNum, itemStr, functionStr):
		try:
			iniLink = self.webdriver.find_element (By.PARTIAL_LINK_TEXT, menuStr)
			iniLink.click()

			# Open frame
			#linkString = f"//a[contains(@href, '{optionNum}.{itemStr}/nuevo.{itemStr}.php?modo=1')]"
			#linkString = f"//a[contains(@href, '{optionNum}.{itemStr}/{functionStr}.{itemStr}.php?todos=todos')]"
			linkString = f"//a[contains(@href, '{optionNum}.{itemStr}/{functionStr}.{itemStr}.php?todos=todos')]"
			print ("-- linkString:", linkString)
			iniLink = self.webdriver.find_element (By.XPATH, linkString)
			iniLink.click()

			# Switch to the frame or window containing the <object> element
			object_frame = self.webdriver.find_element (By.TAG_NAME, "object")
			print ("-- object frame:", object_frame)
			wait = WebDriverWait (self.webdriver, 2)  # Adjust the timeout as needed
			wait.until (EC.frame_to_be_available_and_switch_to_it (object_frame))

			self.printLinksFromDocument (object_frame)
			print ("-- Waiting for form...")

			# Explicitly wait for the form to be located
			docForm = WebDriverWait(self.webdriver, 10).until(
				EC.presence_of_element_located((By.TAG_NAME, tagName))
			)

			return docForm
		except Exception as e:
			Utils.printx("No se pudo crear document nuevo en el CODEBIN")
			return None

	#-----------------------------------------------------------
	#-- Fill CODEBIN form fields with ECUDOC fields
	#-----------------------------------------------------------
	def fillForm (self, docForm, codebinFields):
		CARTAPORTE  = self.docType == "CARTAPORTE"
		MANIFIESTO  = self.docType == "MANIFIESTO"
		DECLARACION = self.docType == "DECLARACION"

		for field in codebinFields.keys():
			value = codebinFields [field]
			if not value:
				continue

			# Reception data copied to the others fields
			if CARTAPORTE and field in ["lugar2", "lugaremision"]:
				continue

			# Totals calculated automatically
			elif CARTAPORTE and field in ["totalmr", "monedat", "totalmd", "monedat2"]:
				continue

			# Radio button group
			elif MANIFIESTO and "radio" in field:
				elem = docForm.find_element (By.ID, field)
				self.wedriver.execute_script("arguments[0].click();", elem)

			# Tomados de la BD del vehículo y de la BD del conductor
			elif MANIFIESTO and field in ["a9", "a10", "a11", "a12"] and \
				field in ["a19", "a20", "a21", "a22"]:
				continue  

			# Tomados de la BD de la cartaporte
			elif MANIFIESTO and field in ["a29","a30","a31","a32a","a32b",
			                              "a33","a34a","a34b","a34c","a34d","a40"]:
				continue  

			else:
				elem = docForm.find_element (By.NAME, field)
				#elem.click ()
				elem.send_keys (value.replace ("\r\n", "\n"))

	#-----------------------------------------------------------
	#-- Get CODEBIN values from form with ECUDOC fields
	#-----------------------------------------------------------
	def getDataFromForm (self, docForm, codebinFields):
		CARTAPORTE  = self.docType == "CARTAPORTE"
		MANIFIESTO  = self.docType == "MANIFIESTO"
		DECLARACION = self.docType == "DECLARACION"

		for field in codebinFields.keys():
			value = codebinFields [field]
			if not value:
				continue

			# Reception data copied to the others fields
			if CARTAPORTE and field in ["lugar2", "lugaremision"]:
				continue

			# Totals calculated automatically
			elif CARTAPORTE and field in ["totalmr", "monedat", "totalmd", "monedat2"]:
				continue

			# Radio button group
			elif MANIFIESTO and "radio" in field:
				elem = docForm.find_element (By.ID, field)
				self.wedriver.execute_script("arguments[0].click();", elem)

			# Tomados de la BD del vehículo y de la BD del conductor
			elif MANIFIESTO and field in ["a9", "a10", "a11", "a12"] and \
				field in ["a19", "a20", "a21", "a22"]:
				continue  

			# Tomados de la BD de la cartaporte
			elif MANIFIESTO and field in ["a29","a30","a31","a32a","a32b",
			                              "a33","a34a","a34b","a34c","a34d","a40"]:
				continue  

			else:
				elem = docForm.find_element (By.NAME, field)
				#elem.click ()
				elem.send_keys (value.replace ("\r\n", "\n"))

	#-------------------------------------------------------
	#-- Return input parameters file
	#-------------------------------------------------------
	def getInputParametersFile (self):
		if self.docType == "CARTAPORTE":
			self.inputsParams = "cartaporte_input_parameters.json"
		elif self.docType == "MANIFIESTO":
			self.inputsParams = "manifiesto_input_parameters.json"
		elif self.docType == "DECLARACION":
			self.inputsParams = "declaracion_input_parameters.json"
		else:
			message= f"ERROR: Tipo de documento desconocido:", docType
			raise Exception (message)
		return self.inputsParams
	
#----------------------------------------------------------
# Remove invalid CODEBIN JSON files for cartaportes 
#----------------------------------------------------------
def cleanCodebinCartaportesFiles (inDir):
	files       = os.listdir (inDir)
	invalidDir  = f"{inDir}/invalid"
	os.system (f"mkdir {invalidDir}")
	pathFiles   = [f"{inDir}/{x}" for x in files if "invalid" not in x]
	for path in pathFiles:

		print ("-- path:", path)
		data = json.load (open (path))
		subjectFields = ["txt02", "txt03", "txt04", "txt05", "txt06", "txt07", "txt08", "txt19"]
		if any ([data [x]["value"].strip()=="" for x in subjectFields]):
			os.system (f"mv {path} {invalidDir}")

#----------------------------------------------------------------
# startCodebinBot
#----------------------------------------------------------------
def startCodebinBot (docType, codebinFieldsFile):
	botCodebin = CodebinBot (docType, codebinFieldsFile)
	botCodebin.transmitFileToCodebin (codebinFieldsFile)

#-----------------------------------------------------------
# Call to main
#-----------------------------------------------------------
if __name__ == "__main__":
	main()
