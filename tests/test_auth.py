# tests/test_auth.py
import pytest


async def test_auth_login(client, test_user):
	# given
	data = {"email": "test@test.com", "password": "Test1234!"}

	# when 
	response = await client.post("/auth/login", json = data)

	# then
	assert response.status_code == 200
