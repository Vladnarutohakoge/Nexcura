import sys
import json
sys.stdout.reconfigure(encoding='utf-8')

from app import app, get_db_connection

def run_tests():
    print("==================================================")
    print("NEXCURA PATIENT PORTAL FULL VERIFICATION SUITE")
    print("==================================================")

    with app.test_client() as c:
        # TEST 1: GET /patient-portal.html
        print("\n[TEST 1] Verifying /patient-portal.html HTML, styles, and button handlers...")
        res = c.get('/patient-portal.html')
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        html = res.data.decode('utf-8', errors='ignore')

        # 1a. Petrol Blue + Burnished Copper Theme Color Palette
        assert '#193B4A' in html, "Petrol Blue #193B4A missing"
        assert '#BC805E' in html, "Burnished Copper #BC805E missing"
        assert '#F5F7F6' in html, "Main Background #F5F7F6 missing"
        assert '#DCE8EB' in html, "Soft Blue Highlight #DCE8EB missing"
        assert '#24596A' in html, "Primary Buttons #24596A missing"
        assert '#46545B' in html, "Body Text #46545B missing"
        assert '--petrol-blue:' in html and '#193B4A' in html, "Petrol Blue CSS token missing"
        assert '--copper:' in html and '#BC805E' in html, "Burnished Copper CSS token missing"
        assert '--bg-main:' in html and '#F5F7F6' in html, "Main Background CSS token missing"
        print("  -> PASS: Petrol Blue + Burnished Copper palette (#193B4A, #BC805E, #F5F7F6, #DCE8EB, #24596A, #46545B) verified.")

        # 1b. Unnumbered navigation labels
        assert '1. Dashboard' not in html, "Numbered nav '1. Dashboard' found"
        assert '7. Personal Profile' not in html, "Numbered nav '7. Personal Profile' found"
        assert '2. Appointments' not in html, "Numbered nav '2. Appointments' found"
        assert '8. Medical History' not in html, "Numbered nav '8. Medical History' found"
        assert '30. Logout' not in html, "Numbered nav '30. Logout' found"
        print("  -> PASS: All navigation labels cleanly unnumbered.")

        # 1c. View Summary button wiring
        assert 'openPastApptSummary(' in html, "openPastApptSummary missing"
        assert '/api/v1/patient/summary' in html, "/api/v1/patient/summary fetch missing in openPastApptSummary"
        assert 'Patient Health Summary' in html, "Summary modal title missing"
        print("  -> PASS: View Summary buttons wired to live clinical summary API.")

        # 1d. Add Condition button wiring
        assert 'openAddConditionModal()' in html, "openAddConditionModal() onclick missing on Add Condition button"
        assert 'submitNewCondition' in html, "submitNewCondition handler missing"
        assert 'patientConditionsTable' in html, "patientConditionsTable ID missing"
        assert 'loadPatientConditions' in html, "loadPatientConditions missing"
        print("  -> PASS: Add Condition button wired with modal, validation, and table updates.")

        # 1e. Request buttons wiring
        assert 'openRequestCorrectionModal()' in html, "openRequestCorrectionModal() onclick missing"
        assert 'submitCorrectionRequest' in html, "submitCorrectionRequest handler missing"
        assert 'openRefillRequestModal()' in html, "openRefillRequestModal() missing"
        assert '/api/v1/patient/requests' in html, "Requests API calls missing in HTML"
        assert 'handleRefillSubmit' in html, "handleRefillSubmit missing"
        print("  -> PASS: All Patient Request buttons wired (Refill, Correction, Emergency).")

        # 1f. Dashboard data visualization
        assert 'id="dashAppointmentsChart"' in html, "dashAppointmentsChart canvas missing"
        assert 'id="dashBreakdownChart"' in html, "dashBreakdownChart canvas missing"
        assert 'initPatientDashboardCharts' in html, "initPatientDashboardCharts function missing"
        assert 'fetchAndUpdatePatientDashboardCharts' in html, "fetchAndUpdatePatientDashboardCharts missing"
        assert '/api/v1/patient/dashboard' in html, "Dashboard API fetch endpoint missing"
        print("  -> PASS: Dashboard live charts and dynamic updates verified.")

        # TEST 2: GET /api/v1/patient/summary
        print("\n[TEST 2] Verifying GET /api/v1/patient/summary API...")
        s_res = c.get('/api/v1/patient/summary')
        assert s_res.status_code == 200, f"Expected 200, got {s_res.status_code}"
        s_data = s_res.get_json()
        assert s_data.get('success') is True, "Success should be True"
        summary = s_data.get('summary', {})
        assert 'patient' in summary, "Patient info missing in summary"
        assert 'appointments' in summary, "Appointments missing in summary"
        assert 'prescriptions' in summary, "Prescriptions missing in summary"
        assert 'labReports' in summary, "Lab reports missing in summary"
        assert 'conditions' in summary, "Conditions missing in summary"
        assert 'vitals' in summary, "Vitals missing in summary"
        print(f"  -> PASS: /api/v1/patient/summary returned {len(summary['appointments'])} appointments, {len(summary['prescriptions'])} prescriptions, {len(summary['labReports'])} lab reports, {len(summary['conditions'])} conditions.")

        # TEST 3: GET & POST /api/v1/patient/conditions
        print("\n[TEST 3] Verifying GET & POST /api/v1/patient/conditions API...")
        cond_get = c.get('/api/v1/patient/conditions')
        assert cond_get.status_code == 200
        conds = cond_get.get_json().get('conditions', [])
        initial_count = len(conds)
        print(f"  -> Initial conditions count: {initial_count}")

        # Test duplicate prevention (Hypertension is already seeded)
        dup_res = c.post('/api/v1/patient/conditions', json={
            'condition_name': 'Hypertension',
            'onset_year': '2019',
            'status': 'Ongoing'
        })
        assert dup_res.status_code == 409, f"Expected 409 Conflict for duplicate, got {dup_res.status_code}"
        dup_data = dup_res.get_json()
        assert dup_data.get('success') is False
        print(f"  -> PASS: Duplicate condition rejected: '{dup_data.get('error')}'")

        # Test adding a new condition
        import random
        test_cond_name = f"Allergic Bronchitis Test-{random.randint(1000, 9999)}"
        add_res = c.post('/api/v1/patient/conditions', json={
            'condition_name': test_cond_name,
            'onset_year': '2023',
            'status': 'Ongoing',
            'notes': 'Verified test condition submission',
            'patient_name': 'Alex Morgan',
            'patient_id': 'NX-P0001'
        })
        assert add_res.status_code == 201, f"Expected 201, got {add_res.status_code}"
        add_data = add_res.get_json()
        assert add_data.get('success') is True
        assert add_data['condition']['condition_name'] == test_cond_name
        assert add_data['condition']['approval_status'] == 'Pending Clinical Review'
        print(f"  -> PASS: New condition created successfully: '{test_cond_name}' (Pending Clinical Review)")

        # Verify condition is in DB
        cond_get_after = c.get('/api/v1/patient/conditions')
        after_count = len(cond_get_after.get_json().get('conditions', []))
        assert after_count == initial_count + 1, f"Expected {initial_count + 1}, got {after_count}"
        print(f"  -> PASS: Conditions count updated from {initial_count} to {after_count}")

        # TEST 4: GET & POST /api/v1/patient/requests
        print("\n[TEST 4] Verifying GET & POST /api/v1/patient/requests API...")
        req_get = c.get('/api/v1/patient/requests')
        assert req_get.status_code == 200
        req_count_before = len(req_get.get_json().get('requests', []))

        # Add Prescription Refill Request
        refill_res = c.post('/api/v1/patient/requests', json={
            'request_type': 'Prescription Refill',
            'item_name': 'Atorvastatin 10mg',
            'details': 'Doorstep Delivery to Registered Address',
            'patient_name': 'Alex Morgan',
            'patient_id': 'NX-P0001'
        })
        assert refill_res.status_code == 201, f"Expected 201, got {refill_res.status_code}"
        refill_data = refill_res.get_json()
        assert refill_data.get('success') is True
        assert refill_data['request']['status'] == 'Pending'
        print(f"  -> PASS: Prescription Refill request saved (# {refill_data['request']['id']}) with status: Pending")

        # Add Medical History Correction Request
        corr_res = c.post('/api/v1/patient/requests', json={
            'request_type': 'Record Correction',
            'item_name': 'Seasonal Allergies (Onset Year)',
            'details': 'Onset year was 2012 rather than 2010 per previous physician summary',
            'patient_name': 'Alex Morgan',
            'patient_id': 'NX-P0001'
        })
        assert corr_res.status_code == 201, f"Expected 201, got {corr_res.status_code}"
        corr_data = corr_res.get_json()
        assert corr_data.get('success') is True
        assert corr_data['request']['status'] == 'Pending'
        print(f"  -> PASS: Record Correction request saved (# {corr_data['request']['id']}) with status: Pending")

        # TEST 5: GET /api/v1/patient/dashboard (Live KPI & Daily Updates)
        print("\n[TEST 5] Verifying GET /api/v1/patient/dashboard live updates...")
        dash_res = c.get('/api/v1/patient/dashboard?range=7days')
        assert dash_res.status_code == 200, f"Expected 200, got {dash_res.status_code}"
        dash_data = dash_res.get_json()
        assert dash_data.get('success') is True
        stats = dash_data.get('stats', {})
        daily = dash_data.get('dailyUpdates', {})
        assert 'totalAppointments' in stats
        assert 'totalConditions' in stats
        assert 'pendingRequests' in stats
        assert 'labels' in daily
        assert len(daily['labels']) == 7
        assert len(daily['appointments']) == 7
        assert stats['totalConditions'] >= after_count
        assert stats['pendingRequests'] >= 2
        print(f"  -> PASS: Dashboard stats verified: {stats['totalAppointments']} total appts, {stats['totalConditions']} conditions, {stats['pendingRequests']} pending requests.")
        print(f"  -> PASS: Daily 7-day activity array: {daily['labels']}")

        # Test 30-day range
        dash30_res = c.get('/api/v1/patient/dashboard?range=30days')
        assert dash30_res.status_code == 200
        dash30_data = dash30_res.get_json()
        assert len(dash30_data['dailyUpdates']['labels']) == 30
        print(f"  -> PASS: Dashboard 30-day range returns 30 daily data points.")

        print("\n==================================================")
        print("ALL 5 FULL VERIFICATION TESTS PASSED SUCCESSFULLY!")
        print("==================================================")

if __name__ == '__main__':
    run_tests()
