from fastapi.testclient import TestClient
from backend.app.main import app
def test_health_endpoint_reports_ok():
 with TestClient(app) as client:
  response=client.get('/health');assert response.status_code==200;assert response.json()['status']=='ok'
def test_home_serves_mvp_ui():
 with TestClient(app) as client:
  response=client.get('/');assert response.status_code==200;assert 'AudioHardcore' in response.text
def test_scan_endpoint_rejects_missing_directory():
 with TestClient(app) as client:
  response=client.post('/library/scan',json={'path':'/definitely/not/a/real/folder'});assert response.status_code==400
