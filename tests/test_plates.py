import pytest
import os
import inspect
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from parking_service import ParkingService


@pytest.fixture(scope='module')
def service():
    service = ParkingService()
    service.db_handler.create_connection()
    yield service
    service.db_handler.clear_table()
    service.db_handler.close_connection()


def test_positive_case(service):
    result = service.check_plate('2.jpeg')
    assert result[0] == '5AOJZ30'  # mistake in text recognition
    assert result[1] is True


def test_wrong_image_format(service):
    with pytest.raises(Exception):
        service.check_plate('1.docx')


def test_bad_resolution(service):
    with pytest.raises(Exception):
        service.check_plate('0.png')


def test_no_letters_case(service):
    result = service.check_plate('4.jpg')
    assert result[0] == '1097395'
    assert result[1] is False


def test_ending_on_6_symbol(service):
    result = service.check_plate('5.jpg')
    assert result[0] == '5ZZROL6'  # mistake in text recognition
    assert result[1] is False


def test_has_m_letter(service):
    result = service.check_plate('3.jpg')
    assert result[0] == '6SAM123'
    assert result[1] is False


def test_check_db_storage(service):
    # checks that 4 results (with no Exception thrown) from previous tests are stored inside db
    data = service.db_handler.select_all_results()
    assert len(data) == 4


def test_api_request_status_is_not_200(service):
    service.set_wrong_api_url()
    with pytest.raises(Exception):
        service.check_plate('2.jpeg')
