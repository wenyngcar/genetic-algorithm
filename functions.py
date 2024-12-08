import random

def generate_population(n):
    population = []
    for _ in range(n):  # Use underscore (_) for a variable that's not used
        # Generate binary strings for w, x, y, z
        solution = []
        for _ in range(4):  # Loop for generating 16 binary values directly
            solution.extend(['1' if random.random() < 0.5 else '0' for _ in range(4)])
        population.append(solution)
    return population
        
def generate_wheel(strength: list) -> list:
    wheel = []
    pair = []
    dimension = len(strength)
    start = 0.0
    end = strength[0]
    pair.append(start)
    pair.append(end)
    wheel.append(pair)

    for num in range(dimension):
        pair = []
        if num != 0:
            start = end
            end = start + strength[num]
            pair.append(start)
            pair.append(end)
            wheel.append(pair)
    
    return wheel