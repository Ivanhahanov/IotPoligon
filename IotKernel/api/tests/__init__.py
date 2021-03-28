from fastapi.testclient import TestClient
from IotKernel.api.server import app

client = TestClient(app)