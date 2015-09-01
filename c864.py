import os
#import re
import glob
#import time
from time import strftime
from collections import defaultdict
import collections
# or "import collections [module]" and call defaultdict by using collections.defaultdict(list)
from My import _lookupname
from My import _edielement

# 864 class definition
class c864:

	def __init__(self, fileName):
		# 864
		self.outLoc = "C:\\PerlScripts\\test\\out\\archive\\"
		self.fileName = fileName
		self.header864 = {}
		self.detail1_864 = defaultdict(list)
		self.detail2_864 = defaultdict(list)
		# 0 - Transaction ID, 1 - Corporation (incl N1, N3, and N4), 2 - Transaction Date
		# 3 - Transaction Type, 4 - REF, 5 - PER
		self.headerlist = ['blank','blank','blank','blank','blank','blank',]
		# 
		self.detail1list = defaultdict(list)
		# 0 - Msg Text, 1 - Print Ctrl, 2 - Msg Number
		self.detail2list = defaultdict(list)
	
	def ReadFile(self):
		with open(self.fileName) as fh:
			# for every line, store values into attributes
			for fLine in fh:
				# Rcord_Sequence = 00001 (header), 00002 (detail)
				if (fLine[35:40] == '00001'):
					# Need all 15 characters for Translator_Id (no strip)
					self.header864['Translator_Id'] = fLine[0:15]
					self.header864['Transaction_Id'] = fLine[20:30].rstrip()
					self.header864['BMG_TS_Purpose_Code'] = fLine[53:55].rstrip()
					self.header864['BMG_TS_Type_Code'] = fLine[55:57].rstrip()
					self.header864['DTM_Qualifier'] = fLine[57:60].rstrip()
					self.header864['DTM_Date'] = fLine[60:68].rstrip()
					self.header864['N1_Entity_Id_Code'] = fLine[68:71].rstrip()
					self.header864['N1_Name'] = fLine[71:101].rstrip()
					self.header864['N1_Id_Qualifier'] = fLine[101:103].rstrip()
					self.header864['N1_Id_Code'] = fLine[103:133].rstrip()
					self.header864['N3_Address_1'] = fLine[133:163].rstrip()
					self.header864['N3_Address_2'] = fLine[163:193].rstrip()
					self.header864['N4_City'] = fLine[193:213].rstrip()
					self.header864['N4_State'] = fLine[213:215].rstrip()
					self.header864['N4_Postal_Code'] = fLine[215:225].rstrip()
					self.header864['N4_Country'] = fLine[225:230].rstrip()
					self.header864['REF_Id_Qualifier'] = fLine[230:233].rstrip()
					self.header864['REF_Id'] = fLine[233:253].rstrip()
					self.header864['PER_Contact_Function_Code'] = fLine[253:255].rstrip()
					self.header864['PER_Name'] = fLine[255:285].rstrip()
					self.header864['PER_Phone'] = fLine[285:305].rstrip()
					self.header864['PER_Fax'] = fLine[305:325].rstrip()
					self.header864['PER_Email'] = fLine[325:365].rstrip()
				elif (fLine[35:40] == '00002'):
					# Loop2_Sequence = 9xxxx (detail2), else (detail1)
					#print ("Loop2 Seq = ", fLine[48:50]) # debug
					if (fLine[48:50] != '90'):
						self.detail1_864['MIT_Reference_Id'].append(fLine[53:103].rstrip())
						self.detail1_864['N1_Entity_Id_Code'].append(fLine[103:106].rstrip())
						self.detail1_864['N1_Name'].append(fLine[106:136].rstrip())
						self.detail1_864['N1_Id_Qualifier'].append(fLine[136:138].rstrip())
						self.detail1_864['N1_Id_Code'].append(fLine[138:168].rstrip())
						self.detail1_864['N3_Address_1'].append(fLine[168:198].rstrip())
						self.detail1_864['N3_Address_2'].append(fLine[198:228].rstrip())
						self.detail1_864['N4_City'].append(fLine[228:248].rstrip())
						self.detail1_864['N4_State'].append(fLine[248:250].rstrip())
						self.detail1_864['N4_Postal_Code'].append(fLine[250:260].rstrip())
						self.detail1_864['N4_Country'].append(fLine[260:265].rstrip())
						self.detail1_864['REF_Id_Qualifier_1'].append(fLine[265:268].rstrip())
						self.detail1_864['REF_Id_1'].append(fLine[268:288].rstrip())
						self.detail1_864['REF_Id_Qualifier_2'].append(fLine[288:291].rstrip())
						self.detail1_864['REF_Id_2'].append(fLine[291:311].rstrip())
						self.detail1_864['REF_Id_Qualifier_3'].append(fLine[311:314].rstrip())
						self.detail1_864['REF_Id_3'].append(fLine[314:334].rstrip())
						self.detail1_864['PER_Contact_Function_Code'].append(fLine[334:336].rstrip())
						self.detail1_864['PER_Name'].append(fLine[336:366].rstrip())
						self.detail1_864['PER_Phone'].append(fLine[366:386].rstrip())
						self.detail1_864['PER_Fax'].append(fLine[386:406].rstrip())
						self.detail1_864['PER_Email'].append(fLine[406:446].rstrip())
					else:
						self.detail2_864['MSG_Message_Text'].append(fLine[53:185].rstrip())
						self.detail2_864['MSG_Print_Control'].append(fLine[185:188].rstrip())
						self.detail2_864['MSG_Number'].append(fLine[188:218].rstrip())
				else:
					print ("Unknown Rcord_Sequence", fLine[35:40])
			
			fh.close()

	def BMGTransId(self):
		if (self.header864['Transaction_Id'] != ''):
			self.headerlist[0] = "Transaction ID:			" + self.header864['Transaction_Id'] + "\n"
	
	def BMGCorp(self):
		if (self.header864['N1_Name'] != ''):
			self.headerlist[1] = "Corporation:			" + self.header864['N1_Name'] + "\n"
		if (self.header864['N3_Address_1'] != ''):
			x = self.headerlist[1] + self.header864['N3_Address_1'] + "\n"
			self.headerlist[1] = x
		if (self.header864['N3_Address_2'] != ''):
			x = self.headerlist[1] + self.header864['N3_Address_2'] + "\n"
			self.headerlist[1] = x
		if (self.header864['N4_City'] != ''):
			x = self.headerlist[1] + self.header864['N4_City'] + "\n"
			self.headerlist[1] = x
		if (self.header864['N4_State'] != ''):
			x = self.headerlist[1] + self.header864['N4_State'] + "\n"
			self.headerlist[1] = x
		if (self.header864['N4_Postal_Code'] != ''):
			x = self.headerlist[1] + self.header864['N4_Postal_Code'] + "\n"
			self.headerlist[1] = x
		if (self.header864['N4_Country'] != ''):
			x = self.headerlist[1] + self.header864['N4_Country'] + "\n"
			self.headerlist[1] = x
	
	def BMGDTM(self):
		if (self.header864['DTM_Qualifier'] != ''):
			self.headerlist[2] = _edielement.Lookup374(self.header864['DTM_Qualifier'])
			x = self.headerlist[2] + "\n" + self.header864['DTM_Date']
			self.headerlist[2] = x + "\n"
	
	def BMGXaction(self):
		if (self.header864['BMG_TS_Purpose_Code'] != ''):
			self.headerlist[3] = "Transaction Purpose Code:	" + \
			_edielement.Lookup353(self.header864['BMG_TS_Purpose_Code']) + "\n"
		if (self.header864['BMG_TS_Type_Code'] != ''):
			self.headerlist[3] = "Transaction Type:		" + \
			_edielement.Lookup640(self.header864['BMG_TS_Type_Code']) + "\n"
	
	def BMGREF(self):
		if (self.header864['REF_Id_Qualifier'] != ''):
			self.headerlist[4] = _edielement.Lookup128(self.header864['REF_Id_Qualifier']) \
			+ self.header864['REF_Id'] + "\n"
	
	def BMGPER(self):
		tab = '	'
		if (self.header864['PER_Contact_Function_Code'] != ''):
			self.headerlist[5] = _edielement.Lookup366(self.header864['PER_Contact_Function_Code']) + "\n"
		if (self.header864['PER_Name'] != ''):
			x = self.headerlist[5] + tab + "Name: " + self.header864['PER_Name'] + "\n"
			self.headerlist[5] = x
		if (self.header864['PER_Phone'] != ''):
			x = self.headerlist[5] + tab + "Phone: " + self.header864['PER_Phone'] + "\n"
			self.headerlist[5] = x
		if (self.header864['PER_Fax'] != ''):
			x = self.headerlist[5] + tab + "Fax: " + self.header864['PER_Fax'] + "\n"
			self.headerlist[5] = x
		if (self.header864['PER_Email'] != ''):
			x = self.headerlist[5] + tab + "Email: " + self.header864['PER_Email'] + "\n"
			self.headerlist[5] = x

	
	def WriteReport(self):
		# Create Output file
		fName = os.path.basename(self.fileName)
		#print ("filename = " + fName)		# debug
		
		# Output file name
		fNameLen = len(fName)
		fName = fName[:fNameLen-4] + "_report.txt"

		#print ("filename = " + fName)		# debug
		
		fOutH = open(fName, 'w')
		
		# 864 Report Title
		print ("864 Message Report		Date: " + strftime("%b %d, %Y") + "\n\n")
		fOutH.write("864 Message Report		Date: " + strftime("%b %d, %Y") + "\n\n")
		
		# 864 Header
		for k in self.header864:
			if(self.header864[k] != ''):
				# NOTE: if(!self.header864[k]) fails with invalid syntax
				print(k + ': ' + self.header864[k])		# debug
