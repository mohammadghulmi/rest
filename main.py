import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
		
@app.route('/add', methods=['POST'])
def add_emp():
	try:
		_json = request.json
		_name = _json['name']
		_fingerID = _json['fingerID']
		_faceID = _json['faceID']
		_RFID = _json['RFID']		
		if _name and _fingerID and _faceID and _RFID and request.method == 'POST':			
			sqlQuery = "INSERT INTO employees(name, fingerID, faceID, RFID) VALUES(%s, %s, %s, %s)"
			bindData = (_name, _fingerID, _faceID, _RFID)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			respone = jsonify('Employee added successfully!')
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
		
@app.route('/emp')
def emp():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT  name, fingerID, faceID, RFID FROM employees")
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
		
@app.route('/emp/<int:id>')
def emps(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT name, fingerID, faceID, RFID FROM employees WHERE RFID =%s", id)
		empRow = cursor.fetchone()
		respone = jsonify(empRow)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		print("e")

		#cursor.close() 
		#conn.close()

@app.route('/update', methods=['PUT'])
def update_emp():
	try:
		_json = request.json
		_name = _json['name']
		_fingerID = _json['fingerID']
		_faceID = _json['faceID']
		_RFID = _json['RFID']		
		# validate the received values
		if _name and _fingerID and _faceID and _RFID and request.method == 'PUT':			
			sqlQuery = "UPDATE employees SET name=%s, fingerID=%s, faceID=%s, RFID=%s WHERE RFID=%s"
			bindData = (_name, _fingerID, _faceID, _RFID,_RFID)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			respone = jsonify('Employee updated successfully!')
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
		cursor.execute("DELETE FROM employees WHERE RFID =%s", (id))
		conn.commit()
		respone = jsonify('Employee deleted successfully!')
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