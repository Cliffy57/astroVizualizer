import { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars } from '@react-three/drei';
import axios from 'axios';
import AsteroidScene from './components/AsteroidScene';
import './App.css';

function App() {
  const [sceneData, setSceneData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSceneData = async () => {
      try {
        const response = await axios.get('/api/v1/viz/3d-scene');
        setSceneData(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to load asteroid data');
        setLoading(false);
      }
    };

    fetchSceneData();
  }, []);

  if (loading) {
    return <div className="loading">Loading asteroid data...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="app">
      <Canvas camera={{ position: [0, 20, 20], fov: 60 }}>
        <color attach="background" args={['#000']} />
        <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} />
        <OrbitControls enablePan enableZoom enableRotate />
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1.5} />
        {sceneData && <AsteroidScene data={sceneData} />}
      </Canvas>
    </div>
  );
}

export default App;
