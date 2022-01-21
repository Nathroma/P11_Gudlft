from tests.unit_tests.test_server import server
from tests.unit_tests.conftest import client


def test_purchase_not_enough_point(client):
	comp = server.competitions[1]
	club = server.clubs[1]
	response = client.post('/purchasePlaces', data={
		"club": club['name'],
		"competition": comp['name'],
		"places": 6
		})
	assert "Vous n&#39;avez pas assez de points" in response.data.decode()
	assert response.status_code == 200


def test_purchase_max_places(client):
	comp = server.competitions[1]
	club = server.clubs[0]
	response = client.post('/purchasePlaces', data={
		"club": club['name'],
		"competition": comp['name'],
		"places": 15
		})
	assert "Vous ne pouvez pas prendre plus de 12 places" in response.data.decode()
	assert response.status_code == 200


def test_purchase_max_places_available(client):
	comp = server.competitions[2]
	club = server.clubs[0]
	response = client.post('/purchasePlaces', data={
		"club": club['name'],
		"competition": comp['name'],
		"places": 7
		})
	assert "Il n&#39;y a pas assez de places disponible pour cette compétition." in response.data.decode()
	assert response.status_code == 200


def test_purchase_places(client):
	comp = server.competitions[1]
	club = server.clubs[0]
	response = client.post('/purchasePlaces', data={
		"club": club['name'],
		"competition": comp['name'],
		"places": 2
		})
	assert "Reservation validée ! Nombre de places achetées : 2" in response.data.decode()
	assert club["points"] == 15-2*3
	assert comp["numberOfPlaces"] == 15-2
	assert club[comp['name']] == 2
	assert response.status_code == 200
