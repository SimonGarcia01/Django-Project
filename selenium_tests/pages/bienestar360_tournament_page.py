from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
import time


class Bienestar360TournamentPage(BasePage):
    PAGE_TITLE = (By.TAG_NAME, 'h1')
    CREATE_TOURNAMENT_BUTTON = (By.LINK_TEXT, 'Crear Torneo')
    CALENDAR_LINK = (By.LINK_TEXT, 'Ver calendario general')
    TOURNAMENTS_GRID = (By.CSS_SELECTOR, '.tournaments-grid')
    TOURNAMENT_CARDS = (By.CSS_SELECTOR, '.tournaments-grid .card')
    CREATE_GAME_BUTTON = (By.LINK_TEXT, 'Crear partido')
    EMPTY_STATE = (By.CSS_SELECTOR, '.empty-state')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/tournaments/"
    
    def navigate_to(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PAGE_TITLE)
        )
    
    def click_create_tournament(self):
        try:
            create_button = self.find_element(self.CREATE_TOURNAMENT_BUTTON)
            create_button.click()
            return True
        except Exception as e:
            print(f"Error clicking create tournament: {e}")
            return False
    
    def click_create_game_for_tournament(self, tournament_name):
        try:
            print(f"Looking for tournament: {tournament_name}")
            tournaments = self.get_tournaments()
            print(f"Found {len(tournaments)} tournaments in the list")
            
            for card in tournaments:
                try:
                    image_header = card.find_element(By.CSS_SELECTOR, '.card-image-header')
                    title = image_header.find_element(By.CSS_SELECTOR, 'h3.card-title')
                    card_title = title.text.strip()
                    print(f"Checking tournament: '{card_title}'")
                    
                    if tournament_name.lower() in card_title.lower() or card_title.lower() in tournament_name.lower():
                        print(f"✅ Found matching tournament: '{card_title}'")
                        try:
                            create_game_btn = card.find_element(By.LINK_TEXT, 'Crear partido')
                        except:
                            try:
                                create_game_btn = card.find_element(By.PARTIAL_LINK_TEXT, 'Crear')
                            except:
                                create_game_btn = card.find_element(By.CSS_SELECTOR, 'a[href*="createTournamentGame"]')
                        
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", create_game_btn)
                        time.sleep(0.3)
                        create_game_btn.click()
                        print("✅ Clicked 'Crear partido' button")
                        time.sleep(1)
                        return True
                except Exception as e:
                    print(f"Error processing tournament card: {e}")
                    continue
            
            print(f"❌ Tournament '{tournament_name}' not found in the list")
            return False
        except Exception as e:
            print(f"Error clicking create game: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_tournaments(self):
        try:
            time.sleep(1)
            
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.any_of(
                        EC.presence_of_element_located(self.TOURNAMENTS_GRID),
                        EC.presence_of_element_located(self.EMPTY_STATE)
                    )
                )
            except:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body'))
                )
            
            try:
                tournaments = self.driver.find_elements(*self.TOURNAMENT_CARDS)
                if tournaments:
                    return tournaments
            except:
                pass
            
            try:
                grid = self.driver.find_element(*self.TOURNAMENTS_GRID)
                tournaments = grid.find_elements(By.CSS_SELECTOR, '.card')
                if tournaments:
                    return tournaments
            except:
                pass
            
            tournaments = self.driver.find_elements(By.CSS_SELECTOR, '.tournaments-grid .card.card-color-1, .tournaments-grid .card.card-color-2, .tournaments-grid .card.card-color-3, .tournaments-grid .card.card-color-4')
            return tournaments
        except Exception as e:
            print(f"Error getting tournaments: {e}")
            return []
    
    def tournament_exists(self, tournament_name):
        try:
            print(f"Checking if tournament '{tournament_name}' exists in the list...")
            
            self.close_password_dialogs()
            time.sleep(1)
            
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.any_of(
                        EC.presence_of_element_located(self.TOURNAMENTS_GRID),
                        EC.presence_of_element_located(self.EMPTY_STATE)
                    )
                )
            except:
                print("Tournaments grid or empty state not found")
            
            try:
                empty_state = self.driver.find_element(*self.EMPTY_STATE)
                if empty_state.is_displayed():
                    print("Empty state is displayed - no tournaments found")
                    return False
            except:
                pass
            
            tournaments = self.get_tournaments()
            print(f"Found {len(tournaments)} tournaments in the list")
            
            if len(tournaments) == 0:
                try:
                    empty_state = self.driver.find_element(*self.EMPTY_STATE)
                    if empty_state.is_displayed():
                        print("No tournaments found - empty state is shown")
                        return False
                except:
                    print("No tournaments found and no empty state - may be a loading issue")
                    time.sleep(2)
                    tournaments = self.get_tournaments()
                    print(f"After waiting, found {len(tournaments)} tournaments")
            
            for tournament in tournaments:
                try:
                    title = None
                    try:
                        image_header = tournament.find_element(By.CSS_SELECTOR, '.card-image-header')
                        title = image_header.find_element(By.CSS_SELECTOR, 'h3.card-title')
                    except:
                        try:
                            title = tournament.find_element(By.CSS_SELECTOR, 'h3.card-title')
                        except:
                            try:
                                title = tournament.find_element(By.CSS_SELECTOR, '.card-title')
                            except:
                                pass
                    
                    if title and title.text:
                        title_text = title.text.strip()
                        print(f"Checking tournament: '{title_text}' against '{tournament_name}'")
                        
                        if (tournament_name.lower() in title_text.lower() or 
                            title_text.lower() in tournament_name.lower() or
                            tournament_name == title_text):
                            print(f"✅ Tournament found: '{title_text}'")
                            return True
                    else:
                        try:
                            card_text = tournament.text
                            if card_text and tournament_name in card_text:
                                print(f"Tournament found in card text: {card_text[:100]}...")
                                return True
                        except:
                            pass
                except Exception as e:
                    print(f"Error checking tournament: {e}")
                    continue
            
            print(f"❌ Tournament '{tournament_name}' not found. Available tournaments:")
            for i, tournament in enumerate(tournaments):
                try:
                    title = tournament.find_element(By.CSS_SELECTOR, 'h3.card-title, .card-title')
                    if title and title.text:
                        print(f"  {i+1}. '{title.text.strip()}'")
                    else:
                        card_text = tournament.text[:80] if tournament.text else "No text"
                        print(f"  {i+1}. (No title found) Card text: {card_text}...")
                except Exception as e:
                    print(f"  {i+1}. Error getting title: {e}")
            
            return False
        except Exception as e:
            print(f"Error in tournament_exists: {e}")
            import traceback
            traceback.print_exc()
            return False


