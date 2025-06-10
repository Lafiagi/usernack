import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from pizza.models import Pizza, Extra, Order


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def pizza():
    return Pizza.objects.create(
        name="Margherita", base_price=10.0, quantity_in_stock=5, is_available=True
    )


@pytest.fixture
def extras():
    return [
        Extra.objects.create(
            name="Cheese", price=2.0, quantity_in_stock=5, is_available=True
        ),
        Extra.objects.create(
            name="Olives", price=1.5, quantity_in_stock=5, is_available=True
        ),
    ]


@pytest.mark.django_db
def test_list_pizzas(client, pizza):
    url = reverse("pizza-list")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["name"] == pizza.name


@pytest.mark.django_db
def test_retrieve_pizza(client, pizza):
    url = reverse("pizza-detail", args=[pizza.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == pizza.name


@pytest.mark.django_db
def test_search_pizza(client):
    Pizza.objects.create(name="BBQ", base_price=12, is_available=True)
    Pizza.objects.create(name="Veggie Pizza", base_price=11, is_available=True)
    url = reverse("pizza-list")
    response = client.get(url, {"search": "veggie Pizza"})
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["name"] == "Veggie Pizza"


@pytest.mark.django_db
def test_calculate_price(client, pizza, extras):
    url = reverse("pizza-calculate-price", args=[pizza.id])
    payload = {
        "quantity": 2,
        "extras": [extra.id for extra in extras],
    }
    response = client.post(url, data=payload, format="json")
    assert response.status_code == 200
    assert response.data["quantity"] == 2
    assert response.data["total_price"] == pytest.approx(
        (pizza.base_price + sum(e.price for e in extras)) * 2
    )


@pytest.mark.django_db
def test_calculate_price_invalid_quantity(client, pizza):
    url = reverse("pizza-calculate-price", args=[pizza.id])
    response = client.post(url, data={"quantity": 0}, format="json")
    assert response.status_code == 400
    assert "Quantity must be at least 1" in response.data["error"]


@pytest.mark.django_db
def test_list_extras(client, extras):
    url = reverse("extra-list")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_create_order(client, pizza, extras):
    url = reverse("order-list")
    payload = {
        "pizza": pizza.id,
        "extras": [extras[0].id],
        "quantity": 1,
        "customer_name": "John Doe",
        "delivery_address": "123 Pizza Street",
    }
    response = client.post(url, data=payload, format="json")
    assert response.status_code == 201
    order = Order.objects.get(pk=response.data["id"])
    expected_price = pizza.base_price + extras[0].price
    assert order.total_price == expected_price
