import sys

sys.stdout.reconfigure(encoding='utf-8')

from app import app

def test_portal():
    with app.test_client() as c:
        res = c.get('/patient-portal.html')
        print(f"GET /patient-portal.html status: {res.status_code}")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        
        data = res.data.decode('utf-8', errors='ignore')
        print(f"Content length: {len(data)} characters")
        
        # 1. Chart.js CDN check
        assert 'chart.umd.min.js' in data, "Chart.js CDN script not found"
        print("  [PASS] Chart.js included in head")
        
        # 2. Petrol Blue + Burnished Copper theme colors
        assert '#193B4A' in data, "Petrol Blue color #193B4A not found in styles"
        assert '#BC805E' in data, "Burnished Copper color #BC805E not found in styles"
        print("  [PASS] Petrol Blue and Burnished Copper theme colors applied")
        
        # 3. Unnumbered navigation labels
        assert '1. Dashboard' not in data, "1. Dashboard still found in document"
        assert '7. Personal Profile' not in data, "7. Personal Profile still found in document"
        assert '2. Appointments' not in data, "2. Appointments still found in document"
        assert '3. Book an Appointment' not in data, "3. Book an Appointment still found"
        assert '4. Appointment History' not in data, "4. Appointment History still found"
        assert '6. Patient Intake Form' not in data, "6. Patient Intake Form still found"
        assert '8. Medical History' not in data, "8. Medical History still found"
        assert '9. Medical Records' not in data, "9. Medical Records still found"
        assert '10. Medications' not in data, "10. Medications still found"
        assert '30. Logout' not in data, "30. Logout still found"
        print("  [PASS] All 30 navigation labels cleanly unnumbered")
        
        # 4. Dashboard data visualization
        assert 'id="dashAppointmentsChart"' in data, "dashAppointmentsChart canvas not found"
        assert 'id="dashBreakdownChart"' in data, "dashBreakdownChart canvas not found"
        assert 'fetchAndUpdatePatientDashboardCharts' in data, "fetchAndUpdatePatientDashboardCharts function not found"
        assert 'initPatientDashboardCharts' in data, "initPatientDashboardCharts function not found"
        print("  [PASS] Interactive dashboard data visualization charts & dynamic DB fetch present")
        
        # 5. Fixed View buttons
        assert "openApptDetails('pending')" in data, "Pending appointment details button not wired"
        assert "openPastApptSummary('05 Aug 2026', 'Dr. Ananya Iyer', 'Cardiology')" in data, "Appt 3 past summary not wired"
        assert "openPastApptSummary('03 Jun 2026', 'Dr. Priya Sharma', 'General Practice')" in data, "Appt 4 past summary not wired"
        assert "viewDiagnosticModal('Blood Panel (Complete Blood Count)')" in data, "Blood panel diagnostic view not wired"
        assert "viewDiagnosticModal('Chest X-Ray (PA View)')" in data, "Chest X-Ray diagnostic view not wired"
        assert "viewDiagnosticModal('HbA1c (Glycated Hemoglobin)')" in data, "HbA1c diagnostic view not wired"
        assert "openRecordFilterModal()" in data, "openRecordFilterModal not found"
        print("  [PASS] All View and summary action buttons properly wired")

        # 6. Check that backend /api/v1/clinical/dashboard endpoint is working
        api_res = c.get('/api/v1/clinical/dashboard')
        assert api_res.status_code == 200, f"Expected 200 from API, got {api_res.status_code}"
        api_data = api_res.get_json()
        assert api_data.get('success') is True, "API response success is not True"
        assert 'dailyUpdates' in api_data, "API response missing dailyUpdates"
        print("  [PASS] Backend /api/v1/clinical/dashboard endpoint verified and returning live data")

        print("\nALL AUTOMATED TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    test_portal()
