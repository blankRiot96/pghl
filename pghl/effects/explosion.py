import pygame
import random
from pghl.effects.particle import Particle


class Explosion:
    def __init__(self, n_particles, n_size, pos, speed, color, size_reduction=5):
        self.n_particles = n_particles
        self.n_size = n_size

        self.particles = [Particle(
            pos=pos,
            color=color,
            size=random.randrange(*n_size),
            speed=random.uniform(*speed),
            shape="square",
            glow=True,
            size_reduction=size_reduction
        ) for _ in range(n_particles)]

    def draw(self, screen, dt):
        for particle in self.particles:
            particle.draw(screen, dt)

            if particle.size < 0:
                self.particles.remove(particle)
