from flask import send_from_directory
from fpdf import FPDF
# --- Imports and App Setup ---
from flask import Flask, request, jsonify
import csv
import os
from flask_cors import CORS
from datetime import datetime


from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)
# --- Routes ---

# --- PDF Generation & File Serving Endpoints ---
@app.route('/api/waste/<int:waste_id>/generate_ack_slip', methods=['POST'])
def generate_ack_slip(waste_id):
    # Find waste entry
    rows = read_csv(WASTE_CSV)
    entry = next((row for row in rows if int(row['id']) == waste_id), None)
    if not entry:
        return jsonify({'status': 'fail', 'message': 'Waste entry not found'}), 404
    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Acknowledgment Slip', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Waste ID: {entry['id']}", ln=True)
    pdf.cell(0, 10, f"Food Item: {entry['food_item']}", ln=True)
    pdf.cell(0, 10, f"Quantity: {entry['quantity']} kg", ln=True)
    pdf.cell(0, 10, f"Date: {entry['waste_date']}", ln=True)
    pdf.cell(0, 10, f"City: {entry.get('city','')}", ln=True)
    pdf.cell(0, 10, f"State: {entry.get('state','')}", ln=True)
    pdf.cell(0, 10, f"Reason: {entry.get('waste_reason','')}", ln=True)
    pdf.cell(0, 10, f"Picked Up: {entry.get('picked_up','')}", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, 'This slip is auto-generated after successful pickup.', ln=True)
    filename = f"ack_auto_{waste_id}.pdf"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    pdf.output(filepath)
    return jsonify({'status': 'success', 'filename': filename})

@app.route('/uploads/<filename>', methods=['GET'])
def serve_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# ... BASE_DIR and UPLOAD_FOLDER are defined below ...
# --- Routes ---

# --- File Upload Helpers ---
def allowed_file(filename, allowed_exts):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts

