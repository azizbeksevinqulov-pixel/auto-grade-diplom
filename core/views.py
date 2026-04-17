from django.http import HttpResponse
from .utils import grade_answer

def test_page(request):
    if request.method == "POST":
        student = request.POST.get("answer")
        correct = "Python dasturlash tili"

        score = grade_answer(student, correct)

        return HttpResponse(f"Natija: {score}%")

    return HttpResponse("""
        <h2>Javob kiriting:</h2>
        <form method="post">
            <input type="text" name="answer" />
            <button type="submit">Tekshirish</button>
        </form>
    """)
