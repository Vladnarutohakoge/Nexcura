import unittest
import os
from app import app

class ClinicianPortalTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_clinician_portal_routes(self):
        """Verify routes that serve the clinician portal return HTTP 200."""
        routes = ['/clinician-portal', '/clinician', '/clinical-workspace', '/clinician-portal.html']
        for route in routes:
            with self.subTest(route=route):
                response = self.app.get(route)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'NexCura', response.data)
                self.assertIn(b'Dr. A. Mehta', response.data)

    def test_theme_color_tokens(self):
        """Verify Petrol Blue + Burnished Copper color palette tokens are strictly embedded."""
        portal_path = os.path.join(os.path.dirname(__file__), 'clinician-portal.html')
        with open(portal_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tokens = [
            '#193B4A', # Petrol Blue
            '#BC805E', # Burnished Copper
            '#F5F7F6', # Main Background
            '#FFFFFF', # Card Background
            '#DCE8EB', # Soft Blue Highlight
            '#24596A', # Primary Buttons
            '#46545B', # Body Text
            '#D8E1E4', # Borders
        ]
        for token in tokens:
            with self.subTest(token=token):
                self.assertIn(token.lower(), content.lower(), f"Expected color token {token} in clinician-portal.html")

    def test_login_gate_and_session_unlock(self):
        """Verify login gate handler, auto-unlock, and logout are defined."""
        portal_path = os.path.join(os.path.dirname(__file__), 'clinician-portal.html')
        with open(portal_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('id="loginGate"', content)
        self.assertIn('function handleLogin(', content)
        self.assertIn('function handleLogout(', content)
        self.assertIn("gate.style.display = 'none'", content)
        self.assertIn("portal.style.display = ''", content)

    def test_all_20_modules_present(self):
        """Verify all 20 required clinician modules exist as navigable sections and buttons."""
        portal_path = os.path.join(os.path.dirname(__file__), 'clinician-portal.html')
        with open(portal_path, 'r', encoding='utf-8') as f:
            content = f.read()

        required_modules = [
            'dashboard',
            'profile',
            'patient-mgmt',
            'patients',
            'records',
            'history',
            'schedule',
            'appointments',
            'teleconsult',
            'prescriptions',
            'clinical-notes',
            'diagnosis-support',
            'lab-reports',
            'treatment-plans',
            'med-management',
            'alerts',
            'health-analytics',
            'performance-analytics',
            'settings',
            'support',
            'trials',
            'referrals'
        ]
        for mod in required_modules:
            with self.subTest(module=mod):
                self.assertIn(f'id="section-{mod}"', content, f"Missing section section-{mod}")
                self.assertIn(f"switchSection('{mod}'", content, f"Missing switchSection navigation for {mod}")

    def test_3d_animation_canvas(self):
        """Verify 3D canvas and throttled 20-30 FPS frame rate logic."""
        portal_path = os.path.join(os.path.dirname(__file__), 'clinician-portal.html')
        with open(portal_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('id="clinician3DCanvas"', content)
        self.assertIn('TARGET_FPS = 25', content)
        self.assertIn('prefers-reduced-motion', content)
        self.assertIn('document.hidden', content)

    def test_charts_and_local_images(self):
        """Verify Chart.js initialization and local image assets."""
        portal_path = os.path.join(os.path.dirname(__file__), 'clinician-portal.html')
        with open(portal_path, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('id="clinicalTrendsChart"', content)
        self.assertIn('id="clinicalBreakdownChart"', content)
        self.assertIn('static/images/patient/dr_rohan_mehta.jpg', content)
        self.assertIn('static/images/patient/telemedicine_video_call.jpg', content)
        self.assertIn('static/images/patient/lab_diagnostic_testing.jpg', content)

if __name__ == '__main__':
    unittest.main()
