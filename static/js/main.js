import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

// Initialisation de la scène
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Charger l'image de fond (remplace 'background.jpg' par le nom de ton image)
const textureLoader = new THREE.TextureLoader();
const backgroundTexture = textureLoader.load('../../imgs/background.jpg');
scene.background = backgroundTexture;

// Ajout des lumières
const ambientLight = new THREE.AmbientLight(0x404040, 2); // Lumière douce
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 2); // Lumière directionnelle
directionalLight.position.set(5, 5, 5).normalize();
scene.add(directionalLight);

// Gestion du chargement du modèle et animations
const loader = new GLTFLoader();
let model, mixer, currentAction;

const animationsTalk = [
    'assets/scene-talk.glb',
];

const animationsLaugh = [
    'assets/scene-laugh.glb',
];

const animationsAngry = [
    'assets/scene-angry.glb',
];

const animationsTask = [
    'assets/scene-sit-down.glb',
    'assets/scene-sit-to-type.glb',
    'assets/scene-typing.glb',
];

const animationsStopTask = [
    'assets/scene-stop-type.glb',
    'assets/scene-sit-up.glb',
];

var newAction;

// Charger et appliquer une animation
async function loadAnimation(animationPath) {
    return new Promise((resolve, reject) => {
        loader.load(animationPath, (gltf) => {
            console.log(`Animation ${animationPath} chargée avec succès`);

            const animation = gltf.animations[0];

            if (animation) {
                if (currentAction) {
                    currentAction.fadeOut(0.5);
                }

                newAction = mixer.clipAction(animation);
                newAction.reset().fadeIn(0.5).play();

                currentAction = newAction;

                newAction.clampWhenFinished = true;
                newAction.loop = THREE.LoopOnce;
                newAction.getMixer().addEventListener('finished', () => {
                    resolve();
                });
            } else {
                console.warn(`Aucune animation trouvée dans ${animationPath}`);
                resolve();
            }
        }, undefined, (error) => {
            console.error(`Erreur lors du chargement de l’animation : ${error}`);
            reject(error);
        });
    });
}

// Fonction pour jouer toutes les animations enchaînées
async function playChainedAnimationsTest(index = 0) {
    if (index < animationsTask.length) {
        await loadAnimation(animationsTask[index]);
        await playChainedAnimationsTest(index + 1);
    } else {
        await loadAnimation(animationsTask[2]);
    }
}

async function playChainedAnimationsTest2(index2 = 0) {
    if (index2 < animationsStopTask.length - 1) {
        await loadAnimation(animationsStopTask[index2]);
        await playChainedAnimationsTest2(index2 + 1);
    } else {
        await loadAnimation(animationsTalk[0]);
    }
}

// Changer d'animation à chaque clic
async function test1() {
    await loadAnimation(animationsTalk[0]);
}

async function test2() {
    await loadAnimation(animationsLaugh[0]);
}

async function test3() {
    await loadAnimation(animationsAngry[0]);
}

async function test4() {
    await playChainedAnimationsTest(0);
}

async function test5() {
    await playChainedAnimationsTest2(0);
}

async function changeAnimation(task) {
    switch (task) {
        case 'talk':
            await test1();
            break;
        case 'laugh':
            await test2();
            break;
        case 'angry':
            await test3();
            break;
        case 'task':
            await test4();
            break;
        case 'stop-task':
            await test5();
            break;
        default:
            console.log('Task not found');
    }
}

// Attach the changeAnimation function to the window object
window.changeAnimation = changeAnimation;

// Charger le modèle principal (character.glb)
loader.load('assets/character.glb', (gltf) => {
    model = gltf.scene;
    model.scale.set(2, 2, 2);
    model.position.set(-0.1, -2.3, 0);
    scene.add(model);

    console.log('Modèle chargé avec succès');

    // Initialisation du mixer après avoir ajouté le modèle
    mixer = new THREE.AnimationMixer(model);

    // Charger la première animation
    changeAnimation('talk');
}, undefined, (error) => {
    console.error('Erreur lors du chargement du modèle :', error);
});

// Ajuster la caméra
camera.position.set(0, 1, 5);
camera.lookAt(0, 1, 0);

// Fonction d'animation
function animate() {
    if (mixer) {
        mixer.update(0.016); // Mise à jour (~60 FPS)
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
