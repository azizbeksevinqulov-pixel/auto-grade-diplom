from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Test, Question, Result, CustomUser
from .utils import grade_answer


# ===================== REGISTER =====================
@csrf_exempt
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if not username or not password:
            return HttpResponse("Xatolik: ma'lumot to‘liq emas")

        CustomUser.objects.create_user(
            username=username,
            password=password,
            role=role
        )

        return redirect("/login/")

    return HttpResponse("""
    <body style="background:#0f172a;color:white;text-align:center;padding-top:100px;">
        <h2>Register</h2>

        <form method="post">
            <input name="username" placeholder="Username"><br><br>
            <input name="password" type="password" placeholder="Password"><br><br>

            <select name="role">
                <option value="student">Student</option>
                <option value="teacher">Teacher</option>
            </select><br><br>

            <button>Register</button>
        </form>

        <br>
        <a href="/login/" style="color:cyan;">Login</a>
    </body>
    """)


# ===================== LOGIN =====================
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)

            if user.role == "admin":
                return redirect("/admin-panel/")
            elif user.role == "teacher":
                return redirect("/create/")
            else:
                return redirect("/test/")

        return HttpResponse("Login xato ❌")

    return HttpResponse("""
    <body style="background:#0f172a;color:white;text-align:center;padding-top:100px;">
        <h2>Login</h2>

        <form method="post">
            <input name="username" placeholder="Username"><br><br>
            <input name="password" type="password" placeholder="Password"><br><br>
            <button>Kirish</button>
        </form>

        <br>
        <a href="/register/" style="color:cyan;">Register</a>
    </body>
    """)


# ===================== LOGOUT =====================
def logout_view(request):
    logout(request)
    return redirect("/login/")


# ===================== ADMIN PANEL =====================
@login_required
def admin_panel(request):
    return HttpResponse("""
    <h2>Admin Panel</h2>
    <a href="/users/">Foydalanuvchilar</a><br>
    <a href="/results/">Natijalar</a><br>
    <a href="/stats/">Statistika</a><br>
    <a href="/logout/">Chiqish</a>
    """)


# ===================== TEST CREATE =====================
@csrf_exempt
@login_required
def create_test(request):
    if request.method == "POST":
        test = Test.objects.create(title=request.POST.get("title"))

        Question.objects.create(
            test=test,
            text=request.POST.get("question"),
            correct_answer=request.POST.get("correct")
        )

        return HttpResponse("Test yaratildi ✅ <br><a href='/create/'>Yana qo‘shish</a>")

    return HttpResponse("""
    <h2>Test yaratish</h2>

    <form method="post">
        <input name="title" placeholder="Test nomi"><br><br>
        <input name="question" placeholder="Savol"><br><br>
        <input name="correct" placeholder="To‘g‘ri javob"><br><br>

        <button>Saqlash</button>
    </form>

    <br>
    <a href="/logout/">Logout</a>
    """)


# ===================== TEST TOPSHIRISH =====================
@csrf_exempt
@login_required
def take_test(request):
    test = Test.objects.last()

    if not test:
        return HttpResponse("Test mavjud emas")

    questions = test.questions.all()

    if request.method == "POST":
        total = 0

        for q in questions:
            ans = request.POST.get(str(q.id))
            total += grade_answer(ans, q.correct_answer)

        score = round(total / len(questions), 2)

        Result.objects.create(test=test, score=score)

        return HttpResponse(f"""
        <h2>Natija: {score}%</h2>
        <a href="/test/">Qayta topshirish</a>
        """)

    html = "<h2>Test</h2><form method='post'>"

    for q in questions:
        html += f"<p>{q.text}</p><input name='{q.id}'><br><br>"

    html += "<button>Yuborish</button></form>"

    return HttpResponse(html)


# ===================== USERS =====================
@login_required
def users_list(request):
    users = CustomUser.objects.all()

    html = "<h2>Foydalanuvchilar</h2>"
    for u in users:
        html += f"<p>{u.username} | {u.role}</p>"

    return HttpResponse(html)


# ===================== RESULTS =====================
@login_required
def results_list(request):
    results = Result.objects.all()

    html = "<h2>Natijalar</h2>"
    for r in results:
        html += f"<p>{r.test.title} - {r.score}%</p>"

    return HttpResponse(html)


# ===================== STATS =====================
@login_required
def stats_view(request):
    data = [r.score for r in Result.objects.all()]

    return HttpResponse(f"""
    <h2>Statistika</h2>

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


# ===================== ADMIN CREATE (TEMP) =====================
def create_admin(request):
    if not CustomUser.objects.filter(username="admin").exists():
        CustomUser.objects.create_superuser(
            username="admin",
            password="1234",
            role="admin"
        )
        return HttpResponse("Admin yaratildi: admin / 1234")

    return HttpResponse("Admin allaqachon bor")
