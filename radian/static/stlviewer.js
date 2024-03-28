import * as THREE from "three";

import Stats from "three/stats";

import { STLLoader } from "three/stlloader";

import { OrbitControls } from "three/orbitcontrols"

export function STLViewer(stl_model, elem_id) {

  let scene, camera, renderer, container;

  init(stl_model, elem_id);
  animate();

  function init(stl_model, elem_id) {

    container = document.createElement('div');
    let model_elem = document.getElementById(elem_id)
    model_elem.parentNode.replaceChild(container, model_elem)

    camera = new THREE.PerspectiveCamera(45, (window.innerWidth / 2) / window.innerHeight, 0.1, 100);
    camera.position.set(4, 2, 4);

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xa0a0a0);
    //scene.fog = new THREE.Fog(0xa0a0a0, 4, 20);


    const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 3);
    hemiLight.position.set(0, 20, 0);
    scene.add(hemiLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 3);
    directionalLight.position.set(0, 20, 10);
    directionalLight.castShadow = true;
    directionalLight.shadow.camera.top = 2;
    directionalLight.shadow.camera.bottom = - 2;
    directionalLight.shadow.camera.left = - 2;
    directionalLight.shadow.camera.right = 2;
    scene.add(directionalLight);
    scene.add( new THREE.AmbientLight( 0xffffff, 1 ) );

    // ground

    const ground = new THREE.Mesh(new THREE.PlaneGeometry(40, 40), new THREE.MeshPhongMaterial({ color: 0xbbbbbb, depthWrite: false }));
    ground.rotation.x = - Math.PI / 2;
    ground.receiveShadow = true;
    scene.add(ground);

    const grid = new THREE.GridHelper(40, 20, 0x000000, 0x000000);
    grid.material.opacity = 0.2;
    grid.material.transparent = true;
    scene.add(grid);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize((window.innerWidth / 2), window.innerHeight);
    renderer.shadowMap.enabled = true;

    const loader = new STLLoader();
    console.log("Attempting to display:", stl_model)
    loader.load(stl_model, function (geometry) {
      const material = new THREE.MeshPhongMaterial({
        color: 0xff9c7c,
        specular: 0x494949,
        shininess: 200,
      });
      const mesh = new THREE.Mesh(geometry, material);

      mesh.castShadow = true;
      mesh.receiveShadow = true;
      mesh.position.y = 0.5
      console.log(geometry)

      scene.add(mesh);
      renderer.render(scene, camera);
    });
    console.log("Loaded")

    
    container.appendChild(renderer.domElement);

    //

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.target.set(0, 0.5, 0);
    controls.update();

    //

    window.addEventListener('resize', onWindowResize);

  }

  function onWindowResize() {

    camera.aspect = (window.innerWidth / 2) / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize((window.innerWidth / 2), window.innerHeight);

  }

  function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
  }


}










