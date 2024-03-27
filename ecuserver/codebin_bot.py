#!/usr/bin/env python3

"""
Fill documents into the CODEBIN site using as input an 
ECUAPASSDOCS pdf with their corresponding inputs parameters file
"""
import sys, json, re, time, os
import PyPDF2

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from ecuapassdocs.info.ecuapass_utils import Utils
from ecuapassdocs.info.resourceloader import ResourceLoader 

#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv

	codebinFieldsFile = args [1]   # PDF with Ecudoc fields
	mainCodebinBot (codebinFieldsFile)

#----------------------------------------------------------------
# mainCodebinBot
#----------------------------------------------------------------
def mainCodebinBot (docType, codebinFieldsFile):
	botCodebin = CodebinBot (docType, codebinFieldsFile)
	botCodebin.start ()

#----------------------------------------------------------------
# Bot for filling CODEBIN forms from ECUDOCS fields info
#----------------------------------------------------------------
class CodebinBot:
	def __init__ (self, docType, codebinFieldsFile):
		self.docType           = docType
		self.codebinFieldsFile = codebinFieldsFile
		self.driver            = None

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	def start (self):
		Utils.printx (">> Transmitiendo '{self.docType}' a codebin")
		codebinFields = json.load (open (self.codebinFieldsFile))
		pais = codebinFields.pop ("pais")
		Utils.printx ("-- pais:", pais)

		self.login (pais)
		if self.docType == "CARTAPORTE":
			frameDocumento = self.nuevaCartaporte ()
		elif self.docType == "MANIFIESTO":
			frameDocumento = self.nuevoManifiesto ()

		self.fillForm (frameDocumento, codebinFields)

	#-------------------------------------------------------------------
	#-------------------------------------------------------------------
	def login (self, pais):
		# Open and click on "Continuar" button
		driver = webdriver.Firefox ()
		driver.get ("https://byza.corebd.net")
		submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
		submit_button.click()

		# Open new window with login form, then switch to it
		time.sleep (2)
		winMenu = driver.window_handles [-1]
		driver.switch_to.window (winMenu)

		# Login Form : fill user / password
		loginForm = driver.find_element (By.TAG_NAME, "form")
		userInput = loginForm.find_element (By.NAME, "user")
		userInput.send_keys ("GRUPO BYZA")
		pswdInput = loginForm.find_element (By.NAME, "pass")
		pswdInput.send_keys ("GrupoByza2020*")

		# Login Form:  Select pais (Importación or Exportación : Colombia  or Ecuador)
		docSelectElement = driver.find_element (By.XPATH, "//select[@id='tipodoc']")
		docSelect = Select (docSelectElement)
		docSelect.select_by_value (pais)
		submit_button = loginForm.find_element (By.XPATH, "//input[@type='submit']")
		submit_button.click()

		self.driver = driver
		
	def nuevaCartaporte (self):
		try:
			driver = self.driver
			iniLink = driver.find_element (By.PARTIAL_LINK_TEXT, "Carta Porte")
			iniLink.click()

			iniLink = driver.find_element (By.XPATH, "//a[contains(@href, '1.cpi/nuevo.cpi.php?modo=1')]")
			iniLink.click()

			# Switch to the frame or window containing the <object> element
			object_frame = driver.find_element (By.TAG_NAME, "object")
			wait = WebDriverWait (driver, 2)  # Adjust the timeout as needed
			wait.until (EC.frame_to_be_available_and_switch_to_it (object_frame))

			#import time
			#time.sleep (3)
			#docForm = driver.find_element (By.TAG_NAME, "form")

			# Explicitly wait for the form to be located
			docForm = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.TAG_NAME, "form"))
			)

			return docForm
		except Exception as e:
			Utils.printx("No se pudo crear una nueva cartaporte en el CODEBIN")
			return None

	def nuevoManifiesto (self):
		driver = self.driver
		iniLink = driver.find_element (By.PARTIAL_LINK_TEXT, "Manifiesto de Carga")
		iniLink.click()

		iniLink = driver.find_element (By.XPATH, "//a[contains(@href, '2.mci/nuevo.mci.php?modo=1')]")
		iniLink.click()

		# Switch to the frame or window containing the <object> element
		object_frame = driver.find_element (By.TAG_NAME, "object")
		wait = WebDriverWait (driver, 2)  # Adjust the timeout as needed
		wait.until (EC.frame_to_be_available_and_switch_to_it (object_frame))

		docForm = driver.find_element (By.TAG_NAME, "form")

		return docForm
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

			# Radio button group
			elif MANIFIESTO and "radio" in field:
				elem = docForm.find_element (By.ID, field)
				self.driver.execute_script("arguments[0].click();", elem)

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
# Call to main
#-----------------------------------------------------------
if __name__ == "__main__":
	main()
