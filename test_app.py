from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Test for the different user pages"""

    def setUp(self):
        """Add sample user"""

        User.query.delete()

        user = User(first_name='TestFName', last_name='TestLName', image_url='data:image/jpeg;base64,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')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Cleaning up """
        db.session.rollback()

    def test_users_page(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFName', html)

    def test_show_userinfo(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>TestFName TestLName</h2>', html)

    def create_newuser(self):
        with app.test_client() as client:
            d = {"first_name": "TestFName2", "last_name": "TestLName2",
                 "image_url": "https://i.pinimg.com/474x/88/25/21/882521a6c1fc9b389949700558a1ab25.jpg"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h2>TestFName2 TestLName2</h2>", html)

    def create_newpost(self):
        with app.test_client() as client:
            p = {"title": "TestPost1", "content": "TestingContent1", "user_id": 1}
            resp = client.post("/users/1/posts/new", data=p,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h2>TestPost1</h2>", html)

    def edit_newpost(self):
        with app.test_client() as client:
            p = {"title": "TestPost2", "content": "TestingContent2"}
            resp = client.post("/posts/1/edit", data=p,
                               follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h2>TestPost2</h2>", html)
