import unittest
import os
import re
from app import app, PORTAL_ACCOUNTS, ROLE_TARGET_MAP

class UnifiedLoginFlowTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_single_entry_point_login_page(self):
        """Verify the unified login page is served at /login and /login.html with role options."""
        for path in ['/login', '/login.html']:
            res = self.app.get(path)
            self.assertEqual(res.status_code, 200)
            self.assertIn(b'Healthcare Portal Sign In', res.data)
            self.assertIn(b'Patient', res.data)
            self.assertIn(b'Clinician', res.data)
            self.assertIn(b'Staff', res.data)
            self.assertIn(b'Admin', res.data)

    def test_clinician_authentication_and_redirection(self):
        """Verify clinician login redirects directly to the Clinician Dashboard with session and cookies."""
        res = self.app.post('/api/v1/auth/login', json={
            'username': 'clinician',
            'password': 'clinic@123',
            'portal': 'clinician'
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data['authenticated'])
        self.assertEqual(data['user']['role'], 'Clinician')
        self.assertEqual(data.get('redirect'), '/clinician-portal.html')

        # Check cookies set on response
        cookies = res.headers.get_all('Set-Cookie')
        cookie_text = " ".join(cookies)
        self.assertIn('nexcura_clinician_auth=authenticated', cookie_text)
        self.assertIn('nxc_auth_role=clinician', cookie_text)

    def test_all_roles_redirection_destinations(self):
        """Verify Patient, Clinician, Staff, Admin each receive their correct dashboard target."""
        expected_destinations = {
            'patient': ('patient', 'patient@123', '/patient-portal.html'),
            'clinician': ('clinician', 'clinic@123', '/clinician-portal.html'),
            'staff': ('staff', 'staff@123', '/staff-portal.html'),
            'admin': ('admin', 'admin@123', '/admin-portal.html'),
        }

        for role, (user, pwd, expected_dest) in expected_destinations.items():
            with self.subTest(role=role):
                res = self.app.post('/login', json={
                    'username': user,
                    'password': pwd,
                    'portal': role
                })
                self.assertEqual(res.status_code, 200)
                data = res.get_json()
                self.assertTrue(data['authenticated'])
                self.assertEqual(data.get('redirect'), expected_dest)

    def test_clinician_portal_no_duplicate_login_page(self):
        """Verify clinician-portal.html has loginGate hidden by default and portalContent visible."""
        portal_path = os.path.join(os.path.dirname(__file__), 'clinician-portal.html')
        with open(portal_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # The duplicate loginGate must be hidden by default
        self.assertIn('id="loginGate" style="display:none;', content)
        # The portalContent must be visible by default (not display:none)
        self.assertIn('id="portalContent" style=""', content)

        # Must have single entry point redirection for unauthenticated visits
        self.assertIn("window.location.replace('login.html?role=clinician')", content)

        # Logout must redirect to login.html?role=clinician
        self.assertIn("function handleLogout()", content)
        self.assertIn("window.location.replace('login.html?role=clinician')", content)

    def test_patient_staff_admin_portal_single_entry_point(self):
        """Verify patient, staff, and admin portals redirect unauthenticated access to unified login page."""
        portals = [
            ('patient-portal.html', 'login.html?role=patient'),
            ('staff-portal.html', 'login.html?role=staff'),
            ('admin-portal.html', 'login.html?role=admin'),
        ]
        for filename, expected_redirect in portals:
            with self.subTest(portal=filename):
                file_path = os.path.join(os.path.dirname(__file__), filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.assertIn(expected_redirect, content)

    def test_logout_endpoint_clears_session_and_cookies(self):
        """Verify /logout clears all auth cookies and redirects to /login.html."""
        res = self.app.get('/logout')
        self.assertEqual(res.status_code, 302)
        self.assertIn('/login.html', res.headers.get('Location'))

        cookies = res.headers.get_all('Set-Cookie')
        cookie_text = " ".join(cookies)
        self.assertIn('nexcura_clinician_auth=;', cookie_text)
        self.assertIn('nexcura_patient_auth=;', cookie_text)

if __name__ == '__main__':
    unittest.main()
