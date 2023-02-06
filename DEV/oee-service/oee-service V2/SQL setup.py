# SQL setup
# sqlFilePath = script_dir + "//" + "Query" + ".sql"

# try:
# 	print("[INFO]" + "[Query file]" + "Opening...")
# 	sqlFile = open(sqlFilePath, 'r')
# 	print("[INFO]" + "[Query file]" + "Successful opened.")
# except Exception as e:
# 	print("[ERROR]" + "[Query file]" + "Opening failed:\n" + str(e) + "\n")

# sqlFileContent = sqlFile.read()
# sqlFile.close()
# sqlFile_rows = sqlFileContent.split("\n")

# sqlCommands = str()

# for row in sqlFile_rows:
# 	if row.find('-- ') == -1:
# 	# if not row.startswith('-- '):
# 	# if not row.startswith('-- ') or not row.find('-- '):

# 		row = row.replace("\t", "").replace("\n", "")

# 		if row.find("20 * 1000") != -1 : row = f"{idealTime} * 1000"
# 		elif row.find("5 minute") != -1 : row = f"'{timestep}'"
# 		elif row.find("2023-01-01T08:00:00Z") != -1 : row = f"'{startDateTime}'"
# 		elif row.find("'In Picking','In Welding','In QC','In Placing'") != -1 : row = timesUp
# 		elif row.find("'Idle','In Reworking','In QC from rework','In Trashing'") != -1 : row = timesDown
# 		elif row.find("In Placing") != -1 : row = endsGood
# 		elif row.find("In Trashing") != -1 : row = endsBad

# 		elif row.find("mtopcua_car") != -1 : row = row.replace("ocua_car", FIWARE_SERVICE.lower())
# 		elif row.find("etplc") != -1 : row = row.replace("plc", CONTEXTS_TYPE.lower())
 
# 		sqlCommands += str(row) + " "


# sqlCommands = sqlCommands.split(';')
# try:
# 	sqlCommands.remove(' ')
# except Exception as e:
# 	print("[WARNING]" + "[SQL Commands]" + ": " + str(e) + "\n")