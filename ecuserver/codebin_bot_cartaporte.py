#!/usr/bin/env python3

import sys

from codebin_bot_base import BotCodebinDoc
from ecuapassdocs.info.ecuapass_utils import Utils

#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv

	codebinFieldsFile = args [1]   # PDF with Ecudoc fields
	mainCodebinBotCartaporte (codebinFieldsFile)


#	# Get codebin fields
#	botCodebin          = BotCodebinCartaporte (ecudocPDFFieldsFile)
#	ecudocFields        = botCodebin.getEmbeddedFieldsFromPDF ()
#	codebinFields, pais = botCodebin.createCodebinFields (ecudocFields)
#
#	# Login to CODEBIN and fill form
#	botCodebin.login (pais)
#	frameCartaporte   = botCodebin.nuevaCartaporte ()
#	botCodebin.fillForm (frameCartaporte, codebinFields)

#----------------------------------------------------------------
# mainCodebinBotCartaporte
#----------------------------------------------------------------
def mainCodebinBotCartaporte (codebinFieldsFile ):
	botCodebin = BotCodebinCartaporte (codebinFieldsFile)
	botCodebin.start ()

#----------------------------------------------------------------
# Bot for filling CODEBIN cartaportes from ECUDOCS PDFs
#----------------------------------------------------------------
class BotCodebinCartaporte (BotCodebinDoc):
	def __init__ (self, codebinFieldsFile):
		super().__init__("CARTAPORTE", codebinFieldsFile)
#-----------------------------------------------------------
#-----------------------------------------------------------
#main ()
if __name__ == "__main__":
	main()
