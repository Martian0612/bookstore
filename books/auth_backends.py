import logging
from social_core.backends.google import GoogleOAuth2

class CustomGoogleOAuth2(GoogleOAuth2):
    def request(self, url, *args, **kwargs):
        logging.info(f"Requesting URL: {url}")
        logging.info(f"Request parameters: {kwargs.get('params')}")
        logging.info(f"Request headers: {kwargs.get('headers')}")

        response = super().request(url, *args, **kwargs)

        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response content: {response.text}")

        if response.status_code !=200:
            logging.error(f"Error during Google OAuth: {response.status_code} {response.text}")

        return response








