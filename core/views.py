from django.http import HttpResponse
from .utils import grade_answer

def test_page(request):
    if request.method == "POST":
        student = request.POST.get("answer")
        correct = "Python dasturlash tili"
        score = grade_answer(student, correct)

        return HttpResponse(f"""
        <html>
        <head>
        <style>
            body {{
                background: var(--bg);
                color: var(--text);
                font-family: sans-serif;
                text-align:center;
                padding-top:100px;
                transition:0.3s;
            }}
            button {{
                padding:10px 20px;
                border:none;
                border-radius:8px;
                background:#38bdf8;
                cursor:pointer;
            }}
        </style>
        </head>

        <body>
            <h1>Natija: {score}%</h1>
            <button onclick="toggleMode()">🌗 Toggle</button>
            <br><br>
            <a href="/">⬅️ Orqaga</a>

        <script>
            function toggleMode() {{
                document.body.classList.toggle("light");
                if(document.body.classList.contains("light")) {{
                    document.body.style.setProperty('--bg', 'white');
                    document.body.style.setProperty('--text', 'black');
                }} else {{
                    document.body.style.setProperty('--bg', '#0f172a');
                    document.body.style.setProperty('--text', 'white');
                }}
            }}

            // default dark
            document.body.style.setProperty('--bg', '#0f172a');
            document.body.style.setProperty('--text', 'white');
        </script>
        </body>
        </html>
        """)

    return HttpResponse("""
    <html>
    <head>
    <style>
        body {
            background: var(--bg);
            color: var(--text);
            font-family: sans-serif;
            text-align:center;
            padding-top:100px;
        }

        input {
            padding:10px;
            border-radius:8px;
            border:none;
            width:250px;
        }

        button {
            padding:10px 20px;
            border:none;
            border-radius:8px;
            background:#38bdf8;
            cursor:pointer;
        }
    </style>
    </head>

    <body>

    <h2>Javob kiriting:</h2>

    <form method="post">
        <input type="text" name="answer" />
        <br><br>
        <button type="submit">Tekshirish</button>
    </form>

    <br>
    <button onclick="toggleMode()">🌗 Toggle</button>

    <script>
        function toggleMode() {
            document.body.classList.toggle("light");

            if(document.body.classList.contains("light")){
                document.body.style.setProperty('--bg', 'white');
                document.body.style.setProperty('--text', 'black');
            } else {
                document.body.style.setProperty('--bg', '#0f172a');
                document.body.style.setProperty('--text', 'white');
            }
        }

        document.body.style.setProperty('--bg', '#0f172a');
        document.body.style.setProperty('--text', 'white');
    </script>

    </body>
    </html>
    """)
