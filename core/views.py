from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Test, Question, Result, CustomUser
from .utils import grade_answer


# LOGIN
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)
            return redirect("/dashboard/")

    return HttpResponse("""
    <body style="background:#0f172a;color:white;text-align:center;padding-top:100px;">
        <h2>Login</h2>
        <form method="post">
            <input name="username" placeholder="Username"><br><br>
            <input name="password" type="password" placeholder="Password"><br><br>
            <button>Kirish</button>
        </form>
    </body>
    """)


# DASHBOARD
@login_required
def dashboard(request):
    return HttpResponse("""
    <h2>Dashboard</h2>
    <a href="/create/">Test yaratish</a><br>
    <a href="/test/">Test topshirish</a><br>
    <a href="/stats/">Statistika</a><br>
    <a href="/users/">Users</a><br>
    <a href="/results/">Results</a><br>
    <a href="/logout/">Logout</a>
    """)


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("/login/")


# TEST CREATE
def create_test(request):
    if request.method == "POST":
        test = Test.objects.create(title=request.POST.get("title"))

        Question.objects.create(
            test=test,
            text=request.POST.get("question"),
            correct_answer=request.POST.get("correct")
        )

        return HttpResponse("Test yaratildi ✅")

    return HttpResponse("""
    <h2>Create Test</h2>
    <form method="post">
        <input name="title" placeholder="Test name"><br><br>
        <input name="question" placeholder="Question"><br><br>
        <input name="correct" placeholder="Correct answer"><br><br>
        <button>Save</button>
    </form>
    """)


# TAKE TEST
def take_test(request):
    test = Test.objects.last()
    questions = test.questions.all()

    if request.method == "POST":
        total = 0

        for q in questions:
            ans = request.POST.get(str(q.id))
            total += grade_answer(ans, q.correct_answer)

        score = round(total / len(questions), 2)

        Result.objects.create(test=test, score=score)

        return HttpResponse(f"<h2>Natija: {score}%</h2>")

    html = "<form method='post'>"

    for q in questions:
        html += f"<p>{q.text}</p><input name='{q.id}'><br><br>"

    html += "<button>Submit</button></form>"

    return HttpResponse(html)


# USERS
def users_list(request):
    users = CustomUser.objects.all()
    return HttpResponse("<br>".join([f"{u.username} | {u.role}" for u in users]))


# RESULTS
def results_list(request):
    results = Result.objects.all()
    return HttpResponse("<br>".join([f"{r.test.title} - {r.score}%" for r in results]))


# STATS
def stats_view(request):
    data = [r.score for r in Result.objects.all()]

    return HttpResponse(f"""
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <canvas id="c"></canvas>
    <script>
    new Chart(document.getElementById('c'), {{
        type: 'line',
        data: {{
            labels: {list(range(len(data)))},
            datasets: [{{data: {data}, borderColor:'cyan'}}]
        }}
    }});
    </script>
    """)
