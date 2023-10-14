from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages

from django.contrib.auth import login, authenticate, logout

from .models import ForumUser, Questions, Answers
from .forms import RegForm, AuthForm, ChangeProfileForm, QuestionForm, AnswerForm

@login_required
def index(request):
    users = ForumUser.objects.all().order_by('date_joined')
    checked_counter = request.session.get('checked', 0)
    question_counter = Questions.objects.all().count()

    checked_counter = question_counter - checked_counter

    context = {
        'users': users,
        'checked_counter': checked_counter
    }

    return render(request, 'index.html', context=context)

def reg(request):
    Form = RegForm()

    if request.method == "POST":
        Form = RegForm(request.POST)

        if Form.is_valid():
            host = request.META['HTTP_HOST']

            user = Form.save(commit=False)
            user.set_password(Form.cleaned_data['password'])
            user.generate_token()
            user.save()

            email_file_context = {'name': user.username, 'email': user.email, 'hash': user.unique_token, 'host': host}
            html_content = render_to_string('confirm_email.html', email_file_context)
            plain_text = strip_tags(html_content)

            send_mail('Verification Code', plain_text, "pmicb@forumstudy.uz", [user.email], html_message=html_content)
            messages.info(request, 'На вашу почту было отправлена ссылка потверждения аккаунта')

            return redirect('/auth')
        else:
            messages.error(request, 'Имя пользователя или почта уже заняты')

    return render(request, 'reg.html', context={'Form': Form})

def auth(request):
    Form = AuthForm()

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль')

    return render(request, 'auth.html', context={'Form': Form})

def verify(request, name, email):
    unique_token = request.GET.get('token')
    user = ForumUser.objects.get(username=name)

    if user.email == email and user.unique_token == unique_token:
        user.verified = True
        user.save()

        return redirect('/')
    else:
        return HttpResponse('Error! Invalid token or email')

@login_required
def ask_question(request):
    Form = QuestionForm()
    user = ForumUser.objects.get(username=request.user.username)

    if request.method == "POST":
        Form = QuestionForm(request.POST, request.FILES)

        if Form.is_valid():
            Form.instance.author = request.user
            Form.save()
            return redirect('/')
        else:
            messages.error(request, 'Форма заполнена неправильно')

    return render(request, 'ask_q.html', context={'Form': Form, 'user': user})

def questions(request):
    filter_query = request.GET.get('order_by')

    if not filter_query:
        questions = Questions.objects.all().order_by('-date')
    else:
        questions = Questions.objects.filter(subject=filter_query)
    
    request.session['checked'] = Questions.objects.all().count()

    return render(request, 'questions.html', context={'questions': questions})

def question_details(request, subject, id):
    question = Questions.objects.get(id=id)
    answers = Answers.objects.filter(question=id)

    Form = AnswerForm()

    if request.method == "POST":
        Form = AnswerForm(request.POST, request.FILES)

        if Form.is_valid():
            Form.instance.author = request.user
            Form.instance.question = question
            Form.save()

            return redirect(f'/q/{subject}/{id}')
        else:
            message.error(request, 'Форма заполнена неправильно')

    context={'question': question, 'Form': Form, 'answers': answers}
    return render(request, 'question_detail.html', context=context)

def user(request, username):
    current_user = request.user.username
    user = ForumUser.objects.get(username=username)
    questions = Questions.objects.filter(author=user.id).order_by('-date')

    context={'user': user, 'c_user': current_user, 'questions': questions}

    return render(request, 'user_detail.html', context=context)

@login_required
def settings(request, username):
    if request.user.username == username and request.user.verified:
        user = request.user
        Form = ChangeProfileForm(instance=user)

        if request.method == "POST":
            Form = ChangeProfileForm(request.POST, request.FILES, instance=user)

            if Form.is_valid():
                user = Form.save(commit=False)

                username = Form.cleaned_data.get('username')
                password = Form.cleaned_data.get('password')

                user.set_password(password)
                user.save()

                auth = authenticate(username=username, password=password)
                if auth is not None:
                    login(request, auth)
                    return redirect('/')
                else:
                    messages.error(request, 'Не удалось зарегистрировать')
            else:
                messages.error(request, 'Форма заполнена неправильно')

        return render(request, 'settings.html', context={'Form': Form})

    messages.error(request, 'Вы не являетесь данным пользователем либо вы не потвердили почту')
    return render(request, 'settings.html')

def about(request):
    return render(request, 'about.html')

@login_required
def logout_page(request):
    logout(request)
    return redirect('/reg')