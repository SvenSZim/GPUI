import numpy as np
from numpy.typing import NDArray

from .verletobject import VerletObject

class Engine:
    """
    example implementation of a verlet-physics-solver
    """

    # constants
    substeps: int
    
    gravityMode: int
    gravityStrength: np.float64
    worldcenter: NDArray[np.float64]
    worldrad: np.float64

    objects: list[VerletObject] = []
    objRad: np.float64
    randomRadOffsetRange: np.float64
    doRandomRadOff: bool

    doCollisionSolving: bool
    collisionDamping: np.float64

    def __init__(self, center: NDArray[np.float64], worldradius: np.float64, objradius: np.float64) -> None:
        self.substeps = 12
        self.worldcenter = center
        self.gravityMode = 0
        self.gravityStrength = np.float64(1_000)
        self.worldrad = worldradius
        
        self.objRad = objradius
        self.randomRadOffsetRange = objradius / 2
        self.doRandomRadOff = False

        self.doCollisionSolving = False
        self.collisionDamping = np.float64(0.95)


    def addObject(self, initialPosition: NDArray[np.float64], initialSpeed: NDArray[np.float64]) -> None:
        rad = self.objRad
        if self.doRandomRadOff:
            rad += np.random.uniform(-self.randomRadOffsetRange, self.randomRadOffsetRange)
        self.objects.append(VerletObject(initialPosition, rad, initialPosition-initialSpeed, np.zeros(2)))

    def toggleCollisions(self) -> None:
        self.doCollisionSolving = not self.doCollisionSolving

    def toggleRandomRadOff(self) -> None:
        self.doRandomRadOff = not self.doRandomRadOff

    def setGravityMode(self, mode: int) -> None:
        self.gravityMode = mode % 3

    def update(self, dt: np.float64) -> None:
        subdt: np.float64 = dt / self.substeps
        for _ in range(self.substeps):
            self.applyGravity()
            self.updatePositions(subdt)
            if self.doCollisionSolving:
                self.solveCollisions()
            self.applyConstraint()

    def updatePositions(self, dt: np.float64) -> None:
        for obj in self.objects:
            obj.updatePosition(dt)


    def applyGravity(self) -> None:
        match self.gravityMode:
            case 0:
                gravity: NDArray[np.float64] = self.gravityStrength * np.array([0, 1])
                for obj in self.objects:
                    obj.accelerate(gravity)
            case 2:
                for obj in self.objects:
                    obj.accelerate((self.worldcenter - obj.position) * (self.gravityStrength / np.linalg.norm(self.worldcenter - obj.position)))

    def applyConstraint(self) -> None:
        for obj in self.objects:
            toObj: NDArray[np.float64] = obj.position - self.worldcenter
            dst: np.float64 = np.float64(np.linalg.norm(toObj))

            if dst > self.worldrad - self.objRad:
                toObjNorm = toObj / dst

                velocity = obj.getVelocity()
                reflected_velocity = velocity - 2 * np.dot(velocity, toObjNorm) * toObjNorm
                reflected_velocity *= self.collisionDamping

                obj.position = self.worldcenter + toObjNorm * (self.worldrad - self.objRad)
                obj.prevPosition = obj.position - reflected_velocity

    def solveCollisions(self) -> None:
        for i, obj1 in enumerate(self.objects[:-1]):
            for obj2 in self.objects[i+1:]:
                delta = obj1.position - obj2.position
                dist = np.linalg.norm(delta)
                min_dist = obj1.radius + obj2.radius

                if dist < min_dist and dist > 1e-8:
                    normal = delta / dist
                    penetration = min_dist - dist

                    obj1.position += 0.5 * penetration * normal
                    obj2.position -= 0.5 * penetration * normal

                    v1 = obj1.position - obj1.prevPosition
                    v2 = obj2.position - obj2.prevPosition

                    v_rel = v1 - v2
                    v_rel_normal = np.dot(v_rel, normal)

                    if v_rel_normal < 0:
                        impulse = -v_rel_normal * self.collisionDamping

                        v1_new = v1 + impulse * normal
                        v2_new = v2 - impulse * normal

                        obj1.prevPosition = obj1.position - v1_new
                        obj2.prevPosition = obj2.position - v2_new


    def getAllObjectPositions(self) -> list[tuple[NDArray[np.float64], np.float64]]:
        return [(obj.position, obj.radius) for obj in self.objects]

    def applyRandomTeleports(self, radius: np.float64) -> None:
        for obj in self.objects:
            theta: np.float64 = np.float64(np.random.uniform(0, 2 * np.pi))
            r: np.float64 = radius * np.sqrt(np.random.uniform(0, 1))
            obj.teleport(obj.position + np.array([r * np.cos(theta), r * np.sin(theta)]))

    def clear(self) -> None:
        self.objects = []
