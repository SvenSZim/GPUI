from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

@dataclass
class VerletObject:
    position: NDArray[np.float64]
    radius: np.float64
    prevPosition: NDArray[np.float64]
    acceleration: NDArray[np.float64]

    def updatePosition(self, dt: np.float64) -> None:
        velocity: NDArray[np.float64] = self.getVelocity()
        self.prevPosition = self.position.copy()
        self.position += velocity + self.acceleration * dt * dt
        self.acceleration = np.zeros(2)

    def accelerate(self, dir: NDArray[np.float64]) -> None:
        self.acceleration += dir

    def getSpeed(self) -> np.float64:
        return np.float64(np.linalg.norm(self.position - self.prevPosition))

    def setSpeed(self, speed: np.float64) -> None:
        cSpeed: np.float64 = self.getSpeed()
        if cSpeed != np.float64(0):
            self.prevPosition = self.position - self.getVelocity() * (speed / cSpeed)

    def getVelocity(self) -> NDArray[np.float64]:
        return self.position - self.prevPosition

    def teleport(self, position: NDArray[np.float64]) -> None:
        velocity: NDArray[np.float64] = self.getVelocity()
        self.position = position
        self.prevPosition = self.position - velocity
