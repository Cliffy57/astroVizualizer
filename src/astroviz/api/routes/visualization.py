"""Visualization API endpoints."""

from typing import Any, Optional

import numpy as np
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

router = APIRouter()


def generate_sample_asteroid_data(num_asteroids: int = 10) -> list[dict[str, Any]]:
    """Generate sample asteroid data for visualization."""
    asteroids = []
    for i in range(num_asteroids):
        # Create an elliptical orbit with more interesting variations
        theta = np.linspace(0, 2 * np.pi, 200)  # More points for smoother orbits
        a = np.random.uniform(3, 20)  # Wider range of semi-major axis
        e = np.random.uniform(0.1, 0.7)  # More varied eccentricity
        b = a * np.sqrt(1 - e**2)  # Semi-minor axis

        # Random inclination for more 3D effect
        inclination = np.random.uniform(-0.3, 0.3)

        # Generate orbit points
        x = a * np.cos(theta)
        y = b * np.sin(theta)

        # Random rotation angle for the orbit
        angle = np.random.uniform(0, 2 * np.pi)
        x_rot = x * np.cos(angle) - y * np.sin(angle)
        y_rot = x * np.sin(angle) + y * np.cos(angle)

        # Add inclination effect
        z = (x_rot + y_rot) * np.sin(inclination)
        x_rot = x_rot * np.cos(inclination)
        y_rot = y_rot * np.cos(inclination)

        # Current position (random point on orbit)
        current_theta = np.random.uniform(0, 2 * np.pi)
        current_x = a * np.cos(current_theta) * np.cos(angle) * np.cos(inclination)
        current_y = b * np.sin(current_theta) * np.cos(inclination)
        current_z = (current_x + current_y) * np.sin(inclination)

        # Create orbit points list with slight randomness for more natural look
        orbit_points = []
        for idx in range(len(x_rot)):
            # Add small random variations to make orbits less perfect
            jitter = np.random.uniform(-0.1, 0.1, 3)
            orbit_points.append([
                float(x_rot[idx] + jitter[0]),
                float(y_rot[idx] + jitter[1]),
                float(z[idx] + jitter[2])
            ])

        # Randomize asteroid properties
        size = np.random.uniform(0.1, 0.4)  # Smaller asteroids for better scale
        name = f"Asteroid-{i+1}"

        asteroid = {
            "id": f"ast-{i}",
            "name": name,
            "position": [float(current_x), float(current_y), float(current_z)],
            "size": size,
            "orbit": orbit_points,
        }
        asteroids.append(asteroid)

    return asteroids


@router.get("/3d-scene")
async def get_3d_scene_data(
    max_asteroids: int = Query(
        100, ge=1, le=1000, description="Max asteroids in scene"
    ),
    time_point: Optional[str] = Query(None, description="Time point for visualization"),
) -> JSONResponse:
    """Get 3D scene data for asteroid visualization."""
    try:
        scene_data = {
            "asteroids": generate_sample_asteroid_data(min(max_asteroids, 15)),
            "metadata": {
                "count": 15,
                "time_point": time_point,
                "coordinate_system": "heliocentric",
            },
        }
        return JSONResponse(scene_data)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating scene: {str(e)}"
        ) from e


@router.get("/stats")
async def get_asteroid_statistics() -> dict[str, Any]:
    """Get statistical overview of asteroid data."""
    try:
        # Implementation will calculate real statistics
        stats = {
            "total_count": 0,
            "neo_count": 0,
            "pha_count": 0,
            "size_distribution": {},
            "orbital_classes": {},
        }
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error calculating stats: {str(e)}"
        ) from e
