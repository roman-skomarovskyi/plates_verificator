import requests
import os

from base import Base


dirname = os.path.dirname(__file__)


class ApiHandler(Base):
    def __init__(self, custom_params=None, api_url=None):
        super(ApiHandler, self).__init__()
        self._params = {
            'apikey': '7983d3111188957',
            'isOverlayRequired': False,
            'scale': True
        }
        if custom_params is not None:
            # TODO: implement params verification
            self._params.update()

        self._images_location = dirname + '/images/'
        if not api_url:
            self._api_url = 'https://api.ocr.space/parse/image'
        else:
            self._api_url = api_url

    # TODO: implement logic for url and base64 format
    def post_by_file_name(self, image_name):
        filename = self._images_location + image_name
        with open(filename, 'rb') as f:
            result = requests.post(
                        self._api_url,
                        files={filename: f},
                        data=self._params,
                    )
        self.debug_info('Response', result.text)
        if not self.is_request_successful(result):
            # TODO: Print details
            raise Exception('Error with request. Status code {}'.format(result.status_code))

        return result

    @staticmethod
    def is_request_successful(response):
        return response.status_code == 200
