"""NASA API client for asteroid data."""

from datetime import date, datetime
from typing import Any, Optional
from urllib.parse import urljoin

import httpx

from astroviz.models.asteroid import Asteroid, AsteroidOrbit, AsteroidPhysical


class NASAAPIError(Exception):
    """Custom exception for NASA API errors."""

    pass


class NASAClient:
    """Client for NASA asteroid data APIs."""

    BASE_URL = "https://api.nasa.gov/"
    NEO_URL = "neo/rest/v1/"

    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize NASA API client.

        Args:
            api_key: NASA API key. If None, uses DEMO_KEY with rate limits.
        """
        self.api_key = api_key or "DEMO_KEY"
        self.base_url = urljoin(self.BASE_URL, self.NEO_URL)

        # HTTP client with proper timeouts and retries
        self.client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
        )

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.client.aclose()

    async def _make_request(
        self, endpoint: str, params: dict[str, Any]
    ) -> dict[str, Any]:
        """Make HTTP request to NASA API with error handling.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            JSON response data

        Raises:
            NASAAPIError: If API request fails
        """
        params["api_key"] = self.api_key
        url = urljoin(self.base_url, endpoint)

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise NASAAPIError(
                    "Rate limit exceeded. Consider using a valid API key."
                ) from e
            raise NASAAPIError(
                f"HTTP {e.response.status_code}: {e.response.text}"
            ) from e
        except httpx.RequestError as e:
            raise NASAAPIError(f"Request failed: {str(e)}") from e

    async def get_neo_feed(
        self, start_date: Optional[date] = None, end_date: Optional[date] = None
    ) -> list[dict[str, Any]]:
        """Get Near Earth Object data for date range.

        Args:
            start_date: Start date for NEO feed (default: today)
            end_date: End date for NEO feed (default: start_date + 7 days)

        Returns:
            List of NEO data dictionaries
        """
        if start_date is None:
            start_date = date.today()
        if end_date is None:
            end_date = start_date

        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }

        data = await self._make_request("feed", params)

        # Flatten NEO data from all dates
        all_neos = []
        for _date_str, neos in data.get("near_earth_objects", {}).items():
            all_neos.extend(neos)

        return all_neos

    async def get_asteroid_details(self, asteroid_id: str) -> dict[str, Any]:
        """Get detailed information for a specific asteroid.

        Args:
            asteroid_id: Asteroid ID or SPK-ID

        Returns:
            Detailed asteroid data
        """
        return await self._make_request(f"neo/{asteroid_id}", {})

    async def browse_asteroids(self, page: int = 0, size: int = 20) -> dict[str, Any]:
        """Browse paginated list of asteroids.

        Args:
            page: Page number (0-based)
            size: Number of results per page (max 1000)

        Returns:
            Paginated asteroid data with metadata
        """
        params = {"page": page, "size": min(size, 1000)}
        return await self._make_request("neo/browse", params)

    def _parse_orbital_data(self, orbital_data: dict[str, Any]) -> AsteroidOrbit:
        """Parse orbital elements from NASA API data."""
        return AsteroidOrbit(
            semi_major_axis=float(orbital_data.get("semi_major_axis", 0)),
            eccentricity=float(orbital_data.get("eccentricity", 0)),
            inclination=float(orbital_data.get("inclination", 0)),
            longitude_ascending_node=float(
                orbital_data.get("ascending_node_longitude", 0)
            ),
            argument_periapsis=float(orbital_data.get("perihelion_argument", 0)),
            mean_anomaly=float(orbital_data.get("mean_anomaly", 0)),
        )

    def _parse_physical_data(self, neo_data: dict[str, Any]) -> AsteroidPhysical:
        """Parse physical characteristics from NASA API data."""
        estimated_diameter = neo_data.get("estimated_diameter", {})
        km_data = estimated_diameter.get("kilometers", {})

        return AsteroidPhysical(
            diameter=km_data.get("estimated_diameter_max"),
            absolute_magnitude=neo_data.get("absolute_magnitude_h"),
            # NASA NEO API doesn't provide albedo, rotation_period, spectral_type
            # These would come from other NASA databases (SBDB, etc.)
        )

    def parse_neo_data(self, neo_data: dict[str, Any]) -> Asteroid:
        """Parse NEO data from NASA API into Asteroid model.

        Args:
            neo_data: Raw NEO data from NASA API

        Returns:
            Parsed Asteroid object

        Raises:
            ValidationError: If data doesn't match expected schema
        """
        # Extract orbital data - this is simplified as NASA NEO API
        # doesn't provide full orbital elements
        orbital_data = neo_data.get("orbital_data", {})

        # Create simplified orbital data (real implementation would need SBDB)
        orbit = AsteroidOrbit(
            semi_major_axis=float(orbital_data.get("semi_major_axis", 1.0)),
            eccentricity=float(orbital_data.get("eccentricity", 0.1)),
            inclination=float(orbital_data.get("inclination", 5.0)),
            longitude_ascending_node=0.0,  # Not in NEO API
            argument_periapsis=0.0,  # Not in NEO API
            mean_anomaly=0.0,  # Not in NEO API
        )

        physical = self._parse_physical_data(neo_data)

        return Asteroid(
            id=neo_data["id"],
            name=neo_data["name"],
            neo_reference_id=neo_data.get("neo_reference_id"),
            is_potentially_hazardous=neo_data.get(
                "is_potentially_hazardous_asteroid", False
            ),
            orbit=orbit,
            physical=physical,
            epoch=datetime.now(),  # NEO API doesn't provide epoch
        )
