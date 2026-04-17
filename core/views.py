from django.http import HttpResponse
from .utils import grade_answer

def test_page(request):
    student_answer = "Python bu dasturlash tili"
    correct_answer = "Python dasturlash tili hisoblanadi"

    score = grade_answer(student_answer, correct_answer)

    return HttpResponse(f"Natija: {score}%")
