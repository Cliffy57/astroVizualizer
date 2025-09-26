"""Data processing utilities for asteroid datasets."""

from typing import Any

import numpy as np
import pandas as pd

from astroviz.models.asteroid import Asteroid


class AsteroidDataProcessor:
    """Processor for asteroid data analysis and visualization preparation."""

    @staticmethod
    def asteroids_to_dataframe(asteroids: list[Asteroid]) -> pd.DataFrame:
        """Convert list of Asteroid objects to pandas DataFrame.

        Args:
            asteroids: List of Asteroid objects

        Returns:
            DataFrame with asteroid data
        """
        data = []
        for asteroid in asteroids:
            row = {
                "id": asteroid.id,
                "name": asteroid.name,
                "is_neo": bool(asteroid.neo_reference_id),
                "is_pha": asteroid.is_potentially_hazardous,
                "diameter_km": asteroid.physical.diameter,
                "absolute_magnitude": asteroid.physical.absolute_magnitude,
                "semi_major_axis_au": asteroid.orbit.semi_major_axis,
                "eccentricity": asteroid.orbit.eccentricity,
                "inclination_deg": asteroid.orbit.inclination,
            }
            data.append(row)

        return pd.DataFrame(data)

    @staticmethod
    def calculate_orbital_position(
        asteroid: Asteroid, julian_date: float
    ) -> tuple[float, float, float]:
        """Calculate 3D heliocentric position of asteroid at given time.

        Args:
            asteroid: Asteroid object with orbital elements
            julian_date: Julian date for position calculation

        Returns:
            Tuple of (x, y, z) coordinates in AU
        """
        # Simplified orbital mechanics calculation
        # Real implementation would use more sophisticated algorithms

        orbit = asteroid.orbit

        # Calculate mean motion (simplified)
        np.sqrt(1.0 / (orbit.semi_major_axis**3))  # AU^3/day^2 units

        # Calculate position (very simplified Kepler problem)
        # This is a placeholder - real implementation needs proper orbital mechanics
        x = orbit.semi_major_axis * np.cos(orbit.mean_anomaly)
        y = (
            orbit.semi_major_axis
            * np.sin(orbit.mean_anomaly)
            * np.cos(orbit.inclination)
        )
        z = (
            orbit.semi_major_axis
            * np.sin(orbit.mean_anomaly)
            * np.sin(orbit.inclination)
        )

        return (x, y, z)

    @staticmethod
    def generate_visualization_data(
        asteroids: list[Asteroid], julian_date: float
    ) -> dict[str, Any]:
        """Generate 3D visualization data for asteroids.

        Args:
            asteroids: List of Asteroid objects
            julian_date: Julian date for positions

        Returns:
            Dictionary with visualization data
        """
        positions = []
        colors = []
        sizes = []
        labels = []

        for asteroid in asteroids:
            x, y, z = AsteroidDataProcessor.calculate_orbital_position(
                asteroid, julian_date
            )
            positions.append([x, y, z])

            # Color coding by type
            if asteroid.is_potentially_hazardous:
                colors.append("#FF0000")  # Red for PHAs
            elif asteroid.neo_reference_id:
                colors.append("#FFA500")  # Orange for NEOs
            else:
                colors.append("#FFFFFF")  # White for main belt

            # Size by diameter or absolute magnitude
            if asteroid.physical.diameter:
                sizes.append(max(2, asteroid.physical.diameter / 10))
            else:
                sizes.append(3)

            labels.append(asteroid.name)

        return {
            "positions": positions,
            "colors": colors,
            "sizes": sizes,
            "labels": labels,
            "count": len(asteroids),
        }
