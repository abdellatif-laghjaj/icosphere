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
    renderer.setClearColor(0xffffff);
    currentMount.appendChild(renderer.domElement);

    // Create icosahedron
    const radius = 1;
    const detail = 1; // This creates fewer triangles
    const icosahedronGeometry = new THREE.IcosahedronGeometry(radius, detail);

    // Create curved lines
    const lineMaterial = new THREE.LineBasicMaterial({ color: 0xff0000 });

    const edges = new THREE.EdgesGeometry(icosahedronGeometry);
    const positions = edges.attributes.position.array;

    for (let i = 0; i < positions.length; i += 6) {
      const start = new THREE.Vector3(positions[i], positions[i+1], positions[i+2]);
      const end = new THREE.Vector3(positions[i+3], positions[i+4], positions[i+5]);

      // Calculate midpoint and adjust it slightly outward
      const midPoint = start.clone().add(end).multiplyScalar(0.5);
      midPoint.normalize().multiplyScalar(radius * 1.05); // Reduced bulge factor

      const curve = new THREE.QuadraticBezierCurve3(
        start,
        midPoint,
        end
      );

      const points = curve.getPoints(20);
      const curveGeometry = new THREE.BufferGeometry().setFromPoints(points);
      const curveLine = new THREE.Line(curveGeometry, lineMaterial);
      scene.add(curveLine);
    }

    // Position camera
    camera.position.z = 2;

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