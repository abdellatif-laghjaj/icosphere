import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';

function App() {
  const mountRef = useRef(null);

  useEffect(() => {
    const currentMount = mountRef.current;

    // Scene setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0xffffff);  // Set background to white
    currentMount.appendChild(renderer.domElement);

    // Create icosphere
    const radius = 1;
    const detail = 1;  // Reduced detail to match the image
    const geometry = new THREE.IcosahedronGeometry(radius, detail);

    // Create material for faces
    const faceMaterial = new THREE.MeshBasicMaterial({
      color: 0xeeeeee,  // Light grey color
      side: THREE.DoubleSide
    });

    // Create material for edges
    const edgeMaterial = new THREE.LineBasicMaterial({
      color: 0xff0000,  // Red color
      linewidth: 2
    });

    // Create mesh for faces
    const icosphere = new THREE.Mesh(geometry, faceMaterial);
    scene.add(icosphere);

    // Create edges
    const edges = new THREE.EdgesGeometry(geometry);
    const line = new THREE.LineSegments(edges, edgeMaterial);
    scene.add(line);

    // Position camera
    camera.position.z = 3;

    // Add OrbitControls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.25;
    controls.enableZoom = true;

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

    // Handle window resize
    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };
    window.addEventListener('resize', handleResize);

    // Cleanup
    return () => {
      currentMount.removeChild(renderer.domElement);
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return <div ref={mountRef} style={{ width: '100%', height: '100vh' }} />;
}

export default App;