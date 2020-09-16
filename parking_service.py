from base import Base
from api_handler import ApiHandler
from content_handler import ContentHandler
from db_handler import DateBaseHandler


class ParkingService(Base):
    def __init__(self):
        super(ParkingService, self).__init__()
        self._api_handler = ApiHandler()
        self._content_handler = ContentHandler()
        # db_handler is public for testing purpose
        self.db_handler = DateBaseHandler()

    # TODO: implement functionality for multiple images
    def check_plate(self, image_name):
        response = self._api_handler.post_by_file_name(image_name)
        text = self._content_handler.get_parsed_text(response)

        is_allowed = not self._is_transport_with_no_letters(text) and \
            not self._is_public_transport(text) and \
            not self._is_military_transport(text)

        self._store_result(text, is_allowed)
        self.debug_info('Plate', text)
        self._print_result(is_allowed)

        # Returning text and status for testing purpose
        return [text, is_allowed]

    def set_wrong_api_url(self):
        """
        For testing purpose ONLY
        """
        self._api_handler = ApiHandler(api_url='https://api.ocr.space/parse/imageasd')

    def _is_public_transport(self, text):
        last_symbol = text[-1]
        return last_symbol == 'G' or last_symbol == '6'

    def _is_military_transport(self, text):
        return 'L' in text or 'M' in text

    def _is_transport_with_no_letters(self, text):
        return text.isdecimal()

    def _store_result(self, plate, is_allowed):
        if is_allowed:
            status = 'allowed'
        else:
            status = 'rejected'
        self.db_handler.store_plate_info(plate, status)

    def _print_result(self, is_allowed):
        if is_allowed:
            print('You may park here')
            return

        print('YOU SHALL NOT PASS')
