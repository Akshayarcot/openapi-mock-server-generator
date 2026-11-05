import math
import random
import pygame

class Particle:
    """Juice splash or spark particle created upon slicing."""
    def __init__(self, x, y, color, is_spark=False):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 7) if not is_spark else random.uniform(3, 9)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.gravity = 0.25
        self.color = color
        self.radius = random.uniform(2.5, 5.0)
        self.alpha = 255
        self.decay = random.uniform(8, 14)
        self.is_spark = is_spark

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.alpha = max(0, self.alpha - self.decay)
        self.radius = max(0.5, self.radius - 0.08)

    def is_dead(self):
        return self.alpha <= 0 or self.radius <= 0.5

    def render(self, screen):
        if self.alpha <= 0:
            return
        surf = pygame.Surface((int(self.radius * 2) + 2, int(self.radius * 2) + 2), pygame.SRCALPHA)
        color_with_alpha = (*self.color[:3], int(self.alpha))
        pygame.draw.circle(surf, color_with_alpha, (int(self.radius) + 1, int(self.radius) + 1), int(self.radius))
        screen.blit(surf, (self.x - self.radius, self.y - self.radius))


class FruitHalf:
    """One half of a sliced fruit flying away with physics."""
    def __init__(self, x, y, vx, vy, color, radius, direction=1):
        self.x = x
        self.y = y
        self.vx = vx + direction * random.uniform(2.0, 4.5)
        self.vy = vy - random.uniform(1.0, 3.0)
        self.gravity = 0.4
        self.color = color
        self.radius = radius
        self.angle = 0.0
        self.rot_speed = direction * random.uniform(4.0, 8.0)

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.angle += self.rot_speed

    def off_screen(self, height):
        return self.y - self.radius > height + 50

    def render(self, screen):
        diameter = int(self.radius * 2) + 4
        surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        center = (diameter // 2, diameter // 2)

        # Draw semi-circle half
        rect = pygame.Rect(center[0] - self.radius, center[1] - self.radius, self.radius * 2, self.radius * 2)
        pygame.draw.arc(surf, self.color, rect, 0, math.pi, int(self.radius))
        # Inner flesh lighter tone
        inner_color = tuple(min(255, c + 40) for c in self.color)
        pygame.draw.arc(surf, inner_color, rect, 0.1, math.pi - 0.1, max(2, int(self.radius * 0.4)))

        # Rotate and blit
        rotated_surf = pygame.transform.rotate(surf, self.angle)
        new_rect = rotated_surf.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_surf, new_rect.topleft)


class Fruit:
    def __init__(self, x, y, vx, vy, gravity, radius=28, kind="fruit"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.gravity = gravity
        self.radius = radius
        self.kind = kind  # "fruit" or "bomb"
        self.sliced = False
        self.color = (255, 255, 255)
        self.fuse_timer = 0

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.fuse_timer += 1

    def contains_point(self, x, y):
        """Check if a single point (x, y) is inside the fruit circle."""
        return math.hypot(self.x - x, self.y - y) <= self.radius

    def intersects_segment(self, p1, p2):
        """
        Task 1 Fix: Continuous Collision Detection.
        Checks if line segment p1 -> p2 intersects the fruit circle.
        Computes the minimum distance from circle center to segment.
        """
        if self.sliced:
            return False

        x1, y1 = p1
        x2, y2 = p2
        dx = x2 - x1
        dy = y2 - y1

        # Zero length segment -> fallback to single point check
        if dx == 0 and dy == 0:
            return self.contains_point(x1, y1)

        # Vector projection of circle center onto segment p1-p2
        # Center is (self.x, self.y)
        t = ((self.x - x1) * dx + (self.y - y1) * dy) / (dx * dx + dy * dy)
        t = max(0.0, min(1.0, t))  # Clamp to line segment bounds

        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        dist = math.hypot(self.x - closest_x, self.y - closest_y)
        return dist <= self.radius

    def split(self):
        """Generates two fruit halves and splash particles upon slicing."""
        halves = []
        particles = []

        if self.kind == "fruit":
            # Two tumbling fruit halves
            halves.append(FruitHalf(self.x - 5, self.y, self.vx, self.vy, self.color, self.radius, direction=-1))
            halves.append(FruitHalf(self.x + 5, self.y, self.vx, self.vy, self.color, self.radius, direction=1))
            # Juice particles
            for _ in range(16):
                particles.append(Particle(self.x, self.y, self.color))
        else:
            # Bomb explosion sparks and smoke
            spark_colors = [(255, 200, 50), (255, 80, 20), (240, 240, 240), (80, 80, 80)]
            for _ in range(30):
                particles.append(Particle(self.x, self.y, random.choice(spark_colors), is_spark=True))

        return halves, particles

    def off_screen(self, height):
        return self.y - self.radius > height

    def render(self, screen):
        center = (int(self.x), int(self.y))
        if self.kind == "bomb":
            # Bomb body (dark sphere with specular highlight)
            pygame.draw.circle(screen, (35, 35, 40), center, self.radius)
            pygame.draw.circle(screen, (70, 70, 80), (center[0] - self.radius // 3, center[1] - self.radius // 3), max(3, self.radius // 4))
            # Fuse stem & wick
            stem_rect = (center[0] - 3, center[1] - self.radius - 8, 6, 9)
            pygame.draw.rect(screen, (120, 100, 80), stem_rect)
            # Animated fuse spark
            spark_color = (255, 215, 0) if (self.fuse_timer // 4) % 2 == 0 else (255, 70, 0)
            spark_pos = (center[0], center[1] - self.radius - 10)
            pygame.draw.circle(screen, spark_color, spark_pos, 4)
        else:
            # Fruit outer skin
            pygame.draw.circle(screen, self.color, center, self.radius)
            # Inner flesh gradient / highlight
            inner_color = tuple(min(255, c + 35) for c in self.color)
            pygame.draw.circle(screen, inner_color, (center[0] - self.radius // 4, center[1] - self.radius // 4), max(2, self.radius // 3))
            # Border outline
            pygame.draw.circle(screen, (255, 255, 255, 120), center, self.radius, 2)
