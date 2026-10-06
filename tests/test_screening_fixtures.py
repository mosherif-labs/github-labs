def test_screening_hit_is_reviewed(client, screening_hit):
    response = client.post("/transactions/screen", json=screening_hit)

    assert response.json()["decision"] == "review"


def test_screening_partial_is_reviewed(client, screening_partial):
    response = client.post("/transactions/screen", json=screening_partial)

    assert response.json()["decision"] == "review"


def test_screening_clean_is_cleared(client, screening_clean):
    response = client.post("/transactions/screen", json=screening_clean)

    assert response.json()["decision"] == "clear"
