import hashlib
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Book,Author,Genre,Student,Course,Profile
from .forms import StudentForm,AuthUserForm,RegisterUserForm
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from hello.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone, dateformat
from django.contrib.postgres.search import SearchVector

def about(request):
    return HttpResponse("<h2>О сайте</h2>")
 
def index(request):
    return render(request, "index.html")

def book(request):
    search = request.GET.get('search','')
    select = request.GET.get('select','')
    if search:
        if select=='1':
            search_book_vector = SearchVector('name','age','author','genre')
            book= Book.objects.annotate(search=search_book_vector).filter(search=search)
        if select=='2':
            book=Book.objects.filter(genre__name=search)
        if select=='3':
            book=Book.objects.filter(author__name=search)
    else:
        book = Book.objects.all()
    return render(request, "book.html", {"book": book})
    
 

def create(request):
    if request.method == "POST":
        tom = Book()
        tom.name = request.POST.get("name")
        tom.age = request.POST.get("age")
        tom.save()
        genre = Genre(name= request.POST.get("genre"))
        genre.save()
        auth = Author(name = request.POST.get("author1"))
        auth.save()
        if not request.POST.get("author2") == "" and not request.POST.get("author3") == "":
            auth2 = Author(name = request.POST.get("author2"))
            auth2.save()
            auth3 = Author(name = request.POST.get("author3"))
            auth3.save()
            tom.author.add(auth,auth2,auth3)
        elif not request.POST.get("author2") == "":
            auth2 = Author(name = request.POST.get("author2"))
            auth2.save()
            tom.author.add(auth,auth2)
        elif not request.POST.get("author3") == "":
            auth3 = Author(name = request.POST.get("author3"))
            auth3.save()
            tom.author.add(auth,auth3)
        tom.author.add(auth)
        tom.genre.add(genre)
        return HttpResponseRedirect("/book")


def student_out(request):
    students = Student.objects.all()
    if request.method == 'POST':
        user=request.user
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = user
            student.stbool = True
            #student.user.save()
            student.save() # Now you can send it to DB
            form.save_m2m()
            return redirect("/")
        else :
            return render(request,'student.html',{'form':form,'students':students})   
    else:
        form=StudentForm()
        return render(request,"student.html",{'form':form,'students':students})
   

class MyprojectLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = '/'
    def get_success_url(self):
        return self.success_url

class RegisterUserView(CreateView):
    model = User
    template_name = 'register_page.html'
    form_class = RegisterUserForm
    success_url = '/'
    success_msg = 'Пользователь успешно создан'
    def form_valid(self,form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        email = form.cleaned_data["email"]
        aut_user = authenticate(username=username,password=password,email=email)
        login(self.request, aut_user)
        sha = hashlib.md5(username.encode())
        send_mail(
                'Подтверждение почты',
                render_to_string('message/message.txt', {
                    'name': username,
                    'email': email,
                    'text': 'http://127.0.0.1:8000/confirmation/' + sha.hexdigest(),
                    'time': str(dateformat.format(timezone.now(), 'Y-m-d H:i:s')),
                }), EMAIL_HOST_USER, [email])
        return form_valid

class MyProjectLogout(LogoutView):
    next_page = '/'

def page_confirmation(request, name):
    users = User.objects.all()
    context = {"information": "Активация прошла успешно"}
    for user in users:
        sha = hashlib.md5(user.username.encode())
        if sha.hexdigest() == name:
            user.profile.verified = True
            context["information"] = "Активация прошла успешно"
            user.save()
            break
    return render(request, 'confirmation.html', context) 

def put_book(request):
    try:
        student=request.user.student
        book=Book.objects.create(name='null',age=0)
        user = student.user 
        stbool=student.stbool
        courses = student.course.all()
        list=[]
        for co in courses:
            list.append(co)
        student.delete()
        newstudent=Student.objects.create(name=student.name,age=student.age,stbool=stbool,book=book,user=user)
        newstudent.course.set(courses)
        newstudent.save()
        return HttpResponseRedirect("/book")
    except Book.DoesNotExist:
        return HttpResponseNotFound("<h2>Book not found</h2>")

def take_book(request, id):
    book = Book.objects.get(id=id)
    student=request.user.student
    user = student.user 
    stbool=student.stbool
    book0=student.book
    courses = student.course.all()
    list=[]
    for co in courses:
        list.append(co)
    if student.book.name=='null':
        student.book.delete()
    else:
        student.delete()
    newstudent=Student.objects.create(name=student.name,age=student.age,stbool=stbool,book=book,user=user)
    newstudent.course.set(courses)
    newstudent.save()
    return HttpResponseRedirect("/book")

def kabinet(request):
    search = request.GET.get('search','')
    mycourse = request.user.student.course.all()
    if search:
        search_course_vector = SearchVector('name','stage')
        course= Course.objects.annotate(search=search_course_vector).filter(search=search)
    else:
        course = Course.objects.all()
        x= course.difference(mycourse)
        course=x
    return render(request, "kab.html", {"course": course,"mycourse":mycourse})

def take_course(request,id):
    try:
        course = Course.objects.get(id=id)
        request.user.student.course.add(course)
        request.user.student.save()
        return HttpResponseRedirect("/kab")
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Course not found</h2>")

def put_course(request,id):
    try:
        course = Course.objects.get(id=id)
        request.user.student.course.remove(course)
        request.user.student.save()
        return HttpResponseRedirect("/kab")
    except Course.DoesNotExist:
        return HttpResponseNotFound("<h2>Course not found</h2>")