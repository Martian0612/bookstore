import os
from dotenv import load_dotenv
import requests
import logging
from requests.exceptions import HTTPError, Timeout, RequestException
from rest_framework import status

# Setting up basic/ default logging configuration
logging.basicConfig(filename = 'books_app.log', level= logging.INFO, format= '%(asctime)s - %(levelname)s - %(message)s')

# Loading environment variables from .env file
load_dotenv()

# Access the API key from environment
API_KEY = os.getenv('API_KEY')

# Fetch book data by ID
def get_book_info(book_id):
    url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"

    try:
        response = requests.get(url, timeout= 10)
        # Raise an HTTPError for bad responses (404 Not Found, 500 Server Error)-> use for handling errors before you proceed with processing the response.
        response.raise_for_status() 
        return response.json(), status.HTTP_200_OK
    
    # except HTTPError:
    #     logging.error(f"Failed to fetch book info for ID {book_id}. HTTP error occured.")
    #     return {"error": "We couldn't retrieve the book details at this moment. Please try again later. "} , status.HTTP_500_INTERNAL_SERVER_ERROR
    
    except HTTPError as e:
        logging.error(f"Failed to fetch book info for ID {book_id}. HTTP error: {e}")
        if e.response.status_code == 404:
            return {"error": "Book not found."}, status.HTTP_404_NOT_FOUND
        else:
            return {"error": "There was a problem retrieving the book information. Please try again later."}, status.HTTP_502_BAD_GATEWAY
        
    except Timeout:
        logging.error(f"Request timed out while fetching book info for ID {book_id}.")
        return {"error": "The request took too long to complete. Please check your connection and try again."} , status.HTTP_408_REQUEST_TIMEOUT
    
    # Base class for all exceptions raised by the 'requests' library. It includes network-related errors, invalid URLs,etc.
    except RequestException:
        logging.error(f"An error occured while fetching book info for ID {book_id}.")
        return {"error": "There was a problem connecting to the server. Please try again later."} , status.HTTP_503_SERVICE_UNAVAILABLE
    
    except ValueError:
        logging.error(f"Error parsing JSON response for book ID {book_id}.")
        return {"error": "There was an issue processing the book details. Please try again later."}, status.HTTP_422_UNPROCESSABLE_ENTITY
    
    except Exception:
        logging.error(f"Unexpected error occured while fetching book info for ID {book_id}.")
        return {"error": "An unexpected error occured. Please try again later."}, status.HTTP_500_INTERNAL_SERVER_ERROR
    
# Search books based on keywords, category, genre, etc.
def book_search(search_key):
    url = f"https://www.googleapis.com/books/v1/volumes?q={search_key}"

    try:
        response = requests.get(url, timeout = 10)
        response.raise_for_status()
        return response.json(), status.HTTP_200_OK
    
    except HTTPError as e:
        logging.error(f"Failed to search books with keyword'{search_key}'. HTTP error: {e}.")
        if e.response.status_code == 404:
            return {"error": "Books not found."}, status.HTTP_404_NOT_FOUND
        # issue in retrieving books from server.
        else:
            return {"error": "There was a problem in retrieving the books. Please try again later."}, status.HTTP_502_BAD_GATEWAY
            
    except Timeout:
        logging.error(f"Request timed out during book search with keyword '{search_key}'.")
        return {"error":"The request took too long to complete. Please check your connection and try again."} , status.HTTP_408_REQUEST_TIMEOUT
    
    except RequestException:
        logging.error(f"An error occured during book search with keyword '{search_key}'.")
        return {"error":"There was a problem connecting to the server. Please try again later."} , status.HTTP_503_SERVICE_UNAVAILABLE

    except ValueError:
        logging.error(f"Error parsing JSON response during book search with keyword '{search_key}'.")
        return {"error": "There was an issue processing the search results. Please try again later."}, status.HTTP_422_UNPROCESSABLE_ENTITY
    
    except Exception:
        logging.error(f"Unexpected error occured during book search with keyword '{search_key}'")
        return {"error": "An unexpected error occurred. Please try again later."}, status.HTTP_500_INTERNAL_SERVER_ERROR