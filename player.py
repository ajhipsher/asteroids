import pygame

from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_TIMER,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    SHOT_RADIUS,
)
from shot import Shot


class Player(CircleShape):
    containers = ()

    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0
        for group in self.containers:
            group.add(self)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        return shot

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Handle rotation and movement
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

        # Handle shooting
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            self.shoot()
            self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_TIMER
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
