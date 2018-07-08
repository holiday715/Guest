from django.test import TestCase
from sign.models import Event,Guest
from django.contrib.auth.models import User

# Create your tests here.
class ModelTest(TestCase):


    def setUp(self):
        Event.objects.create(id=1,name='锤子手机发布会',status=True,limit=200,address='Yinhewan',start_time='2016-9-8')
        Guest.objects.create(id=1,event_id=1,realname='tina',phone='15210',email='123@qq.com',sign=False)


    def test_event_models(self):
        result=Event.objects.get(name='锤子手机发布会')
        self.assertEqual(result.address,'Yin')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result=Guest.objects.get(phone='15210')
        self.assertEqual(result.realname,'tina')
        self.assertFalse(result.sign)

class IndexPageTest(TestCase):
    """测试index视图"""
    def test_index_page_renders_index_template(self):
        response=self.client.get('/index/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')

class LoginActionTest(TestCase):
    """测试登录动作"""
    def setUp(self):
        User.objects.create_user('huhu','huhu@qq.com','huhu123456')
    def test_add_admin(self):
        user=User.objects.get(username='huhu')
        self.assertEqual(user.username,'huhu')
        self.assertEqual(user.email,'huhu@qq.com')

    def test_login_action_username_password_null(self):
        test_data={'username':'','password':''}
        response=self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password error!',response.content)

    def test_login_action_username_password_error(self):
        test_data={'username':'abc','password':'123'}
        response=self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password error!',response.content)

    def test_login_action_success(self):
        test_data={'username':'huhu','password':'huhu123456'}
        response=self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,302)

class EventManageTest(TestCase):
    def setUp(self):
        User.objects.create_user('nana','nana@qq.com','nana123456')
        Event.objects.create(name='xiaomi5',limit=100,address='tongzhou',status=1,start_time='2017-8-10 12:30:00')
        self.login_user={'username':'nana','password':'nana123456'}

    def test_event_manage_success(self):
        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/event_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'xiaomi5',response.content)
        self.assertIn(b'tongzhou',response.content)

    def test_event_manage_search_success(self):
        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/search_name/',{'name':'xiaomi5'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'xiaomi5', response.content)
        self.assertIn(b'tongzhou', response.content)

class GuestManageTest(TestCase):
    def setUp(self):
        User.objects.create_user('hehe','hehe@qq.com','hehe123456')
        Event.objects.create(id=1,name='dajiang',limit=2000,address='beijing',status=1,start_time='2017-8-10 12:30:00')
        Guest.objects.create(realname='wawa',phone=123456,email='wawa@qq.com',sign=0,event_id=1)
        self.login_user={'username':'hehe','password':'hehe123456'}
    def test_event_manage_success(self):
        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/guest_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'wawa',response.content)
        self.assertIn(b'123456',response.content)

class SignIndexActionTest(TestCase):
    def setUp(self):
        User.objects.create_user('admin','admin@qq.com','admin123456')
        Event.objects.create(id=1,name='xiaomi5',limit=200,address='beijing',status=1,start_time='2018-09-14 20:30:09')
        Event.objects.create(id=2, name='oppp', limit=200, address='shanghai', status=1,start_time='2018-09-14 20:30:09')
        Guest.objects.create(realname='haha',phone=1234,email='haha@qq.com',sign=0,event_id=1)
        Guest.objects.create(realname='hehe', phone=4321, email='hehe@qq.com', sign=1, event_id=2)
        self.login_user={'username':'admin','password':'admin123456'}
    def test_sign_index_action_phone_null(self):
        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/sign_index_action/1/',{'phone':''})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'phone error',response.content)
    def test_sign_index_action_phone_or_event_id_error(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2/', {'phone': '98'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'phone error.', response.content)
    def test_sign_index_action_user_sign_has(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2/', {'phone': '4321'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user has sign in', response.content)
    def test_sign_index_action_sign_success(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {'phone': '1234'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sign in success!', response.content)

