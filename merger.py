import functions as fn
import sys

arg = sys.argv

# Extracting GSM number according to cell line and forme it in dictionary
smpl = fn.getCellLineGEO(arg[1])

# get data about each cell line
GEO_data, GEO_cell_name = fn.getGEOData(arg[1], smpl)
GEO_geneName = fn.getGeneName(arg[1])

# Extracting cell line names from Almanac data
# Compressing Almanac data by consentration
almanac_data, almanac_names = fn.getAlmanacData(arg[2])

# Compearing names from GEO and ALMANAC data sets
converter = fn.nameConverter(GEO_cell_name, almanac_names)

# merging data
merging_data = fn.mergingData(GEO_data,almanac_names, converter)

# write merging data
fn.writingData(merging_data, GEO_geneName)

