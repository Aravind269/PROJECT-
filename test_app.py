"""
Comprehensive Test Suite for Community Renewable Energy Awareness and Management Portal
"""
import py_loader
import unittest
import json
import time
from app import create_app
from models import db, User, Project, CommunityPost, FeedbackMessage, SavedCalculation

class CommunityPortalTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_01_home_page(self):
        """Test home page loads with HTTP 200 and key headlines"""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Community Renewable Energy Awareness', res.data)
        self.assertIn(b'Solar Energy', res.data)
        self.assertIn(b'Wind Energy', res.data)

    def test_02_awareness_page(self):
        """Test awareness page and source details"""
        res = self.client.get('/awareness')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Understanding Renewable Energy Sources', res.data)
        self.assertIn(b'Solar Energy', res.data)
        self.assertIn(b'Pollution', res.data)

    def test_03_article_detail(self):
        """Test educational article detail page"""
        res = self.client.get('/awareness/article/complete-guide-to-solar-pv')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'The Complete Guide to Solar Photovoltaic Systems', res.data)

    def test_04_calculator_page(self):
        """Test calculator page loads"""
        res = self.client.get('/calculator')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Solar & Carbon Energy Savings Calculator', res.data)
        self.assertIn(b'monthlyCostChart', res.data)

    def test_05_calculator_api(self):
        """Test dynamic calculation API endpoint"""
        payload = {
            'monthly_bill': 180,
            'tariff_rate': 0.16,
            'roof_area': 600,
            'sunlight_hours': 5.0,
            'offset_percentage': 100
        }
        res = self.client.post(
            '/api/calculate-savings',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(data['recommended_kw'], 0)
        self.assertGreater(data['monthly_savings'], 0)
        self.assertGreater(data['annual_co2_saved_tons'], 0)

    def test_06_projects_catalog(self):
        """Test renewable energy projects list and filter"""
        res = self.client.get('/projects')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Community Renewable Energy Projects', res.data)
        self.assertIn(b'Sunny Heights Community Solar Farm', res.data)

    def test_07_project_detail(self):
        """Test project detail page"""
        res = self.client.get('/projects/1')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Sunny Heights Community Solar Farm', res.data)
        self.assertIn(b'Capacity', res.data)

    def test_08_dashboard_page_and_api(self):
        """Test dashboard route and stats API"""
        res = self.client.get('/dashboard')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Community Renewable Energy Dashboard', res.data)

        api_res = self.client.get('/api/dashboard/stats')
        self.assertEqual(api_res.status_code, 200)
        stats = json.loads(api_res.data)
        self.assertIn('sources', stats)
        self.assertIn('generation_by_source', stats)

    def test_09_community_forum(self):
        """Test community page loads"""
        res = self.client.get('/community')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Community Experiences', res.data)

    def test_10_contact_form(self):
        """Test contact form validation and submission"""
        # GET
        res_get = self.client.get('/contact')
        self.assertEqual(res_get.status_code, 200)

        # POST valid feedback
        post_data = {
            'name': 'Test Citizen',
            'email': 'citizen@example.com',
            'subject': 'Solar Microgrid Inquiry',
            'category': 'Inquiry',
            'message': 'We are interested in installing a shared microgrid on our street.'
        }
        res_post = self.client.post('/contact', data=post_data, follow_redirects=True)
        self.assertEqual(res_post.status_code, 200)
        self.assertIn(b'Thank you! Your message and feedback have been successfully submitted', res_post.data)

        # Verify feedback message is in DB
        msg = FeedbackMessage.query.filter_by(email='citizen@example.com').first()
        self.assertIsNotNone(msg)
        self.assertEqual(msg.name, 'Test Citizen')

    def test_11_auth_flow(self):
        """Test user registration, login, profile view, and logout"""
        unique_email = f"pioneer_{int(time.time() * 1000)}@community.org"
        # Register
        reg_data = {
            'name': 'Green Pioneer',
            'email': unique_email,
            'password': 'password123',
            'confirm_password': 'password123',
            'location': 'Seattle, WA',
            'energy_interest': 'Rooftop Solar & Efficiency'
        }
        reg_res = self.client.post('/register', data=reg_data, follow_redirects=True)
        self.assertEqual(reg_res.status_code, 200)
        self.assertIn(b'Welcome to the Community Renewable Energy Portal', reg_res.data)

        # Logout
        logout_res = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You have been logged out securely', logout_res.data)

        # Login
        login_data = {
            'email': unique_email,
            'password': 'password123'
        }
        login_res = self.client.post('/login', data=login_data, follow_redirects=True)
        self.assertIn(b'Welcome back, Green Pioneer', login_res.data)

        # Profile
        prof_res = self.client.get('/profile')
        self.assertEqual(prof_res.status_code, 200)
        self.assertIn(b'Green Pioneer', prof_res.data)

if __name__ == '__main__':
    unittest.main()
