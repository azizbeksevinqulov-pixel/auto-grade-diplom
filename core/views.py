from django.http import HttpResponse
from .utils import grade_answer

def test_page(request):
    if request.method == "POST":
        student = request.POST.get("answer")
        correct = "Python dasturlash tili"

        score = grade_answer(student, correct)

        return HttpResponse(f"""
        <body style="background:#0f172a;color:white;font-family:sans-serif;text-align:center;padding-top:100px;">
            <h1>Natija: {score}%</h1>
            <a href="/" style="color:#38bdf8;">⬅️ Orqaga</a>
        </body>
        """)

    return HttpResponse("""
    <body style="background:#0f172a;color:white;font-family:sans-serif;text-align:center;padding-top:100px;">
        <h2>Javob kiriting:</h2>

        <form method="post">
            <input type="text" name="answer"
                style="padding:10px;border-radius:8px;border:none;width:250px;" />
            <br><br>
            <button type="submit"
                style="padding:10px 20px;border:none;border-radius:8px;background:#38bdf8;color:black;font-weight:bold;">
                Tekshirish
            </button>
        </form>
    </body>
    """)
