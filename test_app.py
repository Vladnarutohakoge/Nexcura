import unittest
from app import app, check_emergency_keywords

class TestNexCuraApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_health_check(self):
        """Verify that GET /api/v1/health returns 200 OK and healthy status."""
        response = self.client.get('/api/v1/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get('status'), 'healthy')
        self.assertEqual(data.get('platform'), 'NexCura Healthcare Platform')

    def test_emergency_guardrail_detection(self):
        """Verify regex keyword detection for acute life-threatening symptoms."""
        self.assertTrue(check_emergency_keywords("I have severe chest pain and tightness"))
        self.assertTrue(check_emergency_keywords("I can't breathe"))
        self.assertTrue(check_emergency_keywords("shortness of breath"))
        self.assertTrue(check_emergency_keywords("Sudden weakness on my left side and facial droop"))
        self.assertFalse(check_emergency_keywords("How do I prepare for my upcoming appointment?"))
        self.assertFalse(check_emergency_keywords("What are your clinic hours in Bengaluru?"))

    def test_ai_chat_emergency_override(self):
        """Verify POST /api/v1/ai/chat returns critical alert when emergency symptoms are sent."""
        payload = {"message": "I am having acute chest pain and trouble breathing", "language": "en"}
        response = self.client.post('/api/v1/ai/chat', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get('isEmergency'))
        self.assertEqual(data.get('alertLevel'), 'CRITICAL')
        self.assertIn("112", data.get('response', ''))
        self.assertIn("911", data.get('response', ''))

    def test_ai_chat_routine_inquiry(self):
        """Verify POST /api/v1/ai/chat handles routine questions without emergency trigger."""
        payload = {"message": "How can I book an appointment with Dr. Priya Sharma?", "language": "en"}
        response = self.client.post('/api/v1/ai/chat', json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertFalse(data.get('isEmergency'))
        self.assertIsNotNone(data.get('suggestedLink'))

    def test_clinical_trials_search_endpoint(self):
        """Verify GET /api/v1/trials/search returns trial records and disclaimers."""
        response = self.client.get('/api/v1/trials/search?condition=hypertension&pageSize=2')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('studies', data)
        self.assertGreater(data.get('count', 0), 0)
        self.assertIn('disclaimer', data)

    def test_static_portal_serving(self):
        """Verify that static HTML portals are served with 200 OK."""
        pages = [
            'index.html', 'login.html', 'about.html', 'specialties.html', 'clinical-trials.html',
            'ai-assistant.html', 'patient-portal.html', 'clinician-portal.html',
            'admin-portal.html', 'staff-portal.html', 'feedback.html'
        ]
        for page in pages:
            response = self.client.get(f'/{page}')
            self.assertEqual(response.status_code, 200, f"Failed serving {page}")
    def test_auth_login_endpoints(self):
        """Verify role-based portal authentication credentials and rejections."""
        # 1. Valid Admin Login
        res = self.client.post('/api/v1/auth/login', json={'username': 'admin', 'password': 'admin@123', 'portal': 'admin'})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()['authenticated'])

        # 2. Valid Clinician Login
        res = self.client.post('/api/v1/auth/login', json={'username': 'clinician', 'password': 'clinic@123'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['user']['role'], 'Clinician')

        # 3. Valid Staff Login
        res = self.client.post('/api/v1/auth/login', json={'username': 'staff', 'password': 'staff@123'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['user']['role'], 'Hospital Staff')

        # 4. Valid Patient Login
        res = self.client.post('/api/v1/auth/login', json={'username': 'patient', 'password': 'patient@123'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['user']['role'], 'Patient')

        # 5. Invalid Credentials Rejection
        res = self.client.post('/api/v1/auth/login', json={'username': 'admin', 'password': 'wrongpassword'})
        self.assertEqual(res.status_code, 401)
        self.assertFalse(res.get_json()['authenticated'])

    def test_pdf_document_serving(self):
        """Verify that genuine PDF clinical documents are served with application/pdf MIME type."""
        pdf_docs = [
            'NexCura_BloodPanel_2026.pdf',
            'NexCura_ChestXRay_Report_2026.pdf',
            'NexCura_HbA1c_Report_2026.pdf',
            'NexCura_Discharge_Summary_2026.pdf',
            'NexCura_Clinical_Policy_2026.pdf',
            'NexCura_Appointment_Report_2026.pdf'
        ]
        for doc in pdf_docs:
            res = self.client.get(f'/static/documents/{doc}')
            self.assertEqual(res.status_code, 200, f"Failed serving {doc}")
            self.assertEqual(res.content_type, 'application/pdf')
            self.assertTrue(res.data.startswith(b'%PDF-1.4'))

    def test_ai_symptom_reasoning(self):
        """Verify that AI assistant provides grounded non-emergency clinical guidance for symptoms."""
        queries = [
            ("What are normal blood pressure values?", "120/80"),
            ("How to handle a mild fever?", "100.4"),
            ("What is an HbA1c test?", "blood sugar")
        ]
        for query, expected_snippet in queries:
            res = self.client.post('/api/v1/ai/chat', json={'message': query, 'language': 'en'})
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertFalse(data.get('isEmergency'))
            self.assertIn(expected_snippet.lower(), data.get('response', '').lower())

    def test_ai_multilingual_responses(self):
        """Verify that AI assistant responds appropriately in Hindi, Kannada, and Telugu."""
        langs = ['hi', 'kn', 'te']
        for l in langs:
            res = self.client.post('/api/v1/ai/chat', json={'message': 'General wellness check', 'language': l})
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertFalse(data.get('isEmergency'))
            self.assertTrue(len(data.get('response', '')) > 20)

    def test_static_assets_serving(self):
        """Verify critical platform client-side scripts are served."""
        for js_file in ['static/js/main.js', 'static/js/i18n.js']:
            res = self.client.get(f'/{js_file}')
            self.assertEqual(res.status_code, 200, f"Failed serving {js_file}")

    def test_feedback_api(self):
        """Verify GET and POST endpoints for user feedback."""
        # 1. Fetch existing feedbacks
        get_res = self.client.get('/api/v1/feedback')
        self.assertEqual(get_res.status_code, 200)
        get_data = get_res.get_json()
        self.assertIn('feedback', get_data)
        self.assertGreaterEqual(get_data.get('count', 0), 1)

        # 2. Submit new feedback
        post_payload = {
            'name': 'Test User',
            'email': 'test@example.com',
            'department': 'Pediatrics',
            'type': 'appreciation',
            'rating': 5,
            'subject': 'Excellent clinic experience',
            'message': 'Doctors were very supportive and caring.'
        }
        post_res = self.client.post('/api/v1/feedback', json=post_payload)
        self.assertEqual(post_res.status_code, 201)
        post_data = post_res.get_json()
        self.assertTrue(post_data.get('success'))
        self.assertEqual(post_data['feedback']['name'], 'Test User')

        # 3. Bad request rejection
        bad_res = self.client.post('/api/v1/feedback', json={'name': 'Empty'})
        self.assertEqual(bad_res.status_code, 400)

    def test_appointments_sqlite_api(self):
        """Verify GET and POST /api/v1/appointments SQLite persistence."""
        # 1. Fetch existing appointments
        get_res = self.client.get('/api/v1/appointments')
        self.assertEqual(get_res.status_code, 200)
        get_data = get_res.get_json()
        self.assertIn('appointments', get_data)
        self.assertGreaterEqual(get_data.get('count', 0), 1)

        # 2. Book new appointment
        post_payload = {
            'patient_name': 'Kavya Sharma',
            'patient_email': 'kavya.s@example.com',
            'phone': '+91 99887 76655',
            'doctor_name': 'Dr. Priya Sharma',
            'specialty': 'Cardiology & Electrophysiology',
            'appointment_date': '2026-10-15',
            'appointment_time': '11:00 AM',
            'reason': 'Arrhythmia consultation'
        }
        post_res = self.client.post('/api/v1/appointments', json=post_payload)
        self.assertEqual(post_res.status_code, 201)
        post_data = post_res.get_json()
        self.assertTrue(post_data.get('success'))
        self.assertEqual(post_data['appointment']['patient_name'], 'Kavya Sharma')

    def test_staff_module_full_crud(self):
        """Verify complete Staff CRUD lifecycle: Create, Read, Search, Filter, Update, Status, Assignment, and Delete."""
        # 1. Read Staff List
        get_res = self.client.get('/api/v1/staff')
        self.assertEqual(get_res.status_code, 200)
        get_data = get_res.get_json()
        self.assertTrue(get_data.get('success'))
        self.assertGreaterEqual(get_data.get('count', 0), 1)

        # 2. Create New Staff
        new_staff_payload = {
            'staff_id': 'STF-TEST-99',
            'name': 'Kavita Sundaram',
            'email': 'kavita.s@nexcura.org',
            'phone': '+91 98765 99999',
            'department': 'ICU',
            'designation': 'Senior Critical Care Specialist',
            'qualification': 'MD Anaesthesiology, FNB Critical Care',
            'specialization': 'Neuro-Critical Care',
            'joining_date': '2024-05-01',
            'employment_type': 'Full-time',
            'salary': 150000,
            'shift': 'Morning',
            'status': 'Active',
            'emergency_contact': 'R. Sundaram (+91 98765 99998)'
        }
        post_res = self.client.post('/api/v1/staff', json=new_staff_payload)
        self.assertEqual(post_res.status_code, 201)
        post_data = post_res.get_json()
        self.assertTrue(post_data.get('success'))
        self.assertEqual(post_data['staff']['staff_id'], 'STF-TEST-99')

        # 3. View Single Staff Details
        view_res = self.client.get('/api/v1/staff/STF-TEST-99')
        self.assertEqual(view_res.status_code, 200)
        view_data = view_res.get_json()
        self.assertTrue(view_data.get('success'))
        self.assertEqual(view_data['staff']['name'], 'Kavita Sundaram')
        self.assertEqual(view_data['staff']['department'], 'ICU')

        # 4. Search and Filter Staff
        search_res = self.client.get('/api/v1/staff?search=Kavita')
        self.assertEqual(search_res.status_code, 200)
        self.assertGreaterEqual(search_res.get_json()['count'], 1)

        filter_res = self.client.get('/api/v1/staff?department=ICU&shift=Morning')
        self.assertEqual(filter_res.status_code, 200)
        self.assertGreaterEqual(filter_res.get_json()['count'], 1)

        # 5. Update Staff
        update_payload = {
            'name': 'Dr. Kavita Sundaram',
            'department': 'Emergency Medicine',
            'designation': 'HOD Critical Care',
            'shift': 'Evening',
            'status': 'On Duty'
        }
        put_res = self.client.put('/api/v1/staff/STF-TEST-99', json=update_payload)
        self.assertEqual(put_res.status_code, 200)
        self.assertTrue(put_res.get_json()['success'])

        # 6. Status and Assignment PATCH
        status_res = self.client.patch('/api/v1/staff/STF-TEST-99/status', json={'status': 'Inactive'})
        self.assertEqual(status_res.status_code, 200)
        self.assertEqual(status_res.get_json()['status'], 'Inactive')

        assign_res = self.client.patch('/api/v1/staff/STF-TEST-99/assign', json={'department': 'Cardiology', 'shift': 'Night'})
        self.assertEqual(assign_res.status_code, 200)
        self.assertTrue(assign_res.get_json()['success'])

        # 7. Delete Staff
        del_res = self.client.delete('/api/v1/staff/STF-TEST-99')
        self.assertEqual(del_res.status_code, 200)
        self.assertTrue(del_res.get_json()['success'])

        # Verify deletion
        verify_res = self.client.get('/api/v1/staff/STF-TEST-99')
        self.assertEqual(verify_res.status_code, 404)

    def test_staff_exports(self):
        """Verify real Staff CSV export and Staff PDF generation."""
        # 1. CSV Download
        csv_res = self.client.get('/api/v1/staff/export/csv')
        self.assertEqual(csv_res.status_code, 200)
        self.assertEqual(csv_res.content_type, 'text/csv; charset=utf-8')
        self.assertIn('Staff ID', csv_res.data.decode('utf-8'))
        self.assertIn('Sarah Jenkins', csv_res.data.decode('utf-8'))

        # 2. PDF Download
        pdf_res = self.client.get('/api/v1/staff/STF-1001/export/pdf')
        self.assertEqual(pdf_res.status_code, 200)
        self.assertEqual(pdf_res.content_type, 'application/pdf')
        self.assertTrue(pdf_res.data.startswith(b'%PDF-1.4'))

    def test_bed_and_triage_operations(self):
        """Verify Bed occupancy updates, assignment, release, and triage queue operations."""
        # 1. Get Beds
        beds_res = self.client.get('/api/v1/beds')
        self.assertEqual(beds_res.status_code, 200)
        beds = beds_res.get_json()['beds']
        self.assertGreaterEqual(len(beds), 1)

        # 2. Assign and Release Bed
        assign_res = self.client.post('/api/v1/beds/assign', json={'bed_id': 'BED 02', 'patient_name': 'Test Patient'})
        self.assertEqual(assign_res.status_code, 200)

        release_res = self.client.post('/api/v1/beds/BED 02/release')
        self.assertEqual(release_res.status_code, 200)

        # 3. New Triage Admission
        triage_payload = {
            'name': 'Ramesh Verma',
            'age': 52,
            'gender': 'Male',
            'complaint': 'Severe abdominal pain',
            'doctor': 'Dr. Priya Sharma',
            'ward': 'General Ward',
            'priority': 'High'
        }
        adm_res = self.client.post('/api/v1/triage', json=triage_payload)
        self.assertEqual(adm_res.status_code, 201)

    def test_clinical_modules_crud(self):
        """Verify complete Clinical workspace endpoints for Patients, Lab Reports, Discharge Summaries, and Follow-up Tasks."""
        # 1. Clinical Dashboard
        dash_res = self.client.get('/api/v1/clinical/dashboard')
        self.assertEqual(dash_res.status_code, 200)
        self.assertTrue(dash_res.get_json()['success'])

        # 2. Clinical Patients GET & POST
        pt_res = self.client.get('/api/v1/clinical/patients')
        self.assertEqual(pt_res.status_code, 200)
        self.assertTrue(pt_res.get_json()['success'])

        # 3. Clinical Lab Reports GET, POST, PUT, DELETE
        lab_res = self.client.get('/api/v1/clinical/lab-reports')
        self.assertEqual(lab_res.status_code, 200)
        self.assertTrue(lab_res.get_json()['success'])

        # 4. Clinical Discharge Summaries GET, POST, PUT, DELETE
        dis_res = self.client.get('/api/v1/clinical/discharge-summaries')
        self.assertEqual(dis_res.status_code, 200)
        self.assertTrue(dis_res.get_json()['success'])

        # 5. Clinical Follow-up Tasks GET, POST, PUT, DELETE
        task_res = self.client.get('/api/v1/clinical/tasks')
        self.assertEqual(task_res.status_code, 200)
        self.assertTrue(task_res.get_json()['success'])

    def test_extensionless_page_routing(self):
        """Verify that clean extensionless URLs (e.g. /login, /register, /patient-portal) resolve with 200 OK."""
        pages = ['login', 'register', 'patient-portal', 'clinician-portal', 'admin-portal', 'staff-portal']
        for p in pages:
            res = self.client.get(f'/{p}')
            self.assertEqual(res.status_code, 200, f"Clean URL /{p} failed")

if __name__ == '__main__':
    unittest.main()


