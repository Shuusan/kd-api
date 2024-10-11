from flask import Flask, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)
