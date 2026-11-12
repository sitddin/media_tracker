def test_health_with_client(client):
    response = client.get("/health")

    assert response.status_code == 200