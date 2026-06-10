import pygame
import math
from track import Track
from car import Car
from evolution import next_generation

# Configurações iniciais
WIDTH, HEIGHT = 1200, 800
NUM_CARS = 30
MUTATION_RATE = 0.3

def draw_track(surface, track, cam_x, cam_y):
    # Desenha o traçado da pista conectando os pontos
    pts = [(p[0] - cam_x, p[1] - cam_y) for p in track.points]
    if len(pts) > 1:
        pygame.draw.lines(surface, (80, 80, 90), True, pts, int(track.width * 2))
        pygame.draw.lines(surface, (255, 255, 255), True, pts, 2)  # Linha central


def draw_car(surface, car, cam_x, cam_y):
    # Converte coordenadas da câmera
    cx, cy = int(car.pos[0] - cam_x), int(car.pos[1] - cam_y)

    color = (80, 255, 140) if car.alive else (100, 100, 100)

    # Desenha os sensores se o carro estiver vivo
    if car.alive:
        for i, angle_offset in enumerate(car.sensor_angles):
            dist = car.sensors[i] * car.sensor_length
            end_x = cx + math.cos(car.angle + angle_offset) * dist
            end_y = cy + math.sin(car.angle + angle_offset) * dist
            pygame.draw.line(surface, (255, 100, 100), (cx, cy), (end_x, end_y), 1)

    # Desenha o carro (retângulo rotacionado)
    car_len, car_wid = 20, 10
    corners = [
        (car_len / 2, car_wid / 2), (car_len / 2, -car_wid / 2),
        (-car_len / 2, -car_wid / 2), (-car_len / 2, car_wid / 2)
    ]
    rotated_corners = []
    for x, y in corners:
        rx = x * math.cos(car.angle) - y * math.sin(car.angle)
        ry = x * math.sin(car.angle) + y * math.cos(car.angle)
        rotated_corners.append((cx + rx, cy + ry))

    pygame.draw.polygon(surface, color, rotated_corners)


def draw_telemetry(surface, car, font):
    if not car: return

    # Painel Principal (Lado Direito)[cite: 3]
    hud_rect = pygame.Rect(WIDTH - 250, 10, 240, 200)
    pygame.draw.rect(surface, (15, 20, 35), hud_rect, border_radius=10)

    # 1. THROTTLE & STEERING (Estilo sua imagem)
    steer, gas = car.brain.last_output

    # Texto combinado
    txt = font.render("THROTTLE  |  STEERING", True, (180, 200, 220))
    surface.blit(txt, (WIDTH - 235, 30))

    # Barra de Steering (Slider com bolinha verde)
    pygame.draw.line(surface, (100, 100, 120), (WIDTH - 150, 75), (WIDTH - 30, 75), 3)
    ball_x = (WIDTH - 150) + (steer + 1) * 60  # Mapeia -1..1 para a linha
    pygame.draw.circle(surface, (80, 255, 140), (int(ball_x), 75), 8)

    # Barra de Throttle (Laranja)
    gas_val = (gas + 1) * 40  # Normaliza para altura
    pygame.draw.rect(surface, (255, 144, 48), (WIDTH - 230, 130 - gas_val, 15, gas_val))

    # 2. VELOCIDADE
    speed_txt = font.render(f"SPEED: {car.speed:.1f}", True, (255, 255, 255))
    surface.blit(speed_txt, (WIDTH - 150, 110))

    # Sensores
    for i, val in enumerate(car.sensors):
        txt = font.render(f"S{i}: {val:.2f}", True, (200, 200, 200))
        surface.blit(txt, (WIDTH - 230, 210 + i * 15))

    # Progress e delta
    prog_txt = font.render(f"PROG: {car.prev_progress:.2f}", True, (255, 255, 255))
    delta_txt = font.render(f"DELTA: {car.last_delta:.3f}", True, (200, 200, 100))
    surface.blit(prog_txt, (WIDTH - 230, 320))
    surface.blit(delta_txt, (WIDTH - 230, 340))

    # Reward breakdown
    r_txt = font.render(f"RWD: {car.last_reward:.2f}", True, (100, 255, 100))
    surface.blit(r_txt, (WIDTH - 230, 360))

    # 3. MINI VISUALIZADOR DA REDE (O diferencial)
    # Desenha os neurônios firing (opcional, mas muito foda visualmente)
    for i, h in enumerate(car.brain.last_hidden):
        color = (80, 255, 140) if h > 0 else (255, 80, 80)
        alpha = int(abs(h) * 255)
        pygame.draw.circle(surface, color, (WIDTH - 230 + (i * 25), 180), 5)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Neural Network F1 Racing")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    track = Track()
    cars = [Car(track) for _ in range(NUM_CARS)]
    generation = 1

    cam_x, cam_y = 0, 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Atualiza física
        alive_count = 0
        best_car = None
        best_score = -1

        for car in cars:
            car.update()
            if car.alive:
                alive_count += 1
                if car.score > best_score:
                    best_score = car.score
                    best_car = car

        # Câmera segue o melhor carro[cite: 4, 8]
        if best_car:
            target_cam_x = best_car.pos[0] - WIDTH / 2
            target_cam_y = best_car.pos[1] - HEIGHT / 2
            cam_x += (target_cam_x - cam_x) * 0.1
            cam_y += (target_cam_y - cam_y) * 0.1

        # Detecta carros que completaram volta
        finished_cars = [c for c in cars if c.finished]

        # Critério principal: completou volta
        if len(finished_cars) > 0:
            cars = next_generation(cars, track, MUTATION_RATE, generation)
            generation += 1

        # Fallback de segurança (caso ninguém complete)
        elif alive_count == 0:
            cars = next_generation(cars, track, MUTATION_RATE, generation)
            generation += 1

        # Renderização
        screen.fill((20, 24, 30))
        draw_track(screen, track, cam_x, cam_y)

        for car in cars:
            draw_car(screen, car, cam_x, cam_y)

        if best_car:
            draw_telemetry(screen, best_car, font)

        # HUD
        gen_text = font.render(f"Gen: {generation} | Alive: {alive_count}/{NUM_CARS}", True, (255, 255, 255))
        screen.blit(gen_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()