#!/usr/bin/env python3

VERSION="0.842"
"""
LOG: 
 - 0.842:Mayo10: Moified to work with CODEBIN web as a thread
"""

import os, sys, time
import signal

from threading import Thread as threading_Thread

# For open URLs
from selenium import webdriver

# For server
from flask import Flask as flask_Flask 
from flask import request as flask_request 
from werkzeug.serving import make_server

# doc, document bots
from ecuapass_doc import EcuDoc
from ecuapass_bot_cartaporte import mainBotCartaporte
from ecuapass_bot_manifiesto import mainBotManifiesto
from ecuapass_bot_declaracion import mainBotDeclaracion

# Codebin, Ecuapassdocs Bot
from bot_codebin import startCodebinBot, CodebinBot
from bot_ecuapassdocs import startEcuapassdocsBot
from ecuapass_bot import EcuBot

from ecuapassdocs.info.ecuapass_feedback import EcuFeedback
from ecuapassdocs.info.ecuapass_utils import Utils

# Define the maximum idle time in seconds before stopping the server
MAX_IDLE_TIME = 10  # Change this to your desired time

# Flag to track whether a request has been received
request_received = False

#sys.stdout.reconfigure(encoding='utf-8')

# Driver for web interaction
driver = None
def main ():
	args = sys.argv
	if len (args) > 1:
		if "--version" in args:
			print ("Version: ", VERSION)
		else:
			mainDoc (sys.argv [1], os.getcwd())
	else:
		EcuServer.run_server_forever()

def printx (*args, flush=True, end="\n"):
	print ("SERVER:", *args, flush=flush, end=end)
