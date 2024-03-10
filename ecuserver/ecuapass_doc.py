#!/usr/bin/env python3

import os, sys, json, re
import PyPDF2

# For doc
from pickle import load as pickle_load
from pickle import dump as pickle_dump
from traceback import format_exc as traceback_format_exc

# For Azure
import azure.core.credentials 
from azure.ai.formrecognizer import DocumentAnalysisClient

from ecuapassdocs.info.ecuapass_data import EcuData
from ecuapassdocs.info.ecuapass_info_cartaporte_BYZA import CartaporteByza
from ecuapassdocs.info.ecuapass_info_cartaporte_BOTERO import CartaporteBotero
from ecuapassdocs.info.ecuapass_info_cartaporte_NTA import CartaporteNTA
from ecuapassdocs.info.ecuapass_info_cartaporte_SYTSA import CartaporteSytsa
from ecuapassdocs.info.ecuapass_info_manifiesto_BYZA import ManifiestoByza
from ecuapassdocs.info.ecuapass_info_manifiesto_BOTERO import ManifiestoBotero
from ecuapassdocs.info.ecuapass_info_manifiesto_NTA import ManifiestoNTA
from ecuapassdocs.info.ecuapass_info_manifiesto_SYTSA import ManifiestoSytsa
from ecuapassdocs.info.ecuapass_info_declaracion import Declaracion

from ecuapassdocs.utils.ecuapass_feedback import EcuFeedback
from ecuapassdocs.utils.ecuapass_utils import Utils


"""
Remember to remove the key from your code when you're done, and never
post it publicly. For production, use secure methods to store and 
access your credentials. For more information, see https://docs.
microsoft.com/en-us/azure/cognitive-services/cognitive-services-
security?tabs=command-line%2Ccsharp#environment-variables-and-
application-configuration
"""
USAGE="\n\
Extract info from PDF ECUAPASS document (cartaporte|manifiesto|declaracion).\n\
USAGE: ecuapass_doc.py <PDF document>\n"

def main ():
	if (len (sys.argv) < 2):
		print (USAGE)
	else:
		docFilepath = sys.argv [1]
		mainDoc (docFilepath, os.getcwd())

def printx (*args, flush=True, end="\n"):
	print ("SERVER:", *args, flush=flush, end=end)

#----------------------------------------------------------
# Run Azure analysis for custom document
#----------------------------------------------------------
def mainDoc (inputFilepath, runningDir):
	fieldsJsonFile = None
	ecuFieldsFile  = None
	docFieldsFile  = None
	try:
		# Load "empresa": reads and checks if "settings.txt" file exists
		empresaName = getNombreEmpresaFromSettings (runningDir)

		# Start document processing
		filename         = os.path.basename (inputFilepath)
		documentType     = getDocumentTypeFromFilename (filename)
		fieldsJsonFile   = EcuDoc.processDocument (inputFilepath, documentType, empresaName)

		#EcuFeedback.sendLog (f"LOG_{empresaName}_{filename}")

		# Get from document Ecuapass and document fields
		ecuFields, docFields  = getDocumentFields (documentType, empresaName, fieldsJsonFile, runningDir)
		ecuFieldsFile         = EcuDoc.saveFields (ecuFields, filename, "ECUFIELDS")
		docFieldsFile         = EcuDoc.saveFields (docFields, filename, "DOCFIELDS")
		printx (f"Análisis exitoso del documento: '{inputFilepath}'")
	except Exception as ex:
		printx (traceback_format_exc())
		printx (f"FEEDBACK: '{inputFilepath}'")

	return ecuFieldsFile, docFieldsFile

#-----------------------------------------------------------
#-----------------------------------------------------------
def getNombreEmpresaFromSettings (runningDir):
	settingsPath  = os.path.join (runningDir, "settings.txt")
	if os.path.exists (settingsPath) == False:
		printx (f"El archivo de configuración '{settingsPath}' no existe")
		sys.exit (-1)

	settings     = json.load (open (settingsPath, encoding="utf-8")) 
	empresaName  = settings ["empresa"]
	print (">>> Empresa actual: ", empresaName)
	return empresaName

