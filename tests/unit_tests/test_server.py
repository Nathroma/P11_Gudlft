import server

server.clubs = [
    {
        "name":"test",
        "email":"test@unitaire.com",
        "points":"15"
    },
    {
        "name":"Essaie",
        "email": "essaie@secondaire.com",
        "points":"5"
    }
]

server.competitions = [
	{
		"name": "First",
		"date": "2019-02-12 09:00:00",
		"numberOfPlaces": "24"
	},
	{
		"name": "Second",
		"date": "2023-07-15 11:30:00",
		"numberOfPlaces": "15"
	},
	{
		"name": "Third",
		"date": "2022-09-30 11:00:00",
		"numberOfPlaces": "6"
	}
]


def test_unknown_email_adress(client):
	email = "fake@email.com"
	response = client.post('/showSummary', data={"email": email})
	assert response.status_code == 200
	assert "Aucune adresse email correspondante !" in response.data.decode()
	

def test_correct_email_adress(client):
	email = "test@unitaire.com"
	response = client.post('/showSummary', data={"email": email})
	assert response.status_code == 200
	assert ("Welcome, " + email) in response.data.decode()


def test_oudated_comp(client):
	response = client.get('/book/First/test')
	assert "Une erreur est apparue, veuillez reessayer" in response.data.decode()
	assert response.status_code == 200


def test_should_status_code_ok(client):
	response = client.get('/')
	assert response.status_code == 200


def test_clubs_table_points(client):
	response = client.get('/display')
	assert response.status_code == 200
	assert server.clubs[0]["name"] in response.data.decode()
	assert server.clubs[1]["points"] in response.data.decode()


def test_logout(client):
	response = client.get('/logout')
	assert response.status_code == 302
