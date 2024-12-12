from flask import Flask, jsonify, request
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Configure the SQL Server connection
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=localhost\\SQLEXPRESS;'  # Use your SQL Server instance
    'DATABASE=kd2sidb;'              # Correct database name
    'Trusted_Connection=yes;'        # Use Windows Authentication
)


@app.route('/share_information', methods=['POST'])
def add_share_information():
    data = request.get_json()
    cursor = conn.cursor()
    query = """INSERT INTO dbo.share_information 
               (info_id, info_level, info_title, info_subtitle, copy_active, date_added, date_modified) 
               VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(
        query,
        (
            data['info_id'],
            data['info_level'],
            data['info_title'],
            data['info_subtitle'],
            int(data['copy_active']),
            data['date_added'],
            data['date_modified'],
        ),
    )
    conn.commit()
    return jsonify({"message": "Added successfully"}), 201

@app.route('/share_information', methods=['GET'])
def get_share_information():
    cursor = conn.cursor()
    query = "SELECT info_id, info_level, info_title, info_subtitle, copy_active, date_added, date_modified FROM dbo.share_information"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convert the rows into a list of dictionaries (JSON-like structure)
    result = []
    for row in rows:
        result.append({
            'info_id': str(row[0]),  # Convert GUID to string
            'info_level': row[1],
            'info_title': row[2],
            'info_subtitle': row[3],
            'copy_active': bool(row[4]),
            'date_added': str(row[5]),
            'date_modified': str(row[6]) if row[6] else None
        })
    
    return jsonify(result)

@app.route('/share_information/<info_id>', methods=['DELETE'])
def delete_share_information(info_id):
    cursor = conn.cursor()
    query = "DELETE FROM dbo.share_information WHERE info_id = ?"
    cursor.execute(query, (info_id,))
    conn.commit()
    return jsonify({"message": "Deleted successfully"}), 200

@app.route('/share_information/<info_id>', methods=['PUT'])
def update_share_information(info_id):
    data = request.get_json()
    cursor = conn.cursor()
    query = """UPDATE dbo.share_information 
               SET info_level = ?, info_title = ?, info_subtitle = ?, copy_active = ?, date_modified = GETDATE() 
               WHERE info_id = ?"""
    cursor.execute(
        query,
        (
            data['info_level'],
            data['info_title'],
            data['info_subtitle'],
            int(data['copy_active']),
            info_id
        ),
    )
    conn.commit()
    return jsonify({"message": "Updated successfully"}), 200



# Endpoint for pump_condition table
@app.route('/pump_condition', methods=['GET'])
def get_pump_conditions():
    pump_id = request.args.get('pump_id')
    cursor = conn.cursor()
    
    if pump_id:
        query = "SELECT pump_id, pump_on, current_water_level, active_since, last_active FROM dbo.pump_condition WHERE pump_id = ?"
        cursor.execute(query, (pump_id,))
    else:
        query = "SELECT pump_id, pump_on, current_water_level, active_since, last_active FROM dbo.pump_condition"
        cursor.execute(query)
    
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            'pump_id': int(row[0]),
            'pump_on': bool(row[1]),
            'current_water_level': float(row[2]),
            'active_since': str(row[3]) if row[3] else None,
            'last_active': str(row[4]) if row[4] else None
        })
    
    return jsonify(result)

# Endpoint for pump_error_log table
@app.route('/pump_error_log', methods=['GET'])
def get_pump_error_logs():
    pump_id = request.args.get('pump_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    cursor = conn.cursor()
    
    if pump_id and start_date and end_date:
        query = """SELECT pump_id, time_start, time_end, messages, officer 
                   FROM dbo.pump_error_log 
                   WHERE pump_id = ? AND time_start >= ? AND time_start <= ?"""
        cursor.execute(query, (pump_id, start_date, end_date))
    elif pump_id:
        query = "SELECT pump_id, time_start, time_end, messages, officer FROM dbo.pump_error_log WHERE pump_id = ?"
        cursor.execute(query, (pump_id,))
    else:
        query = "SELECT pump_id, time_start, time_end, messages, officer FROM dbo.pump_error_log"
        cursor.execute(query)
    
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            'pump_id': int(row[0]),
            'time_start': str(row[1]),
            'time_end': str(row[2]) if row[2] else None,
            'messages': row[3],
            'officer': row[4] if row[4] else None
        })
    
    return jsonify(result)

# Endpoint for pump_log table
@app.route('/pump_log', methods=['GET'])
def get_pump_logs():
    pump_id = request.args.get('pump_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    cursor = conn.cursor()
    
    if pump_id and start_date and end_date:
        query = """SELECT pump_id, water_level, date_time 
                   FROM dbo.pump_log 
                   WHERE pump_id = ? AND date_time >= ? AND date_time <= ?"""
        cursor.execute(query, (pump_id, start_date, end_date))
    elif pump_id:
        query = "SELECT pump_id, water_level, date_time FROM dbo.pump_log WHERE pump_id = ?"
        cursor.execute(query, (pump_id,))
    else:
        query = "SELECT pump_id, water_level, date_time FROM dbo.pump_log"
        cursor.execute(query)
    
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            'pump_id': int(row[0]),
            'water_level': float(row[1]),
            'date_time': str(row[2])
        })
    
    return jsonify(result)

# Endpoint for pump_master table
@app.route('/pump_master', methods=['GET'])
def get_pump_master():
    pump_id = request.args.get('pump_id')
    cursor = conn.cursor()
    
    if pump_id:
        query = "SELECT pump_id, lower_limit, upper_limit FROM dbo.pump_master WHERE pump_id = ?"
        cursor.execute(query, (pump_id,))
    else:
        query = "SELECT pump_id, lower_limit, upper_limit FROM dbo.pump_master"
        cursor.execute(query)
    
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            'pump_id': int(row[0]),
            'lower_limit': float(row[1]),
            'upper_limit': float(row[2])
        })
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
