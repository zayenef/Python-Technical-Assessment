from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_scrape_facebook_data():
    response = client.post("/api/scrape", json={"page_url": "https://www.facebook.com/Nasa/"})
    assert response.status_code == 200
    assert "scraped_data" in response.json()
