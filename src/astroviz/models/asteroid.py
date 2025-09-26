"""Asteroid data models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AsteroidOrbit(BaseModel):
    """Orbital parameters of an asteroid."""

    semi_major_axis: float = Field(..., description="Semi-major axis in AU")
    eccentricity: float = Field(..., ge=0, le=1, description="Orbital eccentricity")
    inclination: float = Field(..., description="Orbital inclination in degrees")
    longitude_ascending_node: float = Field(
        ..., description="Longitude of ascending node"
    )
    argument_periapsis: float = Field(..., description="Argument of periapsis")
    mean_anomaly: float = Field(..., description="Mean anomaly at epoch")


class AsteroidPhysical(BaseModel):
    """Physical characteristics of an asteroid."""

    diameter: Optional[float] = Field(None, description="Diameter in kilometers")
    absolute_magnitude: Optional[float] = Field(
        None, description="Absolute magnitude H"
    )
    albedo: Optional[float] = Field(None, ge=0, le=1, description="Geometric albedo")
    rotation_period: Optional[float] = Field(
        None, description="Rotation period in hours"
    )
    spectral_type: Optional[str] = Field(None, description="Spectral classification")


class Asteroid(BaseModel):
    """Complete asteroid data model."""

    id: str = Field(..., description="Unique asteroid identifier")
    name: str = Field(..., description="Asteroid name or designation")
    neo_reference_id: Optional[str] = Field(None, description="NEO reference ID")
    is_potentially_hazardous: bool = Field(default=False, description="PHO status")
    orbit: AsteroidOrbit
    physical: AsteroidPhysical
    epoch: datetime = Field(..., description="Epoch of orbital elements")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CloseApproach(BaseModel):
    """Close approach data for NEOs."""

    asteroid_id: str
    approach_date: datetime
    velocity_kms: float = Field(..., description="Velocity in km/s")
    miss_distance_km: float = Field(..., description="Miss distance in kilometers")
    miss_distance_au: float = Field(..., description="Miss distance in AU")
