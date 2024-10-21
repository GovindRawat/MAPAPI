import httpx
import logging


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger("APIClient")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def get(self, endpoint, params=None):
        try:
            # Configure the client to verify SSL certificates
            with httpx.Client(verify=False) as client:
                self.logger.info(f"Sending GET request to {self.base_url}{endpoint} with params {params}")
                response = client.get(f"{self.base_url}{endpoint}", params=params)
                response.raise_for_status()
                self.logger.info(f"Received response with status code {response.status_code}")
            return response
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}", exc_info=True)
            raise
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}", exc_info=True)
            raise
