# HirePilot AI - Simple Working Resume Analyzer

Yeh ek naya, simple project hai. Isme login/JWT ya Gemini API ki zaroorat nahi hai.
Resume PDF aur Job Description se basic keyword-match report banegi.

## Windows par run karne ke steps

1. ZIP extract karo.
2. Extract hue `HirePilot_AI_Fresh` folder ko VS Code mein kholo.
3. VS Code > Terminal > New Terminal.
4. Commands ek-ek karke chalao:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Agar PowerShell script activation block kare, to isi terminal mein yeh command chalao, phir activate dobara karo:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

5. Browser mein kholo: http://127.0.0.1:8000/
6. PDF resume select karo, job description paste karo, phir **Analyze Resume** dabao.

## Kya karta hai?

- PDF se selectable text extract karta hai.
- PDF 5 MB tak aur 20 pages tak allow karta hai.
- Job description ke common technical skills ko resume se compare karta hai.
- Match score, found skills aur missing skills dikhata hai.
- Koi paid API key nahi chahiye.

## Important

Yeh ATS ka official score nahi hai. Yeh simple keyword coverage estimate hai. Scanned/image-only PDF abhi support nahi hota.
