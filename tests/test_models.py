"""Tests for data models."""

from datetime import datetime

import pytest
from astroviz.models.asteroid import Asteroid, AsteroidOrbit, AsteroidPhysical
from pydantic import ValidationError


class TestAsteroidModels:
    """Test cases for Asteroid data models."""

    def test_asteroid_orbit_validation(self) -> None:
        """Test AsteroidOrbit model validation."""
        # Valid data
        orbit = AsteroidOrbit(
            semi_major_axis=2.5,
            eccentricity=0.3,
            inclination=15.0,
            longitude_ascending_node=120.0,
            argument_periapsis=45.0,
            mean_anomaly=180.0,
        )
        assert orbit.semi_major_axis == 2.5

        # Invalid eccentricity
        with pytest.raises(ValidationError):
            AsteroidOrbit(
                semi_major_axis=2.5,
                eccentricity=1.5,  # Must be <= 1
                inclination=15.0,
                longitude_ascending_node=120.0,
                argument_periapsis=45.0,
                mean_anomaly=180.0,
            )

    def test_asteroid_physical_optional_fields(self) -> None:
        """Test AsteroidPhysical model with optional fields."""
        physical = AsteroidPhysical()
        assert physical.diameter is None
        assert physical.absolute_magnitude is None

        physical_with_data = AsteroidPhysical(
            diameter=5.2, absolute_magnitude=18.5, albedo=0.15
        )
        assert physical_with_data.diameter == 5.2

    def test_complete_asteroid_model(self) -> None:
        """Test complete Asteroid model creation."""
        orbit = AsteroidOrbit(
            semi_major_axis=2.5,
            eccentricity=0.3,
            inclination=15.0,
            longitude_ascending_node=120.0,
            argument_periapsis=45.0,
            mean_anomaly=180.0,
        )

        physical = AsteroidPhysical(diameter=5.2, absolute_magnitude=18.5)

        asteroid = Asteroid(
            id="test_123",
            name="Test Asteroid",
            orbit=orbit,
            physical=physical,
            epoch=datetime.now(),
        )

        assert asteroid.id == "test_123"
        assert not asteroid.is_potentially_hazardous  # Default False
        assert asteroid.orbit.semi_major_axis == 2.5


if __name__ == "__main__":
    pytest.main([__file__])
