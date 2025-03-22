import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

// Initialisation de la scène
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Charger l'image de fond (remplace 'background.png' par le nom de ton image)
const textureLoader = new THREE.TextureLoader();
const backgroundTexture = textureLoader.load('background.png');
scene.background = backgroundTexture;

// Ajout des lumières
const ambientLight = new THREE.AmbientLight(0x404040, 2);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
directionalLight.position.set(5, 5, 5).normalize();
scene.add(directionalLight);

// Gestion du chargement du modèle et animations
const loader = new GLTFLoader();
let model, mixer, currentAction;
const animations = ['assets/scene-talk.glb', 'assets/scene-angry.glb', 'assets/scene-laugh.glb'];
let animationIndex = 0;

// Nouvelle liste pour l’enchaînement des animations
const chainedAnimations = [
    'assets/scene-sit-down.glb',
    'assets/scene-sit-to-type.glb',
    'assets/scene-typing.glb',
    'assets/scene-stop-type.glb',
    'assets/scene-sit-up.glb'
];

let playingChainedAnimations = false;

// Charger le modèle principal (character.glb)
loader.load('assets/character.glb', (gltf) => {
    model = gltf.scene;
    model.scale.set(2, 2, 2);
    model.position.set(0, -1, 0);
    scene.add(model);

    console.log('Modèle chargé avec succès');

    // Initialisation du mixer après avoir ajouté le modèle
    mixer = new THREE.AnimationMixer(model);

    // Charger la première animation
    loadAnimation(animations[animationIndex]);
}, undefined, (error) => {
    console.error('Erreur lors du chargement du modèle :', error);
});

// Charger et appliquer une animation
function loadAnimation(animationPath, onComplete = null) {
    loader.load(animationPath, (gltf) => {
        console.log(`Animation ${animationPath} chargée avec succès`);

        const animation = gltf.animations[0];

        if (animation) {
            if (currentAction) {
                currentAction.fadeOut(0.5);
            }

            const newAction = mixer.clipAction(animation);
            newAction.reset().fadeIn(0.5).play();
            currentAction = newAction;

            if (onComplete) {
                newAction.clampWhenFinished = true;
                newAction.loop = THREE.LoopOnce;
                newAction.getMixer().addEventListener('finished', onComplete);
            }
        } else {
            console.warn(`Aucune animation trouvée dans ${animationPath}`);
        }
    }, undefined, (error) => {
        console.error(`Erreur lors du chargement de l’animation : ${error}`);
    });
}

// Fonction pour jouer toutes les animations enchaînées
function playChainedAnimations(index = 0) {
    if (index < chainedAnimations.length) {
        loadAnimation(chainedAnimations[index], () => {
            playChainedAnimations(index + 1);
        });
    } else {
        playingChainedAnimations = false;
    }
}

// Changer d'animation à chaque clic
window.addEventListener('click', () => {
    if (!playingChainedAnimations) {
        playingChainedAnimations = true;
        playChainedAnimations();
    } else {
        animationIndex = (animationIndex + 1) % animations.length;
        loadAnimation(animations[animationIndex]);
    }
});

// Ajuster la caméra
camera.position.set(0, 1, 5);
camera.lookAt(0, 1, 0);

// Fonction d'animation
function animate() {
    if (mixer) {
        mixer.update(0.016);
    }
    renderer.render(scene, camera);
}

renderer.setAnimationLoop(animate);

// Ajustement de la taille du canvas si la fenêtre change
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
