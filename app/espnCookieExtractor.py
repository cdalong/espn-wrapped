import requests
from urllib.parse import urlencode
import re
import json

class ESPNCookieExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_cookies(self, username, password):
        """
        Retrieve SWID and espn_s2 cookies from ESPN
        
        Args:
            username (str): ESPN username/email
            password (str): ESPN password
            
        Returns:
            dict: Dictionary containing 'swid' and 'espn_s2' cookies, or None if failed
        """
        try:
            # Step 1: Get the login page to extract any necessary tokens
            login_page_url = "https://registerdisney.go.com/jgc/v8/client/ESPN-ONESITE.WEB-PROD/guest/login"
            
            # Step 2: Prepare login data
            login_data = {
                'loginValue': username,
                'password': password
            }
            
            # Step 3: Attempt login
            login_response = self.session.post(
                login_page_url,
                data=login_data,
                allow_redirects=True
            )
            
            # Step 4: Check if login was successful by looking for redirect or success indicators
            if login_response.status_code == 200:
                # Try to access ESPN fantasy page to trigger cookie setting
                fantasy_url = "https://fantasy.espn.com/"
                fantasy_response = self.session.get(fantasy_url)
                
                # Extract cookies from session
                cookies = {}
                for cookie in self.session.cookies:
                    if cookie.name == 'SWID':
                        cookies['swid'] = cookie.value
                    elif cookie.name == 'espn_s2':
                        cookies['espn_s2'] = cookie.value
                
                if 'swid' in cookies and 'espn_s2' in cookies:
                    return cookies
                else:
                    print("Login may have failed - cookies not found")
                    return None
            else:
                print(f"Login request failed with status code: {login_response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error during cookie extraction: {str(e)}")
            return None
    
    def validate_cookies(self, swid, espn_s2):
        """
        Validate that the extracted cookies work by making a test API call
        
        Args:
            swid (str): SWID cookie value
            espn_s2 (str): espn_s2 cookie value
            
        Returns:
            bool: True if cookies are valid, False otherwise
        """
        try:
            test_url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leagues"
            
            cookies = {
                'SWID': swid,
                'espn_s2': espn_s2
            }
            
            response = requests.get(test_url, cookies=cookies)
            return response.status_code == 200
            
        except Exception as e:
            print(f"Cookie validation failed: {str(e)}")
            return False

# Usage example
if __name__ == "__main__":
    extractor = ESPNCookieExtractor()
    
    # Method 1: Automated extraction (may not always work due to ESPN's complex auth)
    username = "your_email@example.com"
    password = "your_password"
    
    print("Attempting automated cookie extraction...")
    cookies = extractor.get_cookies(username, password)
    
    if cookies:
        print("Successfully extracted cookies!")
        print(f"SWID: {cookies['swid']}")
        print(f"espn_s2: {cookies['espn_s2']}")
        
        # Validate the cookies
        if extractor.validate_cookies(cookies['swid'], cookies['espn_s2']):
            print("Cookies validated successfully!")
        else:
            print("Cookie validation failed - they may not be working correctly")
    else:
        print("Automated extraction failed.")
        print("\nTrying manual method instead:")
        get_cookies_manual_instructions()