#-----------------------------------------------------------
#-- Get document according to documentType and empresaName
#-----------------------------------------------------------
def getDocumentFields (documentType, empresaName, fieldsJsonFile, runningDir):
	documento = None
	if documentType.upper() == "CARTAPORTE":
		if "BYZA" in empresaName:
			documento  = CartaporteByza (fieldsJsonFile, runningDir)
		elif "BOTERO" in empresaName:
			documento  = CartaporteBotero (fieldsJsonFile, runningDir)
		elif "NTA" in empresaName:
			documento  = CartaporteNTA (fieldsJsonFile, runningDir)
		elif "SYTSA" in empresaName:
			documento  = CartaporteSytsa (fieldsJsonFile, runningDir)
	elif documentType.upper() == "MANIFIESTO":
		if "BYZA" in empresaName:
			documento = ManifiestoByza (fieldsJsonFile, runningDir)
		elif "BOTERO" in empresaName:
			documento = ManifiestoBotero (fieldsJsonFile, runningDir)
		elif "NTA" in empresaName:
			documento = ManifiestoNTA (fieldsJsonFile, runningDir)
		elif "SYTSA" in empresaName:
			documento = ManifiestoSytsa (fieldsJsonFile, runningDir)
	elif documentType.upper() == "DECLARACION":
		print ("ALERTA: Aún no implmentada la obtencion de campos para DECLARACION")
		sys.exit (0)
	else:
		printx (f"FEEDBACK: '{inputFilepath}'")
		raise Exception (f"Tipo de documento '{documentType}' desconocido")

	ecuFields = documento.getMainFields ()
	docFields = documento.getDocFields ()
	return ecuFields, docFields

#-----------------------------------------------------------
#-- Get type of document from filename (e.g CPI-XXX.pdf or CARTAPORTE-XXX.pdf 
#-----------------------------------------------------------
def getDocumentTypeFromFilename (filepath):
	filename = os.path.basename (filepath).upper()
	if "CARTAPORTE" in filename or "CPI" in filename:
		return "CARTAPORTE"
	elif "MANIFIESTO" in filename or "MCI" in filename:
		return "MANIFIESTO"
	elif "DECLARACION" in filename or "DCL" in filename:
		return "DECLARACION"
	else:
		print (f"Tipo de documento desconocido en archivo: '{filename}'")
	return None
	
#-----------------------------------------------------------
# Run cloud analysis
#-----------------------------------------------------------
class EcuDoc:
	def processDocument (inputFilepath, documentType, empresaName):
		try:
			# CACHE: Check cache document
			fieldsJsonFile = EcuDoc.loadDocumentCache (inputFilepath)
			if fieldsJsonFile:
				return fieldsJsonFile
			else: 
				# EMBEDDED: Check embedded fields
				fieldsJsonFile = EcuDoc.getEmbeddedFieldsFromPDF (inputFilepath)
				if fieldsJsonFile:
					return fieldsJsonFile
				else:
					# CLOUD: Analyzing the document using the cloud
					fieldsJsonFile = EcuAzure.analyzeDocument (inputFilepath, documentType, empresaName)
					if fieldsJsonFile:
						return fieldsJsonFile
					else:
						printx ("Error: No se encontró ni pudo procesar el documento")
						return None

		except Exception as ex:
			printx (f"ERROR: iniciando proceso de documento'") 
			raise

	#----------------------------------------------------------------
	#-- Load previous result
	#----------------------------------------------------------------
	def loadDocumentCache (inputFilepath):
		print (">>> Buscando resultados previos...")
		fieldsJsonFile = None
		try:
			#filename       = os.path.basename (inputFilepath)
			filename       = inputFilepath
			pickleFilename = f"{filename.split ('.')[0]}-{EcuAzure.getCloudName()}-CACHE.pkl"
			print (">>> Buscando archivo cache : ", pickleFilename)
			if os.path.isfile (pickleFilename): 
				printx ("Cargando campos desde cache del documento...")
				with open (pickleFilename, 'rb') as inFile:
					result = pickle_load (inFile)
				fieldsJsonFile = EcuAzure.saveResults (result, filename)
		except:
			print (f"ERROR cargando documento desde cache: '{filename}'")
			raise

		return (fieldsJsonFile)
	
	#----------------------------------------------------------------
	#-- Get embedded fields info from PDF
	#----------------------------------------------------------------
	def getEmbeddedFieldsFromPDF (pdfPath):
		fieldsJsonPath = pdfPath.replace (".pdf", "-FIELDS.json")
		try:
			with open(pdfPath, 'rb') as pdf_file:
				pdf_reader = PyPDF2.PdfReader(pdf_file)

				# Assuming the hidden form field is added to the first page
				first_page = pdf_reader.pages[0]

				# Extract the hidden form field value 
				text     = first_page.extract_text()  
				jsonText = re.search ("Embedded_jsonData: ({.*})", text).group(1)
				printx ("Obteniendo campos desde el archivo PDF...")
				fieldsJsonDic  = json.loads (jsonText)
				json.dump (fieldsJsonDic, open (fieldsJsonPath, "w"), indent=4, sort_keys=True)
		except Exception as e:
			Utils.logException (e, "No se pudo leer campos embebidos en el documento PDF.")
			return None

		return (fieldsJsonPath)


	#-- Save fields dict in JSON 
	def saveFields (fieldsDict, filename, suffixName):
		prefixName	= filename.split(".")[0]
		outFilename = f"{prefixName}-{suffixName}.json"
		with open (outFilename, "w") as fp:
			json.dump (fieldsDict, fp, indent=4, default=str, sort_keys=True)

		return outFilename

