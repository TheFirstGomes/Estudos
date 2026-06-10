import math
import numpy as np

# Somente para testes
OVAL_POINTS = [
    [0.2, 0.2], [0.8, 0.2], [0.9, 0.3], [0.9, 0.7],
    [0.8, 0.8], [0.2, 0.8], [0.1, 0.7], [0.1, 0.3]
]

# Suzuka
MONACO_POINTS = [
    [112.72, -296.78], [141.68, -358.45], [228.3, -476.12], [261.68, -477.79],
    [268.28, -456.97], [279.14, -424.69], [298.04, -391.51], [318.47, -398.86],
    [313.16, -472], [357.8, -484.46], [365.28, -403.09], [344.45, -291.44],
    [289.03, -195.14], [206.91, -128.69], [122.62, -88.61], [30.2, -62.67],
    [-24.09, -53.54], [-39.05, -29.5], [-62.78, -34.73], [-168.87, -22.15],
    [-263.53, -7.9], [-290.48, 1.67], [-314.45, 56.66], [-320.24, 92.06],
    [-320.08, 140.15], [-299.16, 162.19], [-285.73, 190.02], [-271.58, 271.95],
    [-267.15, 297], [-286.7, 311.36], [-287.02, 328.62], [-261.2, 391.07],
    [-215.19, 437.82], [-188.97, 452.4], [-186.72, 472.33], [-240.21, 486.91],
    [-267.23, 481.01], [-271.17, 467.99], [-292.41, 430.81], [-314.45, 395.97],
    [-347.26, 288.99], [-357.8, 236.44], [-367.85, 145.27], [-366.41, 85.94],
    [-352.97, 23.93], [-349.51, -9.02], [-340.02, -25.83], [-307.77, -30.61],
    [-257.9, -36.85], [-166.69, -60.67], [-96.56, -76.14], [-55.62, -84.49],
    [-3.74, -109.09], [52.24, -125.9], [106.45, -134.25], [155.11, -167.2],
    [167.9, -195.48], [159.05, -240.56], [128.57, -275.18]
]


class Track:
    def __init__(self):
        self.scale = 1.0
        self.width = 17 * self.scale
        self.points = [(p[0] * self.scale, p[1] * self.scale) for p in MONACO_POINTS]
        self.total_length = self.compute_total_length()

    def compute_total_length(self):
        total = 0
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            total += math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        return total

    def get_start_pos(self):
        # Calcula ângulo inicial[cite: 6]
        p0, p1 = self.points[0], self.points[1]
        angle = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
        return {"pos": p0, "angle": angle}

    def is_on_track(self, x, y):
        # Verifica se (x,y) está dentro dos limites da pista
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            if self._dist_to_segment(x, y, p1, p2) < self.width:
                return True
        return False

    def cast_ray(self, x, y, angle, max_len=220):
        # Lógica de sensor: avança passo a passo até sair da pista[cite: 6]
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        for d in range(0, max_len, 4):
            if not self.is_on_track(x + cos_a * d, y + sin_a * d):
                return d
        return max_len

    def get_progress(self, x, y):
        best_proj = 0
        best_dist = float('inf')
        total_len = 0

        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]

            dx, dy = p2[0] - p1[0], p2[1] - p1[1]
            seg_len = math.hypot(dx, dy)

            if seg_len == 0:
                continue

            t = ((x - p1[0]) * dx + (y - p1[1]) * dy) / (seg_len ** 2)
            t = max(0, min(1, t))

            proj_x = p1[0] + t * dx
            proj_y = p1[1] + t * dy

            dist = (x - proj_x) ** 2 + (y - proj_y) ** 2

            if dist < best_dist:
                best_dist = dist
                best_proj = total_len + t * seg_len

            total_len += seg_len

        return best_proj

    def _dist_to_segment(self, px, py, a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        l2 = dx ** 2 + dy ** 2
        if l2 == 0: return math.sqrt((px - a[0]) ** 2 + (py - a[1]) ** 2)
        t = max(0, min(1, ((px - a[0]) * dx + (py - a[1]) * dy) / l2))
        return math.sqrt((px - (a[0] + t * dx)) ** 2 + (py - (a[1] + t * dy)) ** 2)