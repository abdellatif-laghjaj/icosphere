import React from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import styled from 'styled-components';

const Container = styled.div`
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
`;

function Sphere() {
  const radius = 20;
  const detail = 1;

  return (
    <mesh>
      <icosahedronGeometry args={[radius, detail]} />
      <meshStandardMaterial
        color={0xffffff}
        wireframe
        roughness={0.5}
        metalness={0.6}
      />
    </mesh>
  );
}

function App() {
  return (
    <Container>
      <Canvas camera={{ position: [0, 0, 80], fov: 40 }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[0, 20, 60]} intensity={2} />
        <OrbitControls minDistance={60} maxDistance={150} />
        <Sphere />
      </Canvas>
    </Container>
  );
}

export default App;