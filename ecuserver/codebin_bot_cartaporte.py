#!/usr/bin/env python3

import sys

from codebin_bot_base import BotCodebinDoc
from ecuapassdocs.info.ecuapass_utils import Utils

#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv

	ecudocPDFFieldsFile = args [1]   # PDF with Ecudoc fields

	# Get codebin fields
	botCodebin          = BotCodebinCartaporte (ecudocPDFFieldsFile)
	ecudocFields        = botCodebin.getEmbeddedFieldsFromPDF ()
	codebinFields, pais = botCodebin.createCodebinFields (ecudocFields)

	# Login to CODEBIN and fill form
	botCodebin.login (pais)
	frameCartaporte   = botCodebin.nuevaCartaporte ()
	botCodebin.fillForm (frameCartaporte, codebinFields)

#----------------------------------------------------------------
# mainCodebinBotCartaporte
#----------------------------------------------------------------
def mainCodebinBotCartaporte (codebinFieldsFile, runningDir):
	botCodebin = BotCodebinCartaporte (codebinFieldsFile, runningDir)
	botCodebin.start ()

#----------------------------------------------------------------
# Bot for filling CODEBIN cartaportes from ECUDOCS PDFs
#----------------------------------------------------------------
class BotCodebinCartaporte (BotCodebinDoc):
	def __init__ (self, codebinFieldsFile, runningDir):
		super().__init__("CARTAPORTE", "cartaporte_input_parameters.json", 
		                  codebinFieldsFile, runningDir)
#-----------------------------------------------------------
#-----------------------------------------------------------
#main ()
