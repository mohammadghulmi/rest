import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
		
@app.route('/addlock', methods=['POST'])
def add_lock():
	try:
		_json = request.json
		_name = _json['empName']
		_lockID = _json['lockID']
			
		if _name and _lockID and request.method == 'POST':			
			sqlQuery = "INSERT INTO locks(empName, lockID) VALUES(%s, %s)"
			bindData = (_name, _lockID)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			respone = jsonify('lock added successfully!')
			respone.status_code = 200
			return respone
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		print("e")

	#	cursor.close() 
		#conn.close()
		
@app.route('/lock')
def lock():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT  empName, lockID FROM locks")
		empRows = cursor.fetchall()
		respone = jsonify(empRows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		print("e")

	#	cursor.close() 
	#	conn.close()
		
@app.route('/lock/<string:name>')
def locks(name):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT lockID FROM locks WHERE empName =%s", name)
		empRow = cursor.fetchall()
		respone = jsonify(empRow)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		print("e")

		#cursor.close() 
		#conn.close()

@app.route('/update_lock', methods=['PUT'])
def update_lock():
	try:
		_json = request.json
		_name = _json['empName']
		_lockID = _json['lockID']
		
		# validate the received values
		if _name and _fingerID and _faceID and _RFID and request.method == 'PUT':			
			sqlQuery = "UPDATE locks SET empName=%s, lockID=%s WHERE lockID=%s"
			bindData = (_name, _lockID, _lockID)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			respone = jsonify('lock updated successfully!')
			respone.status_code = 200
			return respone
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		print("e")

		#cursor.close() 
		#conn.close()
		
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_emp(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM lock WHERE lockID =%s", (id))
		conn.commit()
		respone = jsonify('lock deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		print("e")
		#cursor.close() 
		#conn.close()
		
@app.errorhandler(404)
def not_found(error=None):
	message = {
		'status': 404,
		'message': 'Record not found: ' + request.url,
	}
	respone = jsonify(message)
	respone.status_code = 404
	return respone
		
if __name__ == "__main__":
	app.run()