#-----------------------------------------------------------
# Custom document built with the Azure Form Recognizer 
#-----------------------------------------------------------
class EcuAzure:
	AzureKeyCredential = azure.core.credentials.AzureKeyCredential

	#-----------------------------------------------------------------
	#-- Online processing. Return the first document, save resuts
	#-----------------------------------------------------------------
	def analyzeDocument (docFilepath, documentType, empresaName):
		docJsonFile = None
		try:
			credentialsDict  = EcuAzure.initCredentials (documentType, empresaName)
			lgEndpoint		 = credentialsDict ["endpoint"]
			lgKey			 = credentialsDict ["key"]	
			lgLocale		 = credentialsDict ["locale"]
			lgModel			 = credentialsDict ["modelId"]

			lgCredential = EcuAzure.AzureKeyCredential (lgKey)
			docClient	 = DocumentAnalysisClient (endpoint = lgEndpoint, 
												   credential = lgCredential)
			# Read the file into memory
			with open(docFilepath, "rb") as fp:
				poller = docClient.begin_analyze_document (lgModel, document=fp, locale=lgLocale)

			print ("\t>>>", "Polling result....")
			result	  = poller.result()
			document  = result.documents [0]
			docDict   = document.to_dict ()
			fields    = docDict ["fields"]
		

			# Save original result as pickled and json files
			print ("\t>>>", "Saving result....")
			docFilename = os.path.basename (docFilepath)
			fieldsJsonFile = EcuAzure.saveResults (result, docFilename)
		except Exception as ex:
			printx (ex.args [0])
			printx (f"ALERTA: Problemas analizando documento: '{docFilepath}'" )
			raise
			
		return (fieldsJsonFile)

	#-----------------------------------------------------------
	# Call the model according to prefix filename:"CARTAPORTE|MANIFIESTO|DECLARACION"
	#-----------------------------------------------------------
	def initCredentials (documentType, empresaName):
		keys = { "key1": "f18ce9601aaa4196926d846957d7f70a",
			     "endpoint": "https://lgtestfr.cognitiveservices.azure.com/"
			   }

		try:
			print ("\t>>> Leyendo credenciales...")
			credentialsDict = {}
			credentialsDict ["endpoint"] = keys ["endpoint"]
			credentialsDict ["key"]		 = keys ["key1"]
			credentialsDict ["locale"]	 = "es-CO"

			empresa = EcuData.getEmpresaInfo (empresaName)
			print ("\t>>> Empresa actual: ", empresa ["nombre"])
			if (documentType in "CARTAPORTE"):
				credentialsDict ["modelId"]  = empresa ["modelCartaportes"]
			elif (documentType in "MANIFIESTO"):
				print ("\t>>> Modelo actual: ", empresa ["modelManifiestos"])
				credentialsDict ["modelId"]  = empresa ["modelManifiestos"]
			elif (documentType in "DECLARACION"):
				credentialsDict ["modelId"]  = empresa ["modelDeclaraciones"]
			else:
				raise Exception (f"ALERTA:Tipo de documento '{documentType}' desconocido")
		except Exception as ex:
			printx ("ERROR: Problemas inicializando credenciales.")
			raise

		return (credentialsDict)

	#-- Save request result as pickle and json files
	#-- Return output filename for json fields 
	def saveResults (result, docFilepath):
		rootName = docFilepath.split ('.')[0]

		# Save results as Pickle 
		outPickleFile = f"{rootName}-{EcuAzure.getCloudName()}-CACHE" ".pkl"
		with open(outPickleFile, 'wb') as outFile:
			pickle_dump (result, outFile)

		# Save results as JSON file
		resultDict		= result.to_dict ()
#		outJsonFile = f"{rootName}-{EcuAzure.getCloudName()}-CACHE" ".json"
#		with open (outJsonFile, 'w') as outFile:
#			json.dump (resultDict, outFile, indent=4, default=str, sort_keys=True)

