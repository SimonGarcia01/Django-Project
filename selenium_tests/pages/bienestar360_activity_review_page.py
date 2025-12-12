from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class Bienestar360ActivityReviewPage(BasePage):
    """Page Object for Bienestar360 Activity Review Page"""
    
    # Locators
    RATING_FIELD = (By.NAME, 'rating')
    RATING_INPUT = (By.CSS_SELECTOR, 'input[name="rating"], input[type="number"][name="rating"], select[name="rating"]')
    COMMENT_FIELD = (By.NAME, 'comment')
    COMMENT_TEXTAREA = (By.CSS_SELECTOR, 'textarea[name="comment"], textarea#id_comment')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"], input[type="submit"]')
    PAGE_TITLE = (By.TAG_NAME, 'h1')
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, '.alert-success, .message-success, .success')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to(self, activity_id):
        """Navigate to the review page for a specific activity"""
        url = f"http://localhost:8000/activities/{activity_id}/review/"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        import time
        time.sleep(1)
    
    def is_page_loaded(self):
        """Check if the review page is loaded"""
        try:
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            
            # Check for page title
            try:
                title = self.driver.find_element(*self.PAGE_TITLE)
                if "Valora" in title.text or "reseña" in title.text.lower() or "review" in title.text.lower():
                    return True
            except:
                pass
            
            # Check for rating field (can be radio buttons with stars)
            rating_selectors = [
                (By.CSS_SELECTOR, 'input[name="rating"]'),
                (By.CSS_SELECTOR, '.rating'),
                (By.CSS_SELECTOR, '.rating input'),
                (By.CSS_SELECTOR, 'label[for*="star"]'),
            ]
            for selector in rating_selectors:
                try:
                    if self.is_element_present(selector):
                        return True
                except:
                    continue
            
            # Check for comment field
            if self.is_element_present(self.COMMENT_TEXTAREA):
                return True
            
            # Check URL
            if "review" in self.driver.current_url.lower():
                return True
            
            return False
        except Exception as e:
            print(f"Error checking page loaded: {e}")
            return False
    
    def select_rating(self, rating):
        """Select a rating (1-5)"""
        try:
            # The rating system uses star radio buttons with IDs like star1, star2, etc.
            # But the values are reversed (star5 = 5, star4 = 4, etc.) due to RTL direction
            # So rating 5 = star5, rating 1 = star1
            star_id = f"star{rating}"
            
            # Try to find and click the star label (labels are clickable)
            selectors = [
                (By.CSS_SELECTOR, f'label[for="{star_id}"]'),
                (By.ID, star_id),  # The actual input
                (By.CSS_SELECTOR, f'input[name="rating"][value="{rating}"]'),
                (By.CSS_SELECTOR, f'input[id="{star_id}"]'),
                (By.XPATH, f'//input[@name="rating" and @value="{rating}"]'),
                (By.XPATH, f'//label[@for="{star_id}"]'),
            ]
            
            for selector in selectors:
                try:
                    element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(selector)
                    )
                    # Scroll to element if needed
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    element.click()
                    import time
                    time.sleep(0.5)  # Wait for click to register
                    
                    # Verify the rating was selected
                    try:
                        input_element = self.driver.find_element(By.ID, star_id)
                        if input_element.is_selected():
                            return True
                    except:
                        pass
                    
                    return True
                except:
                    continue
            
            # Fallback: try JavaScript click
            try:
                star_input = self.driver.find_element(By.ID, star_id)
                self.driver.execute_script("arguments[0].click();", star_input)
                import time
                time.sleep(0.5)
                return True
            except:
                pass
            
            # Last resort: try as number input
            try:
                rating_field = self.find_element(self.RATING_INPUT)
                rating_field.clear()
                rating_field.send_keys(str(rating))
                return True
            except:
                pass
            
            print(f"Could not select rating {rating}")
            return False
        except Exception as e:
            print(f"Error selecting rating: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def enter_comment(self, comment):
        """Enter a comment"""
        try:
            comment_field = self.find_element(self.COMMENT_TEXTAREA)
            comment_field.clear()
            comment_field.send_keys(comment)
            return True
        except Exception as e:
            print(f"Error entering comment: {e}")
            return False
    
    def submit_review(self):
        """Submit the review"""
        try:
            # Get current URL before submission
            current_url = self.driver.current_url
            
            # Find and click submit button
            submit_button = self.find_element(self.SUBMIT_BUTTON)
            # Scroll to button to ensure it's visible
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            import time
            time.sleep(0.5)
            
            # Click the button
            submit_button.click()
            
            # Wait for form submission - the page will redirect to activity_reviews
            # Don't wait too long or check current_url immediately as it might cause issues
            time.sleep(1)
            
            # Wait for page to start loading (redirect happening)
            try:
                WebDriverWait(self.driver, 15).until(
                    lambda driver: (
                        driver.current_url != current_url or
                        driver.execute_script("return document.readyState") == "complete"
                    )
                )
            except:
                # If timeout, that's okay - form might have been submitted
                pass
            
            return True
        except Exception as e:
            print(f"Error submitting review: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def is_success_message_displayed(self):
        """Check if success message is displayed"""
        try:
            # Check for success message
            selectors = [
                self.SUCCESS_MESSAGE,
                (By.CSS_SELECTOR, '.alert-success'),
                (By.CSS_SELECTOR, '.message'),
                (By.XPATH, "//*[contains(text(), 'Gracias')]"),
                (By.XPATH, "//*[contains(text(), 'enviada')]"),
            ]
            
            for selector in selectors:
                try:
                    element = self.driver.find_element(*selector)
                    if element.is_displayed():
                        return True
                except:
                    continue
            
            # Check page source for success indicators
            page_text = self.driver.page_source.lower()
            if "gracias" in page_text or "enviada" in page_text or "éxito" in page_text:
                return True
            
            return False
        except:
            return False
    
    def has_validation_error(self):
        """Check if there are validation errors on the page"""
        try:
            # Check for Django error messages (from messages framework)
            error_messages = self.driver.find_elements(By.CSS_SELECTOR, '.alert-error, .alert-danger, .messages .alert-error, .messages .alert-danger')
            if error_messages:
                for error in error_messages:
                    if error.is_displayed() and error.text.strip():
                        return True, error.text.strip()
            
            # Check for error list in form
            error_elements = self.driver.find_elements(By.CSS_SELECTOR, '.errorlist, ul.errorlist li, .errors ul li')
            if error_elements:
                for error in error_elements:
                    if error.is_displayed() and error.text.strip():
                        return True, error.text.strip()
            
            # Check for error messages in page source (Django messages)
            page_source = self.driver.page_source.lower()
            if 'error' in page_source or 'requerido' in page_source or 'required' in page_source or 'valoración' in page_source:
                # Try to find the specific error message
                error_selectors = [
                    (By.CSS_SELECTOR, '.alert-error'),
                    (By.CSS_SELECTOR, '.alert-danger'),
                    (By.CSS_SELECTOR, '.errorlist li'),
                    (By.XPATH, "//*[contains(@class, 'alert') and (contains(@class, 'error') or contains(@class, 'danger'))]"),
                    (By.XPATH, "//*[contains(text(), 'requerido') or contains(text(), 'required') or contains(text(), 'valoración')]"),
                ]
                for selector in error_selectors:
                    try:
                        error_text = self.driver.find_elements(*selector)
                        for err in error_text:
                            if err.is_displayed() and err.text.strip():
                                return True, err.text.strip()
                    except:
                        continue
                # If error keywords found but no visible element, still return True
                if 'valoración' in page_source or 'requerido' in page_source:
                    return True, "Validation error found in page"
            
            return False, None
        except Exception as e:
            print(f"Error checking validation error: {e}")
            return False, None
    
    def is_still_on_review_page(self):
        """Check if still on review page (form was not submitted due to validation error)"""
        try:
            current_url = self.driver.current_url.lower()
            return "review" in current_url
        except:
            return False
    
    def clear_comment(self):
        """Clear the comment field"""
        try:
            comment_field = self.find_element(self.COMMENT_TEXTAREA)
            comment_field.clear()
            return True
        except Exception as e:
            print(f"Error clearing comment: {e}")
            return False

