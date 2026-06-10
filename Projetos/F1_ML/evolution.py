import numpy as np
from car import Car
from neural_network import NeuralCar

def crossover(b1, b2):
    w1a, b1a, w2a, b2a = b1.get_weights().values()
    w1b, b1b, w2b, b2b = b2.get_weights().values()

    def mix(a, b):
        mask = np.random.rand(*a.shape) > 0.5
        return np.where(mask, a, b)

    return {'w1': mix(w1a, w1b), 'b1': mix(b1a, b1b), 'w2': mix(w2a, w2b), 'b2': mix(b2a, b2b)}

def next_generation(cars, track, base_mutation, generation):
    cars = sorted(cars, key=lambda c: c.score, reverse=True)
    elite_count = max(2, len(cars)//5)
    elites = cars[:elite_count]

    mutation_rate = base_mutation * (0.995 ** generation)

    new_cars = []

    for c in elites:
        new_cars.append(Car(track, c.brain))

    while len(new_cars) < len(cars):
        p1, p2 = np.random.choice(elites, 2, replace=False)
        child_w = crossover(p1.brain, p2.brain)
        brain = NeuralCar(child_w)
        brain.mutate(mutation_rate)
        new_cars.append(Car(track, brain))

    return new_cars