from flask import Flask, render_template, request, jsonify
import qrcode
from io import BytesIO
import base64
import os
print(f"Templates Folder: {os.path.join(os.getcwd(), 'templates')}")


app = Flask(__name__)

tables = [
    {"id": 1, "status": "kosong"},
    {"id": 2, "status": "kosong"},
    {"id": 3, "status": "kosong"},
    {"id": 4, "status": "kosong"},
    {"id": 5, "status": "kosong"},
    {"id": 6, "status": "kosong"},
    {"id": 7, "status": "kosong"},
    {"id": 8, "status": "kosong"},
]

@app.route('/')
def index():

    table_data = []
    for table in tables:
        qr = qrcode.QRCode()
        qr_data = f"http://192.168.0.9:5000/update_status/{table['id']}"
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = BytesIO()
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img.save(img, format="PNG")
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        
        table_data.append({"table": table, "qr": img_base64})

    return render_template('index.html', table_data=table_data)

@app.route('/get_status', methods=['GET'])
def get_status():
    return jsonify({"tables": tables})


@app.route('/update_status/<int:table_id>', methods=['POST', 'GET'])
def update_status(table_id):
    for table in tables:
        if table['id'] == table_id:
            table['status'] = 'terisi' if table['status'] == 'kosong' else 'kosong'
            return jsonify({"success": True, "message": "Status Kamar diperbarui", "table": table})
    return jsonify({"success": False, "message": "Kamar tidak ditemukan"})


if __name__ == '__main__':
    app.run(host='192.168.0.9', port=5000, debug=True)
