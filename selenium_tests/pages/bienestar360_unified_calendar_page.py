from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class Bienestar360UnifiedCalendarPage(BasePage):
    """Page Object for Bienestar360 Unified Calendar Page"""
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, 'h1')
    CALENDAR_GRID = (By.CSS_SELECTOR, '.calendar-grid, .calendar, table.calendar')
    CALENDAR_DAYS = (By.CSS_SELECTOR, '.calendar-day, .day, td.day')
    ACTIVITY_ITEMS = (By.CSS_SELECTOR, '.activity-item, .calendar-item, [data-type="Actividad"]')
    MONTH_NAVIGATION = (By.CSS_SELECTOR, '.month-navigation, .calendar-nav')
    NEXT_MONTH_BUTTON = (By.CSS_SELECTOR, '.next-month, [aria-label*="siguiente"], .nav-next')
    PREV_MONTH_BUTTON = (By.CSS_SELECTOR, '.prev-month, [aria-label*="anterior"], .nav-prev')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/activities/unified_calendar/"
    
    def navigate_to(self):
        """Navigate to the unified calendar page"""
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        import time
        time.sleep(1)  # Wait for calendar to render
    
    def is_calendar_displayed(self):
        """Check if the calendar is displayed"""
        try:
            # Wait a bit for calendar to render
            import time
            time.sleep(2)
            
            # Check for calendar grid specifically (this is the main calendar element)
            try:
                calendar_grid = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.calendar-grid'))
                )
                if calendar_grid.is_displayed():
                    return True
            except:
                pass
            
            # Check for calendar container
            try:
                calendar_container = self.driver.find_element(By.CSS_SELECTOR, '.calendar-container')
                if calendar_container.is_displayed():
                    return True
            except:
                pass
            
            # Check for calendar days
            try:
                calendar_days = self.driver.find_elements(*self.CALENDAR_DAYS)
                if len(calendar_days) > 0:
                    return True
            except:
                pass
            
            # Check for month navigation (present in unified calendar)
            try:
                month_nav = self.driver.find_element(By.CSS_SELECTOR, '.month-navigation')
                if month_nav.is_displayed():
                    return True
            except:
                pass
            
            # Also check if page contains calendar-related text
            page_text = self.driver.page_source.lower()
            if "calendario unificado" in page_text or "unified calendar" in page_text:
                return True
            
            return False
        except Exception as e:
            print(f"Error checking calendar display: {e}")
            return False
    
    def get_activity_items(self):
        """Get all activity items in the calendar"""
        try:
            # Try multiple selectors for calendar items
            selectors = [
                (By.CSS_SELECTOR, '.calendar-item'),
                (By.CSS_SELECTOR, '[class*="calendar-item"]'),
                (By.CSS_SELECTOR, '.day-items .calendar-item'),
                (By.XPATH, "//div[contains(@class, 'calendar-item')]"),
                (By.CSS_SELECTOR, '[data-type="Actividad"]'),
                (By.CSS_SELECTOR, '.activity-item'),
            ]
            
            for selector in selectors:
                try:
                    items = self.driver.find_elements(*selector)
                    if items:
                        return items
                except:
                    continue
            
            return []
        except:
            return []
    
    def get_activity_count(self):
        """Get the number of activities displayed in the calendar"""
        return len(self.get_activity_items())
    
    def get_activity_info(self, activity_item):
        """Get information from an activity item (name, category, location)"""
        try:
            item_text = activity_item.text
            
            # The calendar item structure is:
            # "Actividad: {name}"
            # "{time} - {location}"
            lines = item_text.split('\n')
            
            name = None
            category = None
            location = None
            time = None
            
            # Extract name from first line (format: "Actividad: {name}")
            if len(lines) > 0:
                first_line = lines[0]
                if ':' in first_line:
                    parts = first_line.split(':', 1)
                    category = parts[0].strip()
                    name = parts[1].strip() if len(parts) > 1 else first_line
                else:
                    name = first_line
            
            # Extract time and location from second line (format: "{time} - {location}")
            if len(lines) > 1:
                second_line = lines[1]
                if ' - ' in second_line:
                    parts = second_line.split(' - ', 1)
                    time = parts[0].strip()
                    location = parts[1].strip() if len(parts) > 1 else None
                else:
                    location = second_line.strip()
            
            return {
                'text': item_text,
                'name': name or item_text.split('\n')[0] if '\n' in item_text else item_text,
                'category': category or 'Actividad',
                'location': location,
                'time': time,
            }
        except Exception as e:
            print(f"Error getting activity info: {e}")
            return {
                'text': activity_item.text if hasattr(activity_item, 'text') else '',
                'name': None,
            }
    
    def has_activity_with_name(self, activity_name):
        """Check if calendar contains an activity with the given name"""
        activities = self.get_activity_items()
        for activity in activities:
            info = self.get_activity_info(activity)
            if info and activity_name.lower() in info['text'].lower():
                return True
        return False