# Donor uploads food image for a waste entry
@app.route('/api/waste/<int:waste_id>/upload_image', methods=['POST'])
def upload_food_image(waste_id):
    print('UPLOAD: Received upload request for waste_id:', waste_id)
    if 'file' not in request.files:
        print('UPLOAD ERROR: No file part in request')
        return jsonify({'status': 'fail', 'message': 'No file part in request'}), 400
    file = request.files['file']
    print('UPLOAD: File received:', file.filename)
    if file.filename == '':
        print('UPLOAD ERROR: No selected file')
        return jsonify({'status': 'fail', 'message': 'No selected file'}), 400
    if file and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
        filename = secure_filename(f"waste_{waste_id}_" + file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print('UPLOAD: Saving to', save_path)
        try:
            file.save(save_path)
            print('UPLOAD: File saved successfully')
            return jsonify({'status': 'success', 'filename': filename})
        except Exception as e:
            print('UPLOAD ERROR: Exception while saving file:', e)
            return jsonify({'status': 'fail', 'message': f'Error saving file: {e}'}), 500
    print('UPLOAD ERROR: Invalid file type')
    return jsonify({'status': 'fail', 'message': 'Invalid file type'}), 400

# NGO uploads acknowledgment slip for a waste entry
@app.route('/api/waste/<int:waste_id>/upload_ack', methods=['POST'])
def upload_acknowledgment(waste_id):
    if 'file' not in request.files:
        return jsonify({'status': 'fail', 'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'fail', 'message': 'No selected file'}), 400
    if file and allowed_file(file.filename, ALLOWED_DOC_EXTENSIONS):
        filename = secure_filename(f"ack_{waste_id}_" + file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Optionally, store filename in waste_data.csv (add 'ack_slip' column if needed)
        return jsonify({'status': 'success', 'filename': filename})
    return jsonify({'status': 'fail', 'message': 'Invalid file type'}), 400

# Admin fetches uploaded docs/images for verification
@app.route('/api/waste/<int:waste_id>/uploads', methods=['GET'])
def get_uploads_for_waste(waste_id):
    files = []
    for fname in os.listdir(app.config['UPLOAD_FOLDER']):
        if fname.startswith(f"waste_{waste_id}_") or fname.startswith(f"ack_{waste_id}_"):
            files.append(fname)
    return jsonify({'files': files})

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE_DIR, 'csv')
WASTE_CSV = os.path.join(CSV_DIR, 'waste_data.csv')
USERS_CSV = os.path.join(CSV_DIR, 'users.csv')
MESSAGES_CSV = os.path.join(CSV_DIR, 'messages.csv')
CONTACT_US_CSV = os.path.join(CSV_DIR, 'contact_us.csv')
LAB_TESTS_CSV = os.path.join(CSV_DIR, 'lab_tests.csv')

# Uploads config (must be after BASE_DIR)
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_DOC_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# Set upload folder config
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Helpers ---
def read_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def append_csv(filepath, fieldnames, data):
    file_exists = os.path.isfile(filepath)
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists or os.stat(filepath).st_size == 0:
            writer.writeheader()
        writer.writerow(data)

def clear_csv(filepath, fieldnames):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

# --- Routes ---

@app.route('/api/waste/<int:waste_id>', methods=['DELETE'])
def delete_waste(waste_id):
    fieldnames = ['id', 'food_item', 'quantity', 'waste_date', 'city', 'state', 'waste_reason']
    rows = read_csv(WASTE_CSV)
    new_rows = [row for row in rows if int(row['id']) != waste_id]
    with open(WASTE_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in new_rows:
            writer.writerow(row)
    return jsonify({'status': 'deleted', 'id': waste_id})

# --- Imports and App Setup ---
from flask import Flask, request, jsonify
import csv
import os
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE_DIR, 'csv')
WASTE_CSV = os.path.join(CSV_DIR, 'waste_data.csv')
USERS_CSV = os.path.join(CSV_DIR, 'users.csv')
MESSAGES_CSV = os.path.join(CSV_DIR, 'messages.csv')
CONTACT_US_CSV = os.path.join(CSV_DIR, 'contact_us.csv')

# --- Helpers ---
def read_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def append_csv(filepath, fieldnames, data):
    file_exists = os.path.isfile(filepath)
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists or os.stat(filepath).st_size == 0:
            writer.writeheader()
        writer.writerow(data)

def clear_csv(filepath, fieldnames):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

# --- Routes ---
@app.route('/api/clear_csv', methods=['POST'])
def clear_csv_api():
    data = request.json
    csv_type = data.get('csv_type')
    if csv_type == 'waste':
        clear_csv(WASTE_CSV, ['id', 'food_item', 'quantity', 'waste_date', 'city', 'state', 'waste_reason'])
    elif csv_type == 'users':
        clear_csv(USERS_CSV, ['id', 'name', 'username', 'password', 'email', 'role'])
    elif csv_type == 'messages':
        clear_csv(MESSAGES_CSV, ['recipient', 'message', 'timestamp'])
    elif csv_type == 'contact_us':
        clear_csv(CONTACT_US_CSV, ['name', 'email', 'subject', 'message', 'timestamp'])
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid csv_type'}), 400
    return jsonify({'status': 'cleared', 'csv_type': csv_type})

@app.route('/api/contact_us', methods=['POST'])
def contact_us():
    data = request.json
    fieldnames = ['name', 'email', 'subject', 'message', 'timestamp']
    data['timestamp'] = datetime.now().isoformat(sep=' ', timespec='seconds')
    append_csv(CONTACT_US_CSV, fieldnames, data)
    return jsonify({'status': 'contact saved'})

@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    fieldnames = ['recipient', 'message', 'timestamp']
    data['timestamp'] = datetime.now().isoformat(sep=' ', timespec='seconds')
    append_csv(MESSAGES_CSV, fieldnames, data)
    return jsonify({'status': 'message stored'})

# Helper to read CSV as list of dicts
def read_csv(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Helper to append row to CSV
def append_csv(filepath, fieldnames, data):
    file_exists = os.path.isfile(filepath)
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists or os.stat(filepath).st_size == 0:
            writer.writeheader()
        writer.writerow(data)

@app.route('/api/waste', methods=['GET'])
def get_waste():
    return jsonify(read_csv(WASTE_CSV))


@app.route('/api/waste', methods=['POST'])
def add_waste():
    data = request.json
    fieldnames = ['id', 'food_item', 'quantity', 'waste_date', 'city', 'state', 'waste_reason', 'picked_up']
    # Convert address to city if sent from old frontend
    if 'address' in data and 'city' not in data:
        data['city'] = data['address']
        del data['address']
    if 'picked_up' not in data:
        data['picked_up'] = ''
    append_csv(WASTE_CSV, fieldnames, data)
    return jsonify({'status': 'success'})

# PATCH endpoint to mark waste as picked up by NGO
@app.route('/api/waste/<int:waste_id>/pickup', methods=['PATCH'])
def pickup_waste(waste_id):
    fieldnames = ['id', 'food_item', 'quantity', 'waste_date', 'city', 'state', 'waste_reason', 'picked_up']
    rows = read_csv(WASTE_CSV)
    updated = False
    picked_entry = None
    for row in rows:
        if int(row['id']) == waste_id:
            row['picked_up'] = 'yes'
            picked_entry = row
            updated = True
    with open(WASTE_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    if updated:
        # Notify all NGOs of pickup
        users = read_csv(USERS_CSV)
        ngo_emails = [u['email'] for u in users if u.get('role', '').lower() == 'ngo']
        for ngo_email in ngo_emails:
            append_csv(MESSAGES_CSV, ['recipient', 'message', 'timestamp'], {
                'recipient': ngo_email,
                'message': f"A donation has been marked for pickup: {picked_entry.get('food_item', '')}, {picked_entry.get('quantity', '')}kg, {picked_entry.get('city', '')}, {picked_entry.get('state', '')}",
                'timestamp': datetime.now().isoformat(sep=' ', timespec='seconds')
            })
        return jsonify({'status': 'picked_up', 'id': waste_id})
    else:
        return jsonify({'status': 'not_found', 'id': waste_id}), 404

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(read_csv(USERS_CSV))

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    fieldnames = ['id', 'name', 'username', 'password', 'email', 'role']
    append_csv(USERS_CSV, fieldnames, data)
    # Notify all NGOs of new registration
    users = read_csv(USERS_CSV)
    ngo_emails = [u['email'] for u in users if u.get('role', '').lower() == 'ngo']
    for ngo_email in ngo_emails:
        append_csv(MESSAGES_CSV, ['recipient', 'message', 'timestamp'], {
            'recipient': ngo_email,
            'message': f"A new user has registered: {data.get('name', '')} ({data.get('email', '')})",
            'timestamp': datetime.now().isoformat(sep=' ', timespec='seconds')
        })
    return jsonify({'status': 'registered'})
# Endpoint for NGOs to view all donation data
@app.route('/api/ngo/donations', methods=['GET'])
def ngo_donations():
    return jsonify(read_csv(WASTE_CSV))

@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    users = read_csv(USERS_CSV)
    for user in users:
        if user['username'] == data['username'] and user['password'] == data['password']:
            return jsonify({'status': 'success', 'user': user})
    return jsonify({'status': 'fail', 'message': 'Invalid credentials'}), 401

@app.route('/api/lab_tests', methods=['POST'])
def submit_lab_test():
    data = request.json
    fieldnames = ['id', 'food_item', 'sample_date', 'status', 'result']
    # Assign new id
    existing = read_csv(LAB_TESTS_CSV)
    new_id = str(max([int(row['id']) for row in existing] or [0]) + 1)
    data['id'] = new_id
    data['status'] = 'Pending'
    data['result'] = ''
    append_csv(LAB_TESTS_CSV, fieldnames, data)
    return jsonify({'status': 'submitted', 'id': new_id})

@app.route('/api/lab_tests', methods=['GET'])
def get_lab_tests():
    return jsonify(read_csv(LAB_TESTS_CSV))

if __name__ == '__main__':
    app.run(debug=True)
