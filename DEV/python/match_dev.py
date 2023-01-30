row = "'Idle','In Reworking','In QC from rework','In Trashing'"

idealTime = timestep = startDateTime = endsGood = endsBad = timesUp = timesDown = "Qualsiasi cosa"

match row:
	case "20 * 1000": row = idealTime + "* 1000"
	case "5 minute": row = timestep
	case "2023-01-01T08:00:00Z": row = startDateTime
	case "In Placing": row = endsGood
	case "In Trashing": row = endsBad
	case "'In Picking','In Welding','In QC','In Placing'": row = timesUp
	case "'Idle','In Reworking','In QC from rework','In Trashing'": row = timesDown

print(row)