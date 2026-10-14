import unittest
import os
import re
from app import app

class TestClinicianPortalFeatures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.portal_path = os.path.join(os.path.dirname(__file__), 'clinician-portal.html')
        with open(cls.portal_path, 'r', encoding='utf-8') as f:
            cls.html = f.read()

    def test_zero_placeholder_click_handlers(self):
        """Ensure no buttons or elements use placeholder showPreviewMsg(this, ...) calls."""
        placeholders = re.findall(r'showPreviewMsg\(this[^\)]*\)', self.html)
        self.assertEqual(len(placeholders), 0, f"Found placeholder handlers: {placeholders}")

    def test_palette_conformance(self):
        """Verify strict Petrol Blue + Burnished Copper color palette."""
        tokens = [
            '--petrol-blue:   #193B4A;',
            '--copper:        #BC805E;',
            '--bg-main:       #F5F7F6;',
            '--bg-card:       #FFFFFF;',
            '--soft-blue:     #DCE8EB;',
            '--primary-btn:   #24596A;',
            '--headings:      #193B4A;',
            '--body-text:     #46545B;',
            '--borders:       #D8E1E4;'
        ]
        for t in tokens:
            cleaned = t.replace(' ', '').lower()
            html_cleaned = self.html.replace(' ', '').lower()
            self.assertIn(cleaned, html_cleaned, f"Missing token: {t}")

    def test_required_modals_exist(self):
        """Verify all new functional modals exist in DOM."""
        modals = [
            'id="uploadRecordModal"',
            'id="orderLabModal"',
            'id="rescheduleModal"',
            'id="taskDetailsModal"',
            'id="referralDetailsModal"',
            'id="userManualModal"',
            'id="addPatientModal"',
            'id="newRefModal"',
            'id="chartDrawer"'
        ]
        for m in modals:
            self.assertIn(m, self.html, f"Missing modal: {m}")

    def test_functional_handlers_defined(self):
        """Verify JavaScript handler functions are defined for every module action."""
        handlers = [
            'function openUploadRecordModal(',
            'function submitUploadRecord(',
            'function openOrderLabModal(',
            'function submitOrderLab(',
            'function openRescheduleModal(',
            'function submitRescheduleAppointment(',
            'function toggleTeleMic(',
            'function toggleTeleCam(',
            'function toggleTeleScreenShare(',
            'function endTeleconsultEncounter(',
            'function attestMedicationReconciliation(',
            'function acknowledgeAllAlerts(',
            'function acknowledgeSingleAlert(',
            'function markAllNotificationsRead(',
            'function saveClinicianSettings(',
            'function handlePasswordUpdate(',
            'function openUserManualModal(',
            'function submitSupportTicket(',
            'function openTaskDetailsModal(',
            'function updateTaskModalStatus(',
            'function openReferralDetailsModal(',
            'function updateReferralModalStatus(',
            'function filterScheduleView('
        ]
        for h in handlers:
            self.assertIn(h, self.html, f"Missing handler: {h}")

    def test_data_visualization_elements(self):
        """Verify multi-metric chart datasets and dashboard indicators."""
        self.assertIn('Scheduled Visits', self.html)
        self.assertIn('Completed Encounters', self.html)
        self.assertIn('Pending Visits', self.html)
        self.assertIn('Diagnostic Lab Orders', self.html)
        self.assertIn('Follow-Up Tasks', self.html)
        self.assertIn('id="clinicalTrendsChart"', self.html)
        self.assertIn('id="clinicalBreakdownChart"', self.html)
        self.assertIn('id="dashScheduleTbody"', self.html)
        self.assertIn('id="dashMetricAppts"', self.html)
        self.assertIn('id="dashMetricIntake"', self.html)
        self.assertIn('id="dashMetricTasks"', self.html)
        self.assertIn('id="dashMetricAlerts"', self.html)

    def test_api_endpoints_functional(self):
        """Verify clinical backend endpoints return HTTP 200 with JSON structures."""
        endpoints = [
            '/api/v1/clinical/dashboard',
            '/api/v1/clinical/patients',
            '/api/v1/clinical/appointments',
            '/api/v1/clinical/prescriptions',
            '/api/v1/clinical/soap-notes',
            '/api/v1/clinical/lab-reports',
            '/api/v1/clinical/tasks',
            '/api/v1/clinical/referrals',
            '/api/v1/clinical/profile'
        ]
        for ep in endpoints:
            with self.subTest(endpoint=ep):
                res = self.client.get(ep)
                self.assertEqual(res.status_code, 200, f"Endpoint {ep} failed with status {res.status_code}")
                data = res.get_json()
                self.assertTrue(data.get('success', False) or len(data) > 0, f"Endpoint {ep} returned invalid payload")

if __name__ == '__main__':
    unittest.main()
