# Multi-Server MCP Weather Assistant 🌤️🤖

מערכת בינה מלאכותית מתקדמת המבוססת על פרוטוקול **MCP (Model Context Protocol)**, המסוגלת לתקשר עם מספר שרתים במקביל כדי לספק נתוני מזג אוויר בזמן אמת מישראל ומארה"ב.

## 📋 סקירה כללית
הפרויקט מדגים שימוש ב-AI Agent כ-"Orchestrator" (מנצח) שמנהל אינטראקציה עם כלי קצה (Tools) שונים. המערכת יודעת לזהות את כוונת המשתמש, לבחור את השרת המתאים (ישראל או חו"ל), להפעיל דפדפן בצורה אוטונומית, לגרד נתונים ולהציג תחזית מעובדת.

## 🏗️ ארכיטקטורת המערכת
המערכת מורכבת משלושה שכבות עיקריות:

1.  **Client (The Host):** סקריפט Python (`host.py`) המנהל את התקשורת מול ה-LLM ומחבר בין השרתים.
2.  **MCP Servers:**
    * **Israel Weather Server:** שרת ייעודי המשתמש ב-Playwright/BeautifulSoup כדי לשלוף נתונים מאתר Weather2Day.
    * **USA Weather Server:** שרת המתממשק ל-API של שירות המטאורולוגיה הלאומי של ארה"ב (NWS).
3.  **LLM Engine:** שימוש במודל **Claude 3.5/4.5** של חברת Anthropic, המנתח את הכלים הזמינים ומחליט על סדר הפעולות.



## 🛠️ טכנולוגיות וכלים
* **שפת פיתוח:** Python 3.10+
* **פרוטוקול:** Model Context Protocol (MCP)
* **בינה מלאכותית:** Anthropic SDK (Claude 3.5 Sonnet / Claude 4.5)
* **ניהול חבילות:** `uv` (כלי מהיר במיוחד לניהול סביבות וירטואליות)
* **אוטומציה וגרידה:** Playwright (לדפדפן "בלתי נראה"), HTTPX, BeautifulSoup4
* **תשתית:** MCP SDK עבור Python

## 🚀 תכונות עיקריות
* **Multi-Server Routing:** המערכת מחברת בין שרתים שונים תחת ממשק אחד.
* **Real-time Web Scraping:** שליפת נתונים דינמית מאתרי אינטרנט ללא API רשמי.
* **Autonomous Decision Making:** המודל מחליט לבד באילו כלים להשתמש (למשל: פתיחת דף, הזנת עיר, קריאת תוכן).
* **Multi-Language Support:** תמיכה מלאה בתחזיות בעברית ובאנגלית.

## 🛠️ הגדרות והרצה

### דרישות קדם
1.  API Key של Anthropic (עם יתרה ב-Tier 1 לפחות).
2.  התקנת `uv`:
    ```bash
    powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
    ```

### התקנה
1.  שבטו את המאגר:
    ```bash
    git clone [repository-url]
    ```
2.  הגדירו את מפתח ה-API בקובץ הקוד או כמשתנה סביבה.

## 🔍 דוגמת הרצה (Usage Example)

### **User Query:**
> "What is the weather in Jerusalem?"

### **System Execution Log:**
```bash
# ה-Host מזהה את הצורך במידע מישראל ומתחבר לשרת המתאים
Connected to server: weather_Israel

# המודל מחליט על סדר פעולות אוטונומי:
[1] Calling: weather_Israel__open_weather_forecast_israel
[2] Calling: weather_Israel__enter_weather_forecast_city_israel(city="ירושלים")
[3] Calling: weather_Israel__get_weather_page_content

פותח על ידי רחלי במסגרת לימודי AI.