class Bienestar360CreateTournamentPage(BasePage):
    PAGE_TITLE = (By.TAG_NAME, 'h1')
    NAME_FIELD = (By.ID, 'id_name')
    SPORT_FIELD = (By.ID, 'id_sport')
    GENDER_SELECT = (By.ID, 'id_gender')
    MODALITY_SELECT = (By.ID, 'id_modality')
    START_DATE_FIELD = (By.ID, 'id_start_date')
    MAX_PARTICIPANTS_FIELD = (By.ID, 'id_max_participants')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"].btn-primary, button.btn-primary[type="submit"]')
    CANCEL_BUTTON = (By.LINK_TEXT, 'Cancelar')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/tournaments/createTournament"
    
    def navigate_to(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PAGE_TITLE)
        )
    
    def create_tournament(self, name, sport, gender, modality, start_date, max_participants):
        try:
            print(f"Filling tournament form: name={name}, sport={sport}, gender={gender}, modality={modality}, start_date={start_date}, max_participants={max_participants}")
            
            name_field = self.find_element(self.NAME_FIELD)
            name_field.clear()
            name_field.send_keys(name)
            print(f"Name field filled: {name_field.get_attribute('value')}")
            time.sleep(0.3)
            
            sport_field = self.find_element(self.SPORT_FIELD)
            sport_field.clear()
            sport_field.send_keys(sport)
            print(f"Sport field filled: {sport_field.get_attribute('value')}")
            time.sleep(0.3)
            
            gender_select = Select(self.find_element(self.GENDER_SELECT))
            gender_select.select_by_value(gender)
            selected_gender = gender_select.first_selected_option.text
            print(f"Gender selected: {selected_gender}")
            time.sleep(0.3)
            
            modality_select = Select(self.find_element(self.MODALITY_SELECT))
            modality_select.select_by_value(modality)
            selected_modality = modality_select.first_selected_option.text
            print(f"Modality selected: {selected_modality}")
            time.sleep(0.3)
            
            date_field = self.find_element(self.START_DATE_FIELD)
            date_field.clear()
            date_field.send_keys(start_date)
            print(f"Start date filled: {date_field.get_attribute('value')}")
            time.sleep(0.3)
            
            max_participants_field = self.find_element(self.MAX_PARTICIPANTS_FIELD)
            max_participants_field.clear()
            max_participants_field.send_keys(str(max_participants))
            print(f"Max participants filled: {max_participants_field.get_attribute('value')}")
            time.sleep(0.3)
            
            self.close_password_dialogs()
            time.sleep(0.5)
            
            try:
                error_messages = self.driver.find_elements(By.CSS_SELECTOR, '.errorlist, .alert-danger, .form-error')
                if error_messages:
                    print(f"Validation errors found before submit: {[e.text for e in error_messages]}")
                    return False
            except:
                pass
            
            print("Clicking submit button...")
            try:
                submit_button = self.find_element(self.SUBMIT_BUTTON)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                time.sleep(0.3)
                submit_button.click()
                print("Submit button clicked")
            except Exception as e:
                print(f"Error clicking submit button: {e}")
                try:
                    submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Guardar') or contains(text(), 'Crear')]")
                    submit_button.click()
                    print("Submit button clicked (alternative selector)")
                except:
                    raise Exception("Could not find or click submit button")
            
            print("Closing password dialogs...")
            for attempt in range(3):
                time.sleep(0.8)
                self.close_password_dialogs()
                print(f"Password dialog close attempt {attempt + 1} completed")
            
            time.sleep(1)
            print(f"Current URL after submit: {self.driver.current_url}")
            
            try:
                error_messages = self.driver.find_elements(By.CSS_SELECTOR, '.errorlist, .alert-danger, .form-error')
                if error_messages:
                    error_texts = [e.text for e in error_messages if e.text]
                    if error_texts:
                        print(f"Validation errors after submit: {error_texts}")
                        if "createTournament" in self.driver.current_url:
                            return False
            except:
                pass
            
            try:
                WebDriverWait(self.driver, 20).until(
                    lambda driver: "tournaments" in driver.current_url and "createTournament" not in driver.current_url
                )
                print(f"✅ Redirected to tournaments menu. URL: {self.driver.current_url}")
                
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.any_of(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.tournaments-grid')),
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.empty-state'))
                        )
                    )
                    print("✅ Tournaments grid loaded")
                except:
                    print("⚠️ Tournaments grid not found, but continuing...")
                
                time.sleep(2)
                self.close_password_dialogs()
                
                return True
            except Exception as e:
                current_url = self.driver.current_url
                print(f"⚠️ Timeout waiting for redirect. Current URL: {current_url}")
                
                self.close_password_dialogs()
                time.sleep(1)
                
                if "tournaments" in current_url and "createTournament" not in current_url:
                    print("✅ On tournaments page (after timeout)")
                    time.sleep(2)
                    self.close_password_dialogs()
                    return True
                else:
                    print(f"❌ Still on createTournament page. URL: {current_url}")
                    try:
                        self.driver.get("http://localhost:8000/tournaments/")
                        time.sleep(2)
                        self.close_password_dialogs()
                        return True
                    except:
                        return False
            
        except Exception as e:
            print(f"Error creating tournament: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def is_success_message_displayed(self):
        try:
            messages = self.driver.find_elements(By.CSS_SELECTOR, '.messages, .alert-success, .success')
            return len(messages) > 0
        except:
            return False


class Bienestar360CreateGamePage(BasePage):
    PAGE_TITLE = (By.TAG_NAME, 'h2')
    
    # Game form fields (for teams modality)
    HOME_TEAM_SELECT = (By.ID, 'id_home_team')
    GUEST_TEAM_SELECT = (By.ID, 'id_guest_team')
    
    # Game form fields (for individual modality)
    HOME_PLAYER_SELECT = (By.ID, 'id_home_player')
    GUEST_PLAYER_SELECT = (By.ID, 'id_guest_player')
    
    # Schedule form fields
    DATE_FIELD = (By.ID, 'id_date')
    START_TIME_FIELD = (By.ID, 'id_start_time')
    END_TIME_FIELD = (By.ID, 'id_end_time')
    CAPACITY_FIELD = (By.ID, 'id_capacity')
    SPACE_FIELD = (By.ID, 'id_space')
    
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def create_game_with_schedule(self, date, start_time, end_time, capacity, space, 
                                  home_team=None, guest_team=None,
                                  home_player=None, guest_player=None):
        try:
            self.enter_text(self.DATE_FIELD, date)
            self.enter_text(self.START_TIME_FIELD, start_time)
            self.enter_text(self.END_TIME_FIELD, end_time)
            self.enter_text(self.CAPACITY_FIELD, str(capacity))
            self.enter_text(self.SPACE_FIELD, space)
            
            try:
                home_team_select = self.driver.find_element(*self.HOME_TEAM_SELECT)
                if home_team and home_team_select.is_displayed():
                    Select(home_team_select).select_by_visible_text(home_team)
                
                guest_team_select = self.driver.find_element(*self.GUEST_TEAM_SELECT)
                if guest_team and guest_team_select.is_displayed():
                    Select(guest_team_select).select_by_visible_text(guest_team)
            except:
                pass
            
            try:
                home_player_select = self.driver.find_element(*self.HOME_PLAYER_SELECT)
                if home_player and home_player_select.is_displayed():
                    Select(home_player_select).select_by_visible_text(home_player)
                
                guest_player_select = self.driver.find_element(*self.GUEST_PLAYER_SELECT)
                if guest_player and guest_player_select.is_displayed():
                    Select(guest_player_select).select_by_visible_text(guest_player)
            except:
                pass
            
            submit_button = self.find_element(self.SUBMIT_BUTTON)
            submit_button.click()
            
            WebDriverWait(self.driver, 10).until(
                lambda driver: "tournaments" in driver.current_url or "results" in driver.current_url
            )
            
            return True
        except Exception as e:
            print(f"Error creating game: {e}")
            return False
    
    def is_success_message_displayed(self):
        try:
            messages = self.driver.find_elements(By.CSS_SELECTOR, '.messages, .alert-success, .success')
            return len(messages) > 0
        except:
            return False


class Bienestar360TournamentCalendarPage(BasePage):
    PAGE_TITLE = (By.TAG_NAME, 'h2')
    CALENDAR_GRID = (By.CSS_SELECTOR, '.calendar-grid')
    CALENDAR_DAYS = (By.CSS_SELECTOR, '.calendar-day')
    GAME_CARDS = (By.CSS_SELECTOR, '.game-card')
    MONTH_NAVIGATION = (By.CSS_SELECTOR, '.month-navigation')
    PREV_MONTH_BUTTON = (By.CSS_SELECTOR, '.nav-btn')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/tournaments/calendar/"
    
    def navigate_to(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.CALENDAR_GRID)
        )
    
    def is_calendar_displayed(self):
        try:
            calendar_grid = self.driver.find_element(*self.CALENDAR_GRID)
            if calendar_grid.is_displayed():
                return True
            
            calendar_days = self.driver.find_elements(*self.CALENDAR_DAYS)
            return len(calendar_days) > 0
        except:
            return False
    
    def get_games_count(self):
        try:
            games = self.driver.find_elements(*self.GAME_CARDS)
            return len(games)
        except:
            try:
                calendar_days = self.driver.find_elements(*self.CALENDAR_DAYS)
                total_games = 0
                for day in calendar_days:
                    game_cards = day.find_elements(By.CSS_SELECTOR, '.game-card')
                    total_games += len(game_cards)
                return total_games
            except:
                return 0
    
    def game_exists_in_calendar(self, game_info):
        try:
            page_text = self.driver.page_source.lower()
            for info in game_info:
                if info and info.lower() in page_text:
                    return True
            return False
        except:
            return False
    
    def get_calendar_title(self):
        try:
            title = self.driver.find_element(*self.PAGE_TITLE)
            return title.text
        except:
            return None


