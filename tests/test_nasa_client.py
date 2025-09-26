"""Tests for NASA API client."""

from datetime import date
from unittest.mock import AsyncMock, patch

import pytest
from astroviz.data.nasa_client import NASAAPIError, NASAClient


class TestNASAClient:
    """Test cases for NASAClient."""

    @pytest.fixture
    def nasa_client(self) -> NASAClient:
        """Create NASAClient instance for testing."""
        return NASAClient(api_key="test_key")

    @pytest.mark.asyncio
    async def test_client_initialization(self, nasa_client: NASAClient) -> None:
        """Test client initialization."""
        assert nasa_client.api_key == "test_key"
        assert "neo/rest/v1/" in nasa_client.base_url

    @pytest.mark.asyncio
    async def test_context_manager(self) -> None:
        """Test async context manager functionality."""
        async with NASAClient() as client:
            assert client.api_key == "DEMO_KEY"

    @pytest.mark.asyncio
    async def test_get_neo_feed_success(self, nasa_client: NASAClient) -> None:
        """Test successful NEO feed request."""
        mock_response = {
            "near_earth_objects": {
                "2024-01-01": [
                    {"id": "123", "name": "Test Asteroid"},
                    {"id": "456", "name": "Another Asteroid"},
                ]
            }
        }

        with patch.object(
            nasa_client, "_make_request", new_callable=AsyncMock
        ) as mock_request:
            mock_request.return_value = mock_response

            result = await nasa_client.get_neo_feed(date(2024, 1, 1), date(2024, 1, 1))

            assert len(result) == 2
            assert result[0]["name"] == "Test Asteroid"
            mock_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_api_error_handling(self, nasa_client: NASAClient) -> None:
        """Test API error handling."""
        with patch.object(nasa_client.client, "get") as mock_get:
            mock_get.side_effect = Exception("Connection error")

            with pytest.raises(NASAAPIError):
                await nasa_client._make_request("test", {})
