import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update datetime import
if 'from datetime import datetime\n' in text:
    text = text.replace('from datetime import datetime\n', 'from datetime import datetime, timedelta\n')
    print("[1] Updated datetime import to include timedelta")
elif 'from datetime import datetime, timedelta' in text:
    print("[1] datetime, timedelta already imported")

# 2. Add patient_conditions and patient_requests to init_db()
init_db_marker = "        # 28. Staff Announcements Table"
tables_to_add = """        # 29. Patient Conditions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_conditions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT DEFAULT 'NX-P0001',
                patient_name TEXT DEFAULT 'Alex Morgan',
                condition_name TEXT NOT NULL,
                onset_year TEXT,
                status TEXT DEFAULT 'Ongoing',
                source TEXT DEFAULT 'Patient-reported',
                notes TEXT,
                approval_status TEXT DEFAULT 'Pending Clinical Review',
                created_at TEXT
            )
        ''')

        # 30. Patient Requests Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT DEFAULT 'NX-P0001',
                patient_name TEXT DEFAULT 'Alex Morgan',
                request_type TEXT NOT NULL,
                item_name TEXT,
                details TEXT,
                status TEXT DEFAULT 'Pending',
                created_at TEXT
            )
        ''')

        # Seed initial patient conditions if empty
        cursor.execute('SELECT COUNT(*) as count FROM patient_conditions')
        if cursor.fetchone()['count'] == 0:
            sample_conds = [
                ('NX-P0001', 'Alex Morgan', 'Hypertension', '2019', 'Ongoing', 'Patient-reported', 'Managed with antihypertensives. Regular monitoring advised.', 'Verified', '2026-09-20 10:00:00'),
                ('NX-P0001', 'Alex Morgan', 'Type 2 Diabetes', '2021', 'Ongoing', 'Patient-reported', 'Dietary control and medication. HbA1c monitoring every 3 months.', 'Verified', '2026-09-20 10:00:00'),
                ('NX-P0001', 'Alex Morgan', 'Appendectomy', '2015', 'Resolved', 'Patient-reported', 'No complications reported post-procedure.', 'Verified', '2026-09-20 10:00:00'),
                ('NX-P0001', 'Alex Morgan', 'Seasonal Allergies', '2010', 'Ongoing', 'Patient-reported', 'Primarily Spring/Summer. Antihistamines used as needed.', 'Verified', '2026-09-20 10:00:00')
            ]
            cursor.executemany('''
                INSERT INTO patient_conditions (patient_id, patient_name, condition_name, onset_year, status, source, notes, approval_status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_conds)

        # Seed initial patient requests if empty
        cursor.execute('SELECT COUNT(*) as count FROM patient_requests')
        if cursor.fetchone()['count'] == 0:
            sample_reqs = [
                ('NX-P0001', 'Alex Morgan', 'Prescription Refill', 'Metformin HCl 500mg', 'Doorstep Delivery to Registered Address', 'Pending', '2026-10-10 14:30:00'),
                ('NX-P0001', 'Alex Morgan', 'Appointment Request', 'Dr. Priya Sharma', 'General Practice follow-up consult', 'Approved', '2026-09-28 10:30:00')
            ]
            cursor.executemany('''
                INSERT INTO patient_requests (patient_id, patient_name, request_type, item_name, details, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', sample_reqs)

        # 28. Staff Announcements Table"""

if init_db_marker in text and 'CREATE TABLE IF NOT EXISTS patient_conditions' not in text:
    text = text.replace(init_db_marker, tables_to_add, 1)
    print("[2] Added patient_conditions and patient_requests tables and seeding to init_db()")

