import pymysql

import time

def predict():
	try:

		database = pymysql.connect(host="84.200.193.29",
                     user="scraper",
                     passwd="scraper",
                     db="historical")

		curs = database.cursor()

		error = None
		sql = "SELECT level FROM two_point_data ORDER BY id DESC LIMIT 4"
		curs.execute(sql)
		result = curs.fetchall()
		print(result)

		first_river_level = str(result[0])[10:-4]
		second_river_level = str(result[1])[10:-4]
		first_old_river_level = str(result[2])[10:-4]
		second_old_river_level = str(result[3])[10:-4]

		sql = "SELECT level FROM tidal ORDER BY id DESC LIMIT 1"
		curs.execute(sql)
		result = curs.fetchall()
		print(result)

		last_tide_level = str(result[0])[10:-4]

		sql = "SELECT degrees FROM weather ORDER BY id DESC LIMIT 1"
		curs.execute(sql)
		result = curs.fetchall()
		print(result)

		last_weather_level = str(result[0])[1:-2]

		prediction = 0
		# if negative, river level falling
		# if postitive, river level rising
		river_status = ((float(first_river_level) + float(second_river_level)) / 2) - ((float(first_old_river_level) + float(second_old_river_level)) / 2)
		mean_river_level = ((float(first_river_level) + float(second_river_level)) / 2)

		if river_status <= 0:
			prediction = (((mean_river_level / 4) * 100) / 2)
		else:
			prediction = ((mean_river_level / 4) * 100)

		sql = ("""INSERT INTO predictions
									(percentage, time)
									VALUES (%s, %s)
							""")
		data = (prediction, time.strftime('%Y-%m-%d %H:%M:%S'))

		print("----------------------------")
		print(first_river_level)
		print(second_river_level)
		print(first_old_river_level)
		print(second_old_river_level)
		print(last_tide_level)
		print(last_weather_level)
		print(prediction)
		curs.execute(sql, data)
		database.commit()
	finally:
		database.close()