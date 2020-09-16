import json

from base import Base


class ContentHandler(Base):
    def __init__(self):
        super(ContentHandler, self).__init__()
        self.success_exit_code = 1

    def _get_parsed_result(self, result):
        result = result.content.decode()
        json_data = json.loads(result)
        self.debug_info('json data', json_data)
        if self._has_parsing_error(json_data):
            error = self._get_parsing_error(json_data)
            raise Exception('Content error. Details: {}'.format(error))

        content = json_data['ParsedResults'][0]
        return content

    def _has_parsing_error(self, content):
        return content['OCRExitCode'] != self.success_exit_code

    @staticmethod
    def _get_parsing_error(content):
        return {
            'exit_code': content['OCRExitCode'],
            'message': content['ErrorMessage']
        }

    def _get_text(self, result):
        return result['ParsedText']

    def get_parsed_text(self, content):
        result = self._get_parsed_result(content)
        text = self._get_text(result)
        if text == '':
            raise Exception('Text is not extracted')

        return self._get_plate_number(text)

    @staticmethod
    def _get_plate_number(text):
        text_lines = text.split("\r\n")
        for line in text_lines:
            # Simple plate number verification, certainly should be improved
            if len(line) == 7:
                return line

        raise Exception('Could not identify plate number due to multiple text lines')