#-----------------------------------------------------------
# Ecuapass server: listen GUI messages and run processes
#-----------------------------------------------------------
app = flask_Flask (__name__)
class EcuServer:
	shouldStop = False
	server     = None
	runningDir = os.getcwd()

	def run_server_forever ():
		portNumber  = EcuServer.getPortNumber ()
		server = make_server('127.0.0.1', portNumber, app)

		# Start firefox webdriver
		CodebinBot.initCodebinWebdriver ()

		printx (f">>>>>>>>>>>>>>>> Server version: {VERSION} <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
		printx (f">>>>>>>>>>>>>>>> Server is running on port::{portNumber}::<<<<<<<<<<<<<<<<<<")
		server.serve_forever()
		#printx (f">>>>>>>>>>>>>>>> Server is running on port::{portNumber}::<<<<<<<<<<<<<<<<<<")

	#----------------------------------------------------------------
	# Listen for remote calls from Java GUI
	#----------------------------------------------------------------
	@app.route('/start_processing', methods=['GET', 'POST'])
	def start_processing ():
			printx ("-------------------- Iniciando Procesamiento -------------------------")
			# Update flag server
			global request_received
			request_received = True

			if EcuServer.shouldStop:
				return {'result': 'Servidor cerrándose...'}

			# Get the file name from the request
			service = flask_request.json ['service']
			data1   = flask_request.json ['data1']
			data2   = flask_request.json ['data2']

			printx ("Servicio  : ", service, flush=True)
			printx ("Dato 1    : ", data1, flush=True)
			printx ("Dato 2    : ", data2, flush=True)

			# Call your existing script's function to process the file
			result = None
			if (service == "doc_processing"):
				result = EcuServer.analizeOneDocument (docFilepath=data1, runningDir=data2)

			elif (service == "bot_processing"):
				result = EcuServer.botProcessing (jsonFilepath=data1, runningDir=data2)

			elif (service == "codebin_transmit"):
				result = EcuServer.codebin_transmit (workingDir=data1, codebinFieldsFile=data2)

			elif (service == "ecuapassdocs_transmit"):
				result = EcuServer.ecuapassdocs_transmit (workingDir=data1, ecuapassdocsFieldsFile=data2)

			elif (service == "open_ecuapassdocs_URL"):
				EcuServer.openEcuapassdocsURL (url=data1)

			elif (service == "stop"):
				EcuServer.stop_server ()

			elif (service == "send_feedback"):
				EcuFeedback.sendFeedback (zipFilepath=data1, docFilepath=data2)
				result = "true"

			elif (service == "is_running"):
				result = "true"

			else:
				result = f">>> Servicio '{service}' no disponible."

			printx (result)
			return {'result': result}

	#----------------------------------------------------------------
	# Stop server
	#----------------------------------------------------------------
	def stop_server ():
		printx ("Finalizando sesión de CODEBIN...")
		webdriver = EcuServer.CodebinBot.getWebdriver ()
		webdriver.quit ()
		printx ("...sesión CODEBIN finalizada")
		EcuServer.should_stop = True
		printx ("Finalizando servidor Ecuapass ...")
		sys.exit (0)

	#----------------------------------------------------------------
	#-- Concurrently process one document given its path
	#----------------------------------------------------------------
	def analizeOneDocument (docFilepath, runningDir):
		workingDir = os.path.dirname (docFilepath)

		# Check if PDF is a valid ECUAPASS document
		if not EcuServer.isValidDocument (docFilepath):
			return f"Tipo de documento '{docFilepath}' no válido"

		# Create and start threads for processing files
		os.chdir (workingDir)
		ecudoc = EcuDoc ()

		TARGET = ecudoc.extractDocumentFields
		ARGS   = (docFilepath, runningDir)
		threading_Thread (target=TARGET, args=ARGS).start ()

	#----------------------------------------------------------------
	# Open Ecuapassdocs URL in Chrome browser
	#----------------------------------------------------------------
	def openEcuapassdocsURL (url):
		import pyautogui as py

		windows = py.getAllWindows ()
		printx (">> Todas las ventanas:", [x.title for x in windows])
		for win in windows:
			if "EcuapassDocs" in win.title and "Google" in win.title:
				win.minimize()
				win.restore (); py.sleep (1)
				return

		global driver
		if driver:
			driver.quit ()
		print (">> Inicializando webdriver...")
		driver = webdriver.Chrome()
		driver.get (url)

		#printx (f">> Abriendo sitio web de EcuapassDocs: '{url}'")
		#driver.execute_script("window.open('" + url + "','_blank');")

#		# Check if the URL is already open in another window
#		url_open = False
#		printx (f">> Buscando una ventana abierta de EcuapassDocs : '{url}'")
#		for handle in driver.window_handles:
#			driver.switch_to.window (handle)
#			print (f">>>> Ventana : '{driver.current_url}'")
#			current_url = driver.current_url
#			if url == current_url:
#				url_open = True
#				break
#
#
#		# Optionally, switch to the last opened window
#		driver.switch_to.window(driver.window_handles[-1])
		
		
	#----------------------------------------------------------------
	#-- Execute bot according to the document type
	#-- Doctype is in the first prefix of the jsonFilepath
	#----------------------------------------------------------------
	def botProcessing (jsonFilepath, runningDir):
		docType = EcuServer.getDoctypeFromFilename (jsonFilepath)

		if docType == "CARTAPORTE":
			mainBotCartaporte (jsonFilepath, runningDir)
		elif docType == "MANIFIESTO":
			mainBotManifiesto (jsonFilepath, runningDir)
		elif docType == "DECLARACION":
			mainBotDeclaracion (jsonFilepath, runningDir)
		else:
			printx ("ERROR: Tipo de documento desconocido: '{filename}'")
			sys.exit (0)

	#----------------------------------------------------------------
	#-- Transmit document fields to CODEBIN web app using Selenium
	#----------------------------------------------------------------
	def codebin_transmit (workingDir, codebinFieldsFile):
		filepath = os.path.join (workingDir, codebinFieldsFile)
		docType = EcuServer.getDoctypeFromFilename (codebinFieldsFile)
		startCodebinBot (docType, filepath)

	#----------------------------------------------------------------
	#-- Transmit document fields to ECUAPASSDOCS web app using Selenium
	#----------------------------------------------------------------
	def ecuapassdocs_transmit (workingDir, ecuapassdocsFieldsFile):
		filepath = os.path.join (workingDir, ecuapassdocsFieldsFile)
		docType = EcuServer.getDoctypeFromFilename (ecuapassdocsFieldsFile)
		startEcuapassdocsBot (filepath)

	#----------------------------------------------------------------
	#-- Check if document filename is an image (.png) or a PDF file (.pdf)
	#----------------------------------------------------------------
	def isValidDocument (filename):
		extension = filename.split (".")[1]
		if extension.lower() in ["PDF", "pdf"]:
			return True
		return False

	#----------------------------------------------------------------
	#-- Get document type from filename
	#----------------------------------------------------------------
	def getDoctypeFromFilename (filename):
		docType = os.path.basename (filename).split("-")[0].upper()
		filename = filename.upper ()
		if "CPI" in filename or "CARTAPORTE" in filename:
			return ("CARTAPORTE")
		elif "MCI" in filename or "MANIFIESTO" in filename:
			return ("MANIFIESTO")
		elif "DCL" in filename or "DECLARACION" in filename:
			return ("DECLARACION")
		else:
			printx (f"ERROR: Tipo de documento desconocido: '{docType}'")
			sys.exit (1)

	#------------------------------------------------------
	# Get free port by adding 1 to the last open port
	#------------------------------------------------------
	def getPortNumber ():
		portFilename = "url_port.txt"
		portNumber = 5000
		
		# read old port
		if os.path.exists (portFilename):
			with open (portFilename, "r", encoding='utf-8') as portFile: 
				portString = portFile.readline ()
				portNumber = int (portString) + 1

		# write new port
		with open (portFilename, "w", encoding='utf-8') as portFile: 
			portFile.write ("%d" % portNumber)

		return (portNumber)


#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()
