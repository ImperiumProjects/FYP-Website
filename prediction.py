import mysql.connector
from mysql.connector import errorcode

import time

config = {
	'user': 'scraper',
	'password': 'scraper',
	'host': '84.200.193.29',
	'database': 'historical'
}
def predict():
	try:
		cnx = mysql.connector.connect(**config)
		cursor = cnx.cursor()

		river_level = ("""SELECT level
							FROM two_point_data
							ORDER BY id
							DESC LIMIT 4
						""")
		cursor.execute(river_level)
		result = cursor.fetchall()
		first_river_level = str(result[0])[10:-4]
		second_river_level = str(result[1])[10:-4]
		first_old_river_level = str(result[2])[10:-4]
		second_old_river_level = str(result[3])[10:-4]

		tide_level = ("""SELECT level
							FROM tidal
							ORDER BY id
							DESC LIMIT 1
						""")
		cursor.execute(tide_level)
		result = cursor.fetchall()
		last_tide_level = str(result[0])[10:-4]

		weather_level = ("""SELECT degrees
								FROM weather
								ORDER BY id
								DESC LIMIT 1
							""")
		cursor.execute(weather_level)
		result = cursor.fetchall()
		last_weather_level = str(result[0])[10:-4]

		prediction = 0
		# if negative, river level falling
		# if postitive, river level rising
		river_status = ((float(first_river_level) + float(second_river_level)) / 2) - ((float(first_old_river_level) + float(second_old_river_level)) / 2)
		mean_river_level = ((float(first_river_level) + float(second_river_level)) / 2)

		if river_status <= 0:
			prediction = (((mean_river_level / 4) * 100) / 2)
		else:
			prediction = ((mean_river_level / 4) * 100)

		add_prediction = ("""INSERT INTO predictions
									(percentage, time)
									VALUES (%s, %s)
							""")
		data = (prediction, time.strftime('%Y-%m-%d %H:%M:%S'))
		cursor.execute(add_prediction, data)

		cnx.commit()

		cursor.close()
		cnx.close()

	except mysql.connector.Error as e:
	    try:
	        print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
	    except IndexError:
	        print ("MySQL Error: %s" % str(e))