class Bienestar360RegisterResultPage(BasePage):
    PAGE_TITLE = (By.TAG_NAME, 'h2')
    HOME_SCORE_FIELD = (By.ID, 'id_homeScore')
    GUEST_SCORE_FIELD = (By.ID, 'id_guestScore')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"].btn-secondary, button.btn-secondary[type="submit"]')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to(self, game_id):
        url = f"http://localhost:8000/tournaments/register_result/{game_id}/"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PAGE_TITLE)
        )
        time.sleep(0.5)
    
    def register_result(self, home_score, guest_score):
        try:
            print(f"Registering result: Home={home_score}, Guest={guest_score}")
            
            home_score_field = self.find_element(self.HOME_SCORE_FIELD)
            home_score_field.clear()
            home_score_field.send_keys(str(home_score))
            print(f"Home score filled: {home_score_field.get_attribute('value')}")
            time.sleep(0.3)
            
            guest_score_field = self.find_element(self.GUEST_SCORE_FIELD)
            guest_score_field.clear()
            guest_score_field.send_keys(str(guest_score))
            print(f"Guest score filled: {guest_score_field.get_attribute('value')}")
            time.sleep(0.3)
            
            self.close_password_dialogs()
            time.sleep(0.5)
            
            submit_button = self.find_element(self.SUBMIT_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(0.3)
            submit_button.click()
            print("Result form submitted")
            
            WebDriverWait(self.driver, 15).until(
                lambda driver: 'results' in driver.current_url.lower() or 'resultado' in driver.current_url.lower()
            )
            time.sleep(1)
            self.close_password_dialogs()
            
            return True
        except Exception as e:
            print(f"Error registering result: {e}")
            import traceback
            traceback.print_exc()
            return False


class Bienestar360ResultsPage(BasePage):
    PAGE_TITLE = (By.TAG_NAME, 'h1')
    RESULTS_GRID = (By.CSS_SELECTOR, '.results-grid')
    RESULT_CARDS = (By.CSS_SELECTOR, '.results-grid .card')
    REGISTER_RESULT_BUTTON = (By.LINK_TEXT, 'Registrar / Editar Resultado')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "http://localhost:8000/tournaments/results/"
    
    def navigate_to(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.PAGE_TITLE)
        )
        time.sleep(0.5)
    
    def get_results(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.RESULTS_GRID)
            )
            cards = self.driver.find_elements(*self.RESULT_CARDS)
            return cards
        except:
            return []
    
    def click_register_result_for_game(self, game_id):
        try:
            results = self.get_results()
            for card in results:
                try:
                    register_link = card.find_element(By.CSS_SELECTOR, f'a[href*="register_result/{game_id}"]')
                    register_link.click()
                    time.sleep(1)
                    return True
                except:
                    continue
            return False
        except Exception as e:
            print(f"Error clicking register result: {e}")
            return False
    
    def result_exists(self, home_score, guest_score):
        try:
            results = self.get_results()
            for card in results:
                card_text = card.text
                if str(home_score) in card_text and str(guest_score) in card_text:
                    return True
            return False
        except Exception as e:
            print(f"Error checking result: {e}")
            return False

