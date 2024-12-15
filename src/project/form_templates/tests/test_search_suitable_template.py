import requests
from fastapi import status
import pytest


def test_get_suitable_form_1():
    form_data = {
        "first_name": "Igor",
        "email": "rud@mail.ru"
    }
    response = requests.post(
        "http://0.0.0.0:8080/get_form",
        json=form_data
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"name": "User Form"}


def test_get_suitable_form_2():
    form_data = {
        "first_name": "Igor",
        "email": "rud@mail.ru",
        "phone_number": "+79261353789",
        "NOT_VALID_last_vizit": "11.12.2024"
    }

    response = requests.post(
        "http://0.0.0.0:8080/get_form",
        json=form_data
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"name": "User Form"}


def test_get_suitable_form_3():
    form_data = {
        "first_name": "Igor",
        "email": "rud@mail.ru",
        "phone_number": "+79261353789",
        "last_vizit": "11.12.2024"
    }

    response = requests.post(
        "http://0.0.0.0:8080/get_form",
        json=form_data
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"name": "Customer Form"}


def test_get_suitable_form_4():
    form_data = {
        "first_name": "Igor",
        "email": "rud@mail.ru",
        "phone_number": "+79261353789",
        "last_vizit": "2024-11-12"
    }

    response = requests.post(
        "http://0.0.0.0:8080/get_form",
        json=form_data
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"name": "Customer Form"}


def test_get_not_suitable_form_1():
    form_data = {
        "first_name": "Igor",
    }
    response = requests.post(
        "http://0.0.0.0:8080/get_form",
        json=form_data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"first_name": "text"}


def test_get_not_suitable_form_2():
    form_data = {
        "first_name": "Igor",
        "email": "invalid email"
    }
    response = requests.post(
        "http://0.0.0.0:8080/get_form",
        json=form_data
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "first_name": "text",
        "email": "text"
    }


def test_incorrect_request_data():
    form_data = {
        "first_name": "Igor",
        "email": 1
    }
    response = requests.post(
        "http://0.0.0.0:8080/get_form",
        json=form_data
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
