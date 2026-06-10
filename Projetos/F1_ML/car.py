import math
import numpy as np
from neural_network import NeuralCar

class Car:
    def __init__(self, track, brain=None):
        self.track = track
        start = track.get_start_pos()
        self.pos = list(start['pos'])
        self.angle = start['angle']

        self.speed = 0
        self.alive = True
        self.score = 0
        self.prev_progress = 0
        self.stuck_frames = 0

        self.laps = 0
        self.finished = False

        self.last_delta = 0
        self.last_reward = 0

        self.brain = brain if brain else NeuralCar()

        self.sensor_angles = [-math.pi/2, -math.pi/4, -math.pi/8, 0, math.pi/8, math.pi/4, math.pi/2]
        self.sensors = np.zeros(len(self.sensor_angles))
        self.sensor_length = 220

    def update(self):
        if not self.alive:
            return

        for i, angle_offset in enumerate(self.sensor_angles):
            d = self.track.cast_ray(self.pos[0], self.pos[1], self.angle + angle_offset, self.sensor_length)
            self.sensors[i] = d / self.sensor_length

        inputs = list(self.sensors) + [self.speed / 5.0, 1.0]

        decision = self.brain.think(inputs)
        steer, gas = decision['steer'], decision['gas']

        self.angle += steer * 0.12
        self.speed = max(0, 2.0 + (gas + 1) * 2.5)

        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        if not self.track.is_on_track(self.pos[0], self.pos[1]):
            self.alive = False
            return

        progress = self.track.get_progress(self.pos[0], self.pos[1])
        delta = progress - self.prev_progress

        track_len = self.track.total_length

        if delta < -track_len * 0.5:
            delta += track_len
        elif delta > track_len * 0.5:
            delta -= track_len

        # detectar volta completa
        if self.prev_progress > track_len * 0.9 and progress < track_len * 0.1:
            self.laps += 1
            self.finished = True

        front_sensor = self.sensors[3]

        reward = (delta * 10) + (self.speed * 0.1) - (abs(steer) ** 2) * 0.02
        reward -= (1 - front_sensor) * self.speed * 0.2

        self.score += reward

        self.last_delta = delta
        self.last_reward = reward

        if delta > 0:
            self.stuck_frames = 0
        else:
            self.stuck_frames += 1

        if self.stuck_frames > 150:
            self.alive = False

        self.prev_progress = progress