#		# Save result document as JSON file
#		document	 = result.documents [0]
#		documentDict = document.to_dict ()
#		outJsonFile = f"{rootName}-DOCUMENT-NONEWLINES" ".json"
#		with open (outJsonFile, 'w') as outFile:
#			json.dump (documentDict, outFile, indent=4, default=str, sort_keys=True)
#
#		# Save document with original (newlines) content
		documentDictNewlines = EcuAzure.getDocumentWithNewlines (resultDict)
		docJsonNewlinesFile = f"{rootName}-DOCUMENT" ".json"
#		with open (docJsonNewlinesFile, 'w') as outFile:
#			json.dump (documentDictNewlines, outFile, indent=4, default=str, sort_keys=True)
#
		# Save fields document as JSON file
		fields	 = documentDictNewlines ["fields"]
		#dicPais  =  {"00_Pais": EcuAzure.getWorkingCountry()}
		#fiedlds  = fields.update (dicPais)
		fieldsJsonFile = f"{rootName}-FIELDS" ".json"
		with open (fieldsJsonFile, 'w') as outFile:
			json.dump (fields, outFile, indent=4, default=str, sort_keys=True)

		return (fieldsJsonFile)

	def getCloudName ():
		return "azure"


	#-- Add newlines to document content 
	def getDocumentWithNewlines (resultsDict):
		#-- Determine whether two floating-point numbers are close in value.
		def isClose(a, b, rel_tol=1e-09, abs_tol=0.0):
			if abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol):
				return True
			return False

		def areClose(float1, float2, tolerance=1e-1):
			return abs(float1 - float2) < tolerance	

		#-- Check if the line is whithin the field box dimensions --
		def isContained (line, field):
			lineContent = line ["content"]
			xl = line ["polygon"][0]["x"]
			yl = line ["polygon"][0]["y"]
			#print ("\t\t> Coords line:", xl, yl)

			fieldContent = field ["content"]
			if (fieldContent == None):
				return False

			xf1   = field ["bounding_regions"][0]["polygon"][0]["x"]
			yf1   = field ["bounding_regions"][0]["polygon"][0]["y"]
			yf2   = field ["bounding_regions"][0]["polygon"][2]["y"]
			#print ("\t\t> Coords field", xf1, yf1, yf2)

			if (lineContent in fieldContent and areClose (xl, xf1) and 
				(areClose (yl, yf1) or yl >= yf1 and yl <= yf2)):
				return True

			return False
		#--------------------------------------------------------------

		lines  = resultsDict ["pages"][0]["lines"]
		fields = resultsDict ["documents"][0]["fields"]
		#fields = {"29_Mercancia_Descripcion": resultsDict ["documents"][0]["fields"]["29_Mercancia_Descripcion"]}

		for line in lines:
			lineContent = line ["content"]
			#print (">>> lineContent:", lineContent)
			#print (">", lineContent)
			for key in fields:
				field = fields [key]
				fieldContent = field ["content"]
				#print ("\t>", fieldContent)

				if isContained (line, field):
					#print (">>> CONTAINED")
					newlineContent = fieldContent.replace (lineContent+" ", lineContent+"\n")
					fields [key] ["content"] = newlineContent
					break

			resultsDict ["documents"][0]["fields"] = fields

		return (resultsDict ["documents"][0])

#	#--------------------------------------------------------------------
#	# Deprecated: Non needed.Get document with lines within fields regions
#	#--------------------------------------------------------------------
#	def getDocumentLinesRegions (resultDict):
#		lines  = resultDict ["pages"][0]["lines"]
#		fields = resultDict ["documents"][0]["fields"]
#
#		for key in fields:
#			#print (">>> Key:", key)
#			field        = fields [key]
#			fieldBox     = []
#			bounding_regions  = field ["bounding_regions"]
#			#print (">>> bounding_regions: ", bounding_regions)
#			if len (bounding_regions) > 0:
#				polygon = bounding_regions [0]["polygon"]
#				for i in range (len(polygon)):
#					fieldBox.append (polygon [i]["x"])
#					fieldBox.append (polygon [i]["y"])
#
#			fields [key]["box"] = fieldBox
#
##			for line in lines:
#				lineContent = line ["content"]
#				if isContained (line, field):
#
#		return fields


#		for line in lines:
#			lineContent = line ["content"]
#			#print (">", lineContent)
#			for key in fields:
#				field = fields [key]
#				fieldContent = field ["content"]
#				#print ("\t>", fieldContent)
#
#				if isContained (line, field):
#					newlineContent = fieldContent.replace (lineContent+" ", lineContent+"\n")
#					fields [key] ["content"] = newlineContent
#					break
#
#			resultsDict ["documents"][0]["fields"] = fields
#
#		return (resultsDict ["documents"][0])

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()