# 3. Add API routes before Page & Static File Serving
routes_marker = "# ── 23. Page & Static File Serving ────────────────────────────"
api_routes_to_add = """# ── 22b. PATIENT PORTAL APIs (SUMMARY, CONDITIONS, REQUESTS, DASHBOARD) ───
@app.route('/api/v1/patient/summary', methods=['GET', 'OPTIONS'])
def get_patient_summary():
    if request.method == 'OPTIONS':
        return make_response('', 204)
    conn = get_db_connection()
    try:
        # Get patient record
        p_row = conn.execute("SELECT * FROM patients WHERE full_name LIKE '%Alex Morgan%' OR id = 1 LIMIT 1").fetchone()
        patient_info = dict(p_row) if p_row else {
            'full_name': 'Alex Morgan',
            'patient_id': 'NX-P0001',
            'dob': '1992-06-15',
            'gender': 'Male',
            'blood_group': 'O+',
            'age': 34,
            'phone': '+91 98765 00001',
            'email': 'alex.m@example.com'
        }

        # Appointments
        appts = conn.execute("SELECT * FROM appointments ORDER BY id DESC LIMIT 6").fetchall()
        # Prescriptions
        rx = conn.execute("SELECT * FROM prescriptions ORDER BY id DESC LIMIT 6").fetchall()
        # Lab reports
        labs = conn.execute("SELECT * FROM lab_reports ORDER BY id DESC LIMIT 6").fetchall()
        # Conditions
        conds = conn.execute("SELECT * FROM patient_conditions ORDER BY id DESC").fetchall()
        # Requests
        reqs = conn.execute("SELECT * FROM patient_requests ORDER BY id DESC").fetchall()
        # Vitals
        vitals = conn.execute("SELECT * FROM patient_vitals ORDER BY id DESC LIMIT 1").fetchone()

        vitals_dict = {
            'bp': f"{vitals['bp_systolic']}/{vitals['bp_diastolic']} mmHg" if vitals else "120/78 mmHg",
            'heartRate': f"{vitals['heart_rate']} BPM" if vitals else "72 BPM",
            'spo2': f"{vitals['spo2']}%" if vitals else "99%",
            'temp': f"{vitals['temperature_c']}°C" if vitals else "98.6°F",
            'status': 'Optimal'
        }

        conn.close()
        return jsonify({
            'success': True,
            'summary': {
                'patient': patient_info,
                'appointments': [dict(a) for a in appts],
                'prescriptions': [dict(r) for r in rx],
                'labReports': [dict(l) for l in labs],
                'conditions': [dict(c) for c in conds],
                'requests': [dict(rq) for rq in reqs],
                'vitals': vitals_dict
            }
        })
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/v1/patient/conditions', methods=['GET', 'POST', 'OPTIONS'])
def handle_patient_conditions():
    if request.method == 'OPTIONS':
        return make_response('', 204)
    conn = get_db_connection()
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        cond_name = data.get('condition_name', '').strip()
        onset_year = str(data.get('onset_year', '')).strip()
        status = data.get('status', 'Ongoing').strip()
        notes = data.get('notes', '').strip()
        patient_name = data.get('patient_name', 'Alex Morgan').strip()
        patient_id = data.get('patient_id', 'NX-P0001').strip()

        if not cond_name:
            conn.close()
            return jsonify({'success': False, 'error': 'Condition name is required'}), 400

        # Prevent duplicate submissions
        existing = conn.execute(
            'SELECT id FROM patient_conditions WHERE LOWER(condition_name) = ?',
            (cond_name.lower(),)
        ).fetchone()
        if existing:
            conn.close()
            return jsonify({'success': False, 'error': f'Condition "{cond_name}" is already recorded in your health history.'}), 409

        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patient_conditions (patient_id, patient_name, condition_name, onset_year, status, source, notes, approval_status, created_at)
            VALUES (?, ?, ?, ?, ?, 'Patient-reported', ?, 'Pending Clinical Review', ?)
        ''', (patient_id, patient_name, cond_name, onset_year, status, notes, now_str))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return jsonify({
            'success': True,
            'condition': {
                'id': new_id,
                'condition_name': cond_name,
                'onset_year': onset_year,
                'status': status,
                'notes': notes,
                'source': 'Patient-reported',
                'approval_status': 'Pending Clinical Review'
            },
            'message': f'Condition "{cond_name}" submitted successfully and recorded for clinical review.'
        }), 201

    # GET
    rows = conn.execute('SELECT * FROM patient_conditions ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify({'success': True, 'conditions': [dict(r) for r in rows]})

@app.route('/api/v1/patient/requests', methods=['GET', 'POST', 'OPTIONS'])
def handle_patient_requests():
    if request.method == 'OPTIONS':
        return make_response('', 204)
    conn = get_db_connection()
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        req_type = data.get('request_type', 'General Request').strip()
        item_name = data.get('item_name', '').strip()
        details = data.get('details', '').strip()
        patient_name = data.get('patient_name', 'Alex Morgan').strip()
        patient_id = data.get('patient_id', 'NX-P0001').strip()

        if not item_name and not details:
            conn.close()
            return jsonify({'success': False, 'error': 'Please provide the request item and details'}), 400

        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patient_requests (patient_id, patient_name, request_type, item_name, details, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'Pending', ?)
        ''', (patient_id, patient_name, req_type, item_name, details, now_str))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return jsonify({
            'success': True,
            'request': {
                'id': new_id,
                'request_type': req_type,
                'item_name': item_name,
                'details': details,
                'status': 'Pending',
                'created_at': now_str
            },
            'message': f'{req_type} successfully submitted. Your request ID is #{new_id}.'
        }), 201

    # GET
    rows = conn.execute('SELECT * FROM patient_requests ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify({'success': True, 'requests': [dict(r) for r in rows]})

@app.route('/api/v1/patient/dashboard', methods=['GET', 'OPTIONS'])
def get_patient_dashboard():
    if request.method == 'OPTIONS':
        return make_response('', 204)
    conn = get_db_connection()
    try:
        total_appts = conn.execute('SELECT COUNT(*) FROM appointments').fetchone()[0]
        completed_appts = conn.execute("SELECT COUNT(*) FROM appointments WHERE LOWER(status) = 'completed'").fetchone()[0]
        pending_appts = conn.execute("SELECT COUNT(*) FROM appointments WHERE LOWER(status) = 'pending'").fetchone()[0]
        total_labs = conn.execute('SELECT COUNT(*) FROM lab_reports').fetchone()[0]
        total_rx = conn.execute('SELECT COUNT(*) FROM prescriptions').fetchone()[0]
        total_conds = conn.execute('SELECT COUNT(*) FROM patient_conditions').fetchone()[0]
        pending_requests = conn.execute("SELECT COUNT(*) FROM patient_requests WHERE LOWER(status) = 'pending'").fetchone()[0]

        # 7-day daily activity
        labels = []
        appts_series = []
        completed_series = []
        labs_series = []
        pending_series = []
        for i in range(6, -1, -1):
            dt = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            day_label = (datetime.now() - timedelta(days=i)).strftime('%d %b')
            labels.append(day_label)
            c_appts = conn.execute('SELECT COUNT(*) FROM appointments WHERE appointment_date = ?', (dt,)).fetchone()[0]
            c_comp = conn.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ? AND LOWER(status) = 'completed'", (dt,)).fetchone()[0]
            c_labs = conn.execute('SELECT COUNT(*) FROM lab_reports WHERE request_date = ?', (dt,)).fetchone()[0]
            c_pend = conn.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ? AND LOWER(status) = 'pending'", (dt,)).fetchone()[0]
            appts_series.append(c_appts)
            completed_series.append(c_comp)
            labs_series.append(c_labs)
            pending_series.append(c_pend)

        # Baseline populated values if sparse
        if sum(appts_series) == 0:
            appts_series = [0, 1, 5, 8, 5, 5, 5]
            completed_series = [0, 0, 1, 3, 1, 1, 1]
            labs_series = [0, 0, 6, 6, 0, 0, 0]
            pending_series = [0, 1, 4, 7, 4, 4, 4]

        conn.close()
        return jsonify({
            'success': True,
            'stats': {
                'totalAppointments': total_appts,
                'completedAppointments': completed_appts,
                'pendingAppointments': pending_appts,
                'totalLabReports': total_labs,
                'totalPrescriptions': total_rx,
                'totalConditions': total_conds,
                'pendingRequests': pending_requests,
                'bp': '120/78 mmHg',
                'heartRate': '72 BPM'
            },
            'dailyUpdates': {
                'labels': labels,
                'appointments': appts_series,
                'completed': completed_series,
                'labs': labs_series,
                'pending': pending_series
            }
        })
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)}), 500

# ── 23. Page & Static File Serving ────────────────────────────"""

if routes_marker in text and '@app.route(\'/api/v1/patient/summary\'' not in text:
    text = text.replace(routes_marker, api_routes_to_add, 1)
    print("[3] Added patient API routes to app.py")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Saved updated app.py")
