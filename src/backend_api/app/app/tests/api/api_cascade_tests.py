import pytest

from app.tests.api.api_test_base import TestAPI


@pytest.mark.usefixtures("clear_db", autouse=True)
class CascadeTestAPI(TestAPI):
    pass