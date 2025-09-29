import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, Line } from '@react-three/drei';
import * as THREE from 'three';

interface AsteroidSceneProps {
  data: {
    asteroids: Array<{
      id: string;
      name: string;
      position: [number, number, number];
      size: number;
      orbit: Array<[number, number, number]>;
    }>;
  };
}

const AsteroidScene = ({ data }: AsteroidSceneProps) => {
  const groupRef = useRef<THREE.Group>(null);

  useFrame((state) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += 0.001;
    }
  });

  return (
    <group ref={groupRef}>
      {/* Sun representation */}
      <Sphere args={[1, 32, 32]} position={[0, 0, 0]}>
        <meshStandardMaterial color="yellow" emissive="yellow" emissiveIntensity={0.6} />
      </Sphere>

      {/* Asteroids and their orbits */}
      {data.asteroids.map((asteroid) => (
        <group key={asteroid.id}>
          {/* Asteroid */}
          <Sphere
            args={[asteroid.size, 16, 16]}
            position={asteroid.position}
          >
            <meshStandardMaterial
              color="gray"
              roughness={0.7}
              metalness={0.3}
            />
          </Sphere>

          {/* Orbit path */}
          <Line
            points={asteroid.orbit}
            color="white"
            lineWidth={1}
            opacity={0.3}
            transparent
          />
        </group>
      ))}
    </group>
  );
};

export default AsteroidScene;
