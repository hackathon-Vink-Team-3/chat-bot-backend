import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_api(api_client):
   assert 1 == 1
