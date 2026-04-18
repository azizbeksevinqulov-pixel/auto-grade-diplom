from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from .models import Test, Question, Result, CustomUser
from .utils import grade_answer


# ===================== REGISTER =====================
@csrf_exempt
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role", "student")

        if not username or not password:
            return HttpResponse("Username va parol majburiy!")

        if CustomUser.objects.filter(username=username).exists():
            return HttpResponse("Bu username allaqachon mavjud!")

        CustomUser.objects.create_user(username=username, password=password, role=role)
        return redirect("/login/")

    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Ro'yxatdan o'tish</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>body { background: linear-gradient(135deg, #0f172a, #1e2937); color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center; }</style>
    </head>
    <body>
        <div class="card p-4 shadow" style="width: 420px; background: rgba(255,255,255,0.1);">
            <h2 class="text-center mb-4">Ro'yxatdan o'tish</h2>
            <form method="post">
                <div class="mb-3"><input name="username" class="form-control" placeholder="Username" required></div>
                <div class="mb-3"><input name="password" type="password" class="form-control" placeholder="Parol" required></div>
                <div class="mb-3">
                    <select name="role" class="form-select">
                        <option value="student">Talaba</option>
                        <option value="teacher">O'qituvchi</option>
                    </select>
                </div>
                <button type="submit" class="btn btn-primary w-100">Ro'yxatdan o'tish</button>
            </form>
            <p class="text-center mt-3"><a href="/login/" class="text-info">Kirish</a></p>
        </div>
    </body>
    </html>
    """)


# ===================== LOGIN =====================
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
            if user.role == "admin": return redirect("/admin-panel/")
            elif user.role == "teacher": return redirect("/create/")
            else: return redirect("/test/")
        return HttpResponse("Login yoki parol noto'g'ri!")

    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Kirish</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>body { background: linear-gradient(135deg, #0f172a, #1e2937); color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center; }</style>
    </head>
    <body>
        <div class="card p-4 shadow" style="width: 420px; background: rgba(255,255,255,0.1);">
            <h2 class="text-center mb-4">Tizimga kirish</h2>
            <form method="post">
                <div class="mb-3"><input name="username" class="form-control" placeholder="Username" required></div>
                <div class="mb-3"><input name="password" type="password" class="form-control" placeholder="Parol" required></div>
                <button type="submit" class="btn btn-success w-100">Kirish</button>
            </form>
            <p class="text-center mt-3"><a href="/register/" class="text-info">Ro'yxatdan o'tish</a></p>
        </div>
    </body>
    </html>
    """)


# ===================== TEST TOPSHIRISH (Chiroyli) =====================
@csrf_exempt
@login_required
def take_test(request):
    test = Test.objects.last()
    if not test:
        return HttpResponse("<h2 class='text-center mt-5 text-white'>Hozircha test yo'q</h2>")

    questions = test.questions.all()

    if request.method == "POST":
        total = sum(grade_answer(request.POST.get(str(q.id), ""), q.correct_answer) for q in questions)
        score = round(total / len(questions), 2) if questions else 0
        Result.objects.create(test=test, score=score)

        return HttpResponse(f"""
        <div class="container mt-5 text-center text-white">
            <h1 class="display-4 text-success">Natija: {score}%</h1>
            <a href="/test/" class="btn btn-primary btn-lg mt-4">Yana topshirish</a>
            <a href="/logout/" class="btn btn-danger btn-lg mt-4">Chiqish</a>
        </div>
        """)

    html = f"""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{test.title}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>body {{ background: #0f172a; color: white; }}</style>
    </head>
    <body>
        <div class="container mt-5">
            <h2 class="text-center mb-4">{test.title}</h2>
            <form method="post">
                {''.join(f'''
                <div class="card mb-4 p-4 bg-dark border-secondary">
                    <h5>{q.text}</h5>
                    <input name="{q.id}" class="form-control mt-3" placeholder="Javobingiz..." required>
                </div>
                ''' for q in questions)}
                <button type="submit" class="btn btn-success btn-lg w-100">Natijani ko'rish</button>
            </form>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


# ===================== TEST YARATISH (Yaxshilangan) =====================
@csrf_exempt
@login_required
def create_test(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if not title:
            return HttpResponse("Test nomi majburiy!")

        test = Test.objects.create(title=title)
        # Bir nechta savol qo'shish imkoniyati (hozircha bitta, keyin kengaytiramiz)
        Question.objects.create(
            test=test,
            text=request.POST.get("question"),
            correct_answer=request.POST.get("correct")
        )
        return HttpResponse(f"Test yaratildi: {title} ✅ <br><a href='/create/'>Yana yaratish</a>")

    return HttpResponse("""
    <!DOCTYPE html>
    <html lang="uz">
    <head>
        <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Test yaratish</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>body { background: #0f172a; color: white; }</style>
    </head>
    <body>
        <div class="container mt-5">
            <h2>Test yaratish</h2>
            <form method="post" class="card p-4 bg-dark">
                <div class="mb-3"><input name="title" class="form-control" placeholder="Test nomi" required></div>
                <div class="mb-3"><input name="question" class="form-control" placeholder="Savol matni" required></div>
                <div class="mb-3"><input name="correct" class="form-control" placeholder="To'g'ri javob" required></div>
                <button type="submit" class="btn btn-primary w-100">Saqlash</button>
            </form>
            <a href="/logout/" class="btn btn-outline-danger mt-3">Chiqish</a>
        </div>
    </body>
    </html>
    """)


# Qolgan funksiyalar (logout_view, admin_panel, users_list, results_list, stats_view, create_admin) ni o'zgartirmasdan qoldiring.
# Agar ularni ham Bootstrap bilan chiroyli qilishni xohlasangiz — ayting.
