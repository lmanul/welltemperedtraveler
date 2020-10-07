USE_NEW_DATA_SOURCE = False

START_YEAR = 2010
START_DATE = str(START_YEAR) + "0101"
END_YEAR = 2019
END_DATE = str(END_YEAR) + "1231"
ALL_YEARS_STR = [str(y) for y in range(START_YEAR, END_YEAR + 1)]


DREMEL_TEMPLATE = (
'SELECT Date, Location, Min_C, Mean_C, Max_C, Rain, Snow '
#'SELECT Date, Location, Min_C, Mean_C, Max_C, Min_H, Mean_H, Max_H, Rain, Snow '
'FROM '
'  (SELECT date as Date, '
'    station_id as StationId, '
'    temp_c_min as Min_C, '
'    temp_c_mean as Mean_C, '
'    temp_c_max as Max_C, '
#'    humidity_pct_min as Min_H, '
#'    humidity_pct_mean as Mean_H, '
#'    humidity_pct_max as Max_H, '
'    rainfall_mm as Rain, '
'    snowfall_mm as Snow '
'  FROM '
'    weather.historical.daily' + ('.new.capacitor' if USE_NEW_DATA_SOURCE else '') + ' '
'  WHERE '
'    (date >= "%s") AND (date <= "%s") AND '
'    temp_c_max != -9999) AS W '
'JOIN '
'  (SELECT '
'    id as Id, '
'    CONCAT(geo.locality_name, ", ", geo.subdivision_1_name, ", ", geo.region_code) as Location '
'  FROM '
'    weather.stations' + ('.new.capacitor' if USE_NEW_DATA_SOURCE else '') + ' '
'  WHERE '
'    geo.locality_name = "%s" AND '
'    geo.region_code = "%s") AS S '
'ON W.StationId = S.Id '
'ORDER BY Date;')

def get_data_from_dremel(place, region_code):
    command = ["echo", "'" + (util.DREMEL_TEMPLATE % (util.START_DATE, util.END_DATE, place, region_code)) + "'"]
    echo_ps = subprocess.Popen(" ".join(command), stdout=subprocess.PIPE, universal_newlines=True, shell=True)
    output = subprocess.check_output([
        'dremel',
        "--min_completion_ratio=" + MIN_COMPLETION_RATIO,
        "--sql_dialect=GoogleSQL",
    ], stdin=echo_ps.stdout, universal_newlines=True)
    echo_ps.wait()
    return output
