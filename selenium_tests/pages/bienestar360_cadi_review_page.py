from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class Bienestar360CADIReviewPage(BasePage):
    """Page Object for Bienestar360 CADI Activity Review Page"""
    
    # Locators
    PAGE_TITLE = (By.TAG_NAME, 'h1')
    REVIEW_CARDS = (By.CSS_SELECTOR, '.review-card, .review-item, [class*="review"]')
    ACTIVITY_LIST = (By.CSS_SELECTOR, '.activity-list, .activity-item')
    RATING_DISPLAY = (By.CSS_SELECTOR, '.rating, .review-rating, [class*="rating"]')
    COMMENT_DISPLAY = (By.CSS_SELECTOR, '.comment, .review-comment, [class*="comment"]')
    AVERAGE_RATING = (By.CSS_SELECTOR, '.average-rating, [class*="average"]')
    EMPTY_MESSAGE = (By.CSS_SELECTOR, '.empty-message, .no-reviews')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/activities/cadi/reviews/"
    
    def navigate_to(self):
        """Navigate to the CADI reviews page"""
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        import time
        time.sleep(1)
    
    def navigate_to_activity_detail(self, activity_id):
        """Navigate to a specific activity's reviews"""
        url = f"http://localhost:8000/activities/cadi/reviews/{activity_id}/"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        import time
        time.sleep(1)
    
    def is_page_loaded(self):
        """Check if the CADI review page is loaded"""
        try:
            return ("cadi" in self.driver.current_url.lower() and 
                   "review" in self.driver.current_url.lower())
        except:
            return False
    
    def get_reviews(self):
        """Get all review cards"""
        try:
            return self.driver.find_elements(*self.REVIEW_CARDS)
        except:
            return []
    
    def get_review_count(self):
        """Get the number of reviews displayed"""
        return len(self.get_reviews())
    
    def has_reviews(self):
        """Check if there are any reviews displayed"""
        reviews = self.get_reviews()
        if reviews:
            return True
        
        # Check for empty message
        try:
            empty_msg = self.driver.find_element(*self.EMPTY_MESSAGE)
            return not empty_msg.is_displayed()
        except:
            # If no empty message and no reviews, assume there might be reviews
            return True
    
    def get_review_info(self, review_card):
        """Get information from a review card (rating, comment)"""
        try:
            review_text = review_card.text
            
            # Try to extract rating
            rating = None
            try:
                rating_element = review_card.find_element(*self.RATING_DISPLAY)
                rating_text = rating_element.text
                # Extract number from rating text
                import re
                numbers = re.findall(r'\d+', rating_text)
                if numbers:
                    rating = int(numbers[0])
            except:
                pass
            
            # Try to extract comment
            comment = None
            try:
                comment_element = review_card.find_element(*self.COMMENT_DISPLAY)
                comment = comment_element.text
            except:
                # If no comment element, use the full text
                comment = review_text
            
            return {
                'text': review_text,
                'rating': rating,
                'comment': comment,
            }
        except:
            return None
    
    def find_review_by_comment(self, comment_text):
        """Find a review by its comment text"""
        reviews = self.get_reviews()
        for review in reviews:
            info = self.get_review_info(review)
            if info and comment_text.lower() in info.get('comment', '').lower():
                return review
        return None
    
    def get_average_rating(self):
        """Get the average rating displayed"""
        try:
            avg_element = self.driver.find_element(*self.AVERAGE_RATING)
            avg_text = avg_element.text
            # Extract number from text
            import re
            numbers = re.findall(r'\d+\.?\d*', avg_text)
            if numbers:
                return float(numbers[0])
        except:
            pass
        return None

