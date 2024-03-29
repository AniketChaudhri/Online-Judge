from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from judge.models import Problem, Submission, Coder, TestCase
from judge.forms import UserForm, ProblemForm, SubmissionForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    return render(request, 'judge/index.html')

def all_problems(request):
    problems = Problem.objects.all()
    return render(request, "judge/all.html", {"problems":problems})


def view_problem(request, pid):
    problem = get_object_or_404(Problem, code=pid)
    payload = {"problem": problem}
    return render(request, "judge/problem.html", payload)


def register_user(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            # save the user to the db
            u = user_form.save()
            u.set_password(u.password)
            u.save()

            coder = Coder(user=u)
            coder.link = "/judge/users/%s" % (u.username)
            coder.score = 0
            # calculation of rank in the beginning
            coder.rank = -1
            for k in Coder.objects.all():
                coder.rank = max(coder.rank, k.rank)
            coder.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, "judge/register.html", {"user_form": user_form, "registered": registered})


def loguserin(request):
    # if form has been filled and sent by the user
    if request.method == 'POST':
        # get the username and password
        username = request.POST.get('username')
        password = request.POST.get('password')
        # authenticate the user using django's in built authenticate function
        user = authenticate(username=username, password=password)
        if user:  # if the user exists log her in and redirect back to home page
            login(request, user)
            return HttpResponseRedirect('/judge/')
        else:  # otherwise redirect to a page showing an error
            print("Invalid login details: {}, {}".format(username, password))
            return HttpResponse("Invalid Login Details")
    else:
        return render(request, "judge/login.html", {})


def add_problem(request):
    # if user is not logged in, throw him to a sign-in page
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/judge/login/")
    else:
        if request.method == 'POST':
            problem_form = ProblemForm(request.POST, request.FILES)
            if problem_form.is_valid():
                # save a new problem
                problem = problem_form.save()
                problem.link = "/judge/problems/%s" % (problem.code)
                problem.author = Coder.objects.get(user=request.user)
                problem.save()
                # link the added test case to the problem and save the test case to db
                try:
                    test = TestCase(problem=problem, input_file=request.FILES['input1'],
                                    output_file=request.FILES['output1'])
                    test.save()
                except:
                    print("error")
                return HttpResponseRedirect("/judge/")
        else:
            # instantiate a new ProblemForm and then render the addproblem page
            problem_form = ProblemForm()
        return render(request, "judge/addproblem.html", {"problem_form": problem_form})