#				switcher = {
#					"Transaction_Id": self.BMGTransId(),
#					"N1_Name": self.BMGCorp(),
#					"DTM_Qualifier": self.BMGDTM(),
#					"BMG_TS_Purpose_Code": self.BMGXaction(),
#					"REF_Id_Qualifier": self.BMGREF(),
#					"PER_Contact_Function_Code": self.BMGPER(),
#				}
#				switcher.get(k, 'none')
				# use if/elif/else as switcher somehow is not working properly
				if(k == 'Transaction_Id'):
					self.BMGTransId()
				elif(k == 'N1_Name'):
					self.BMGCorp()
				elif(k == 'DTM_Qualifier'):
					self.BMGDTM()
				elif(k == 'BMG_TS_Purpose_Code'):
					self.BMGXaction()
				elif(k == 'REF_Id_Qualifier'):
					self.BMGREF()
				elif(k == 'PER_Contact_Function_Code'):
					self.BMGPER()
				
		if(self.headerlist[1] == 'blank'):
			self.headerlist[1] = "Corporation:			" + \
			_lookupname.LookupTPName(self.header864['Translator_Id']) + "\n"
		
		for l in self.headerlist:
			if(l != 'blank'):
				print (l)
				fOutH.write(l)
		
		print ("\n")
		fOutH.write("\n")
		
		# 864 Detail1
		
		
		# 864 Detail2		
		# length of list in self.detail2_864 defaultdict
		msg_len = len(self.detail2_864['MSG_Message_Text'])
			
		# k is the key for output defaultdict
		for k in range(0,msg_len):
			# l is the key for self.detail2_864 defaultdict
			for l in self.detail2_864:
				print(str(l) + " and " + str(k))
				if((self.detail2_864[l])[k] != ''):
					print ((self.detail2_864[l])[k])
					self.detail2list[k].append((self.detail2_864[l])[k] + "\n")

		for k in range(0,msg_len):
			for l in self.detail2list[k]:
				print (l)
				fOutH.write(l)
		
		
#		print(self.header864.items())			# debug
#		print(self.detail1_864.items())			# debug
#		print(self.detail2_864.items())			# debug

		fOutH.close()

# main program
# execute directly, i.e. c:>python blahblah.ph, will yield __name__ = __main__
# import into another file, i.e. import blahblah.ph, will yield __name__ = blahblah and the code
#   below will not execute (this is for testing class c864 on another python script)

if __name__ == "__main__":

	# NOTE: double backslashes are REQUIRED!!!
	ffLoc = "C:\\PerlScripts\\test\\out\\THER_864_*.txt"		# NOTE: change this for other directory
	# glob [module] - glob(ffLoc) [method]
	fList = glob.glob(ffLoc)

	print (fList)	# debug

	for l in fList:
	#	print (l)	# debug
		x = c864(l)
		x.ReadFile()
		x.WriteReport()
		del x

