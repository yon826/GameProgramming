import pygame
import random

# 초기화
pygame.init()

# 화면 크기 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fluid Simulation")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
BLACK = (0, 0, 0)

# 물방울 입자 클래스 정의
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)  # 수평 속도
        self.vy = random.uniform(1, 3)  # 초기 아래쪽 수직 속도
        self.radius = 5  # 입자의 크기

    def update(self, particles): # 중력 효과 적용
        self.vy += 0.3

        # 속도에 따른 위치 업데이트
        self.x += self.vx
        self.y += self.vy

        # 바닥 충돌 및 반발 처리
        if self.y >= HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
            self.vy *= -0.6  # 반발력
            self.vx *= 0.9   # 마찰 효과

        # 다른 입자와 충돌 처리
        for other in particles:
            if other != self:
                dist = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
                if dist < self.radius * 2:  # 겹침 발생 시 반발 처리
                    overlap = self.radius * 2 - dist
                    self.vy -= overlap * 0.09  # 위로 밀어내는 효과
                    other.vy += overlap * 0.1

        # 화면 밖으로 나가지 않도록 제한
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.vx *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius)

# 파티클 리스트 생성
particles = []

# 게임 루프
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 마우스를 누르고 있을 때 물방울 생성
    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        for _ in range(5):  # 여러 개 생성
            particles.append(Particle(mx, my))

    # 파티클 업데이트 및 그리기
    for particle in particles:
        particle.update(particles)
        particle.draw(screen)

    # 오래된 입자 제거 (화면 아래로 사라지는 경우)
    particles = [p for p in particles if p.y < HEIGHT + 50]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
