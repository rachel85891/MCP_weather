from typing import Any
from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright, Browser, Page, Playwright

# יצירת מופע MCP
mcp = FastMCP("weather-Israel")

# משתנים גלובליים לשמירת מופע הדפדפן והעמוד פתוחים בין קריאות
_playwright: Playwright | None = None
_browser: Browser | None = None
_page: Page | None = None

async def init_browser(headless: bool = True):
    """מאתחל את הדפדפן במידה והוא עדיין לא פתוח"""
    global _playwright, _browser, _page
    if _playwright is None:
        _playwright = await async_playwright().start()
        _browser = await _playwright.chromium.launch(headless=headless)
        _page = await _browser.new_page()

@mcp.tool()
async def open_weather_forecast_israel() -> str:
    """פותח דפדפן ומנווט לעמוד התחזית באתר weather2day"""
    global _page
    try:
        # אתחול הדפדפן (headless=True כברירת מחדל, ניתן לשנות ל-False במידת הצורך)
        await init_browser(headless=True)
        
        if _page is not None:
            await _page.goto("https://www.weather2day.co.il/forecast", timeout=30000)
            return "האתר נפתח בהצלחה."
        return "שגיאה: לא ניתן היה ליצור עמוד דפדפן חדש."
    except Exception as e:
        return f"שגיאה בפתיחת האתר: {str(e)}"

@mcp.tool()
async def enter_weather_forecast_city_israel(city: str) -> str:
    """מזין שם של עיר בתיבת החיפוש באתר
    
    Args:
        city: שם העיר בישראל בעברית (לדוגמה: תל אביב)
    """
    global _page
    if _page is None:
        return "שגיאה: הדפדפן אינו פתוח. אנא קרא לכלי open_weather_forecast_israel תחילה."
    
    try:
        # איתור תיבת החיפוש (לפי סוג קלט נפוץ או שם השדה)
        search_input = _page.locator('input[type="text"], input[type="search"]').first
        await search_input.fill(city)
        
        # המתנה קלה כדי לאפשר לרשימה הנפתחת (Dropdown) להיטען
        await _page.wait_for_timeout(1000)
        return f"העיר '{city}' הוזנה בהצלחה בתיבת החיפוש."
    except Exception as e:
        return f"שגיאה בהזנת שם העיר: {str(e)}"

@mcp.tool()
async def select_weather_forecast_city_israel() -> str:
    """בוחר את הפריט הראשון מתוך הרשימה הנפתחת ומקליק עליו למעבר לעמוד התחזית"""
    global _page
    if _page is None:
        return "שגיאה: הדפדפן אינו פתוח. אנא קרא לכלי open_weather_forecast_israel תחילה."
    
    try:
        # איתור הפריט הראשון ברשימת ההשלמה האוטומטית
        dropdown_item = _page.locator(
            ".autocomplete-suggestions > div, .autocomplete-suggestion, .ui-menu-item, .search-results a, [role='option']"
        ).first
        
        # אם הסלקטור הראשון לא נמצא, נשתמש בטכניקת מקלדת כגיבוי (חץ למטה ואנטר)
        if await dropdown_item.count() > 0:
            await dropdown_item.click()
        else:
            search_input = _page.locator('input[type="text"], input[type="search"]').first
            await search_input.press("ArrowDown")
            await _page.wait_for_timeout(500)
            await search_input.press("Enter")
        
        # המתנה לטעינת דף התחזית של העיר שנבחרה
        await _page.wait_for_load_state("networkidle", timeout=15000)
        return "העיר נבחרה בהצלחה ודף התחזית נטען."
    except Exception as e:
        return f"שגיאה בבחירת העיר מהרשימה: {str(e)}"

@mcp.tool()
async def get_weather_page_content() -> str:
    """שולף את המידע מטקסט הדף הפתוח כעת ומנקה אותו מרווחים ותגיות מיותרות עבור ה-LLM"""
    global _page
    if _page is None:
        return "שגיאה: הדפדפן אינו פתוח. אנא קרא לכלי open_weather_forecast_israel תחילה."

    try:
        # שליפת הטקסט הגלוי מתוך גוף העמוד.
        # המתודה inner_text מסננת אוטומטית תגיות script, style ו-HTML ומחזירה רק טקסט נקי.
        raw_text = await _page.locator("body").inner_text()

        # ניקוי שורות ריקות מרובות ורווחים מיותרים כדי לשמור על קונטקסט קריא וממוקד
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        cleaned_text = "\n".join(lines)

        if not cleaned_text:
            return "לא נמצא תוכן טקסטואלי בעמוד."

        return cleaned_text
    except Exception as e:
        return f"שגיאה בחילוץ תוכן העמוד: {str(e)}"

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()