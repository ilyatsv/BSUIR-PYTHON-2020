import hashlib
# Create your tests here.
import pytest
import datetime
from django.test import TestCase
from django.urls import reverse, resolve
from django.test import Client
from django.contrib.auth import authenticate
from firstapp.admin import EmailReply
from firstapp.models import *
from django.contrib.admin.sites import AdminSite
from firstapp.forms import RegisterUserForm, AuthUserForm,StudentForm

@pytest.fixture(scope="function")
def data_sourse(db):
    c = Client()
    c.post('/register', {'username': 'TEST', 'password': '123456', 'password_repeat': '123456', 'email': 'TEST@gmail.com'})
    c.post('/register', {'username': 'TEST2', 'password': '123456', 'password_repeat': '123456', 'email': 'TEST2@gmail.com'})
    user = User.objects.create(username="test1")
    user.set_password('123456')
    user.save()
    author = Author.objects.create(name="Lermantov")
    genre = Genre.objects.create(name="Genre")
    course = Course.objects.create(name="English",stage=1)
    book = Book.objects.create(name="test3", age=1982)
    book2 = Book.objects.create(name="test2", age=1983)
    book3 = Book.objects.create(name="test1", age=1981)
    student = Student.objects.create(name='test',age=23,book=book,user=User.objects.get(username='TEST'),stbool=True)    
    student.course.add(course)
    student.save()
    student = Student.objects.create(name='test2',age=23,book=book3,user=User.objects.get(username='test1'),stbool=True)    
    student.course.add(course)
    student.save()

def test_about():
    c = Client()
    response = c.post('/about')
    assert response.status_code == 200

def test_save(db, data_sourse):
    author = Author.objects.get(name="Lermantov")
    genre = Genre.objects.get(name="Genre")
    book = Book.objects.get(name="test3")
    course = Course.objects.get(name="English")
    #profile = Profile.objects.get(user__username="ilyatsv")
    assert author.name == "Lermantov"
    assert genre.name == "Genre"
    assert book.age == 1982
    assert course.stage == 1
    #assert profile.verified == True


def test_save_user(db, data_sourse):
    user = authenticate(username="TEST", password="123456")
    assert user.email == "TEST@gmail.com"



def test_save_feedback(db, data_sourse):
    feedback = Feedback.objects.create(email_reply_date=datetime.datetime.now(), email_reply_text="sdf",
                                       email_reply_capt="sdfs")
    feedback.email_reply_adress.add(Profile.objects.get(user__username="TEST"))
    my_model_admin = EmailReply(model=Feedback, admin_site=AdminSite())
    my_model_admin.save_model(obj=feedback, request=None, form=None, change=None)



@pytest.mark.parametrize("mail,username,password,password_repeat,error",
                         [('TEST@gmail.com', 'TEST', '123456', '123456', "Данная почта уже сужествует"),
                          ('123@gmail.com', 'TEST', '123456', '123456', "Данное имя уже сужествует"),
                          ('123@gmail.com', 'NEWTEST', '123456', '1234562', "Пароли не совпадают"), ])
def test_registration(db, data_sourse, mail, username, password, password_repeat, error):
    form_data = {'mail': mail, 'username': username, 'password': password, 'password_repeat': password_repeat}
    form = RegisterUserForm(data=form_data)
    assert form.error_value()[1] == error

def test_login(db, data_sourse):
    c = Client()
    response = c.post('/login')
    assert response.status_code == 200
    response = c.post('/login', {'username': 'TEST1', 'password': '123456'})
    assert response.status_code == 200
    response = c.post('/login', {'username': 'TEST', 'password': '123456'})
    assert response.status_code == 302

def test_logout(db, data_sourse):
    c = Client()
    assert c.login(username='TEST', password='123456')
    response = c.post('/logout')
    assert response.status_code == 302

def test_registration_url(db, data_sourse):
    c = Client()
    response = c.post('/register')
    assert response.status_code == 200
    c.post('/register', {'username': 'TEST2', 'password': '123456', 'password_repeat': '123456', 'email': 'TEST2@gmail.com'})
    assert response.status_code == 200


def test_page_confirmation(db, data_sourse):
    c = Client()
    sha = hashlib.md5(Profile.objects.get(user__username="TEST").__str__().encode())
    c.post("/confirmation/" + sha.hexdigest() + "/")
    c.post("/confirmation/" + sha.hexdigest() + "1/")

def test_bookpage(db, data_sourse):
    c = Client()
    response = c.get("/book")
    assert response.status_code == 200
    assert c.login(username='TEST', password='123456')
    response = c.get("/book")
    assert response.status_code == 200
    response = c.get("/book?search=1982&select=1")
    assert response.status_code == 200
    response = c.get("/book?search=Genre&select=2")
    assert response.status_code == 200
    response = c.get("/book?search=Lermontov&select=3")
    assert response.status_code == 200

def test_put_book(db,data_sourse):
    c = Client()
    c.login(username='test1', password='123456')
    response = c.post("/put_book")
    assert response.status_code == 301
    response = c.get("/take_book/0")
    assert response.status_code == 301
    response = c.get("/take_book/1")
    assert response.status_code == 301
    response = c.get("/take_book/2")
    assert response.status_code == 301

def test_kab(db, data_sourse):
    c=Client()
    assert c.login(username='TEST', password='123456')
    response = c.get("/kab")
    assert response.status_code == 200
    response = c.get("/kab?search=1")
    assert response.status_code == 200
    response = c.get("/kab?search=")
    assert response.status_code == 200
    response = c.get("/put_course/0")
    assert response.status_code == 301
    response = c.get("/take_course/0")
    assert response.status_code == 301
    response = c.get("/take_course/1")
    assert response.status_code == 301
    response = c.get("/put_course/1")
    assert response.status_code == 301



def test_index():
    c = Client()
    response = c.post('/index')
    assert response.status_code == 200
    response = c.get('')
    assert response.status_code == 200
    response = c.post('')
    assert response.status_code == 200

def test_create(db,data_sourse):
    c=Client()
    response = c.post('/create/',{'age':32,'author1':'Lermotov','author2':'','author3':'','genre':'Genre','name':'Lermontov2'})
    assert response.status_code == 302
    response = c.post('/create/',{'age':32,'author1':'Lermotov','author2':'123','author3':'123','genre':'Genre','name':'Lermontov2'})
    assert response.status_code == 302
    response = c.post('/create/',{'age':32,'author1':'Lermotov','author2':'123','author3':'','genre':'Genre','name':'Lermontov2'})
    assert response.status_code == 302
    response = c.post('/create/',{'age':32,'author1':'Lermotov','author2':'','author3':'123','genre':'Genre','name':'Lermontov2'})
    assert response.status_code == 302
    response = c.get('/book')
    #assert response.status_code ==200

def test_create_student(db,data_sourse):
    c=Client()
    assert c.login(username='TEST2', password='123456')
    response = c.get('/student')
    #assert response.status_code ==200
    response = c.post('/student',{'age':32,'book':1,'name':'Ilya'})
    assert response.status_code == 200
    response = c.post('/student')
    assert response.status_code == 200

@pytest.mark.parametrize("name,age",
                         [('Ilya', '23'),
                          ('Test', '23')])
def test_st_create(db, data_sourse, name, age):
    book = Book.objects.get(name="test2")
    form_data = {'name': name, 'age': age, 'book': book}
    form = StudentForm(data=form_data)
    assert form.tostr(name,age) == str(name+age)