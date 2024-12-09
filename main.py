import matplotlib.pyplot as plt
import time
import numpy as np
import random

n = 50 # No. of solutions in the population.
added = 2000 # Arbitrary no. added to fitness/evaluation.
mutation_rate = 0.80
generations = 100 #N No. of generations/loop

""" ****************** GENETIC FUNCTIONS *********************** """
def fitness(w, x, y, z):
    return w**3 + x**2 - y**2 - z**2 + (2 * y * z) - (3 * w * x) + (w * z) - (x * y) + 2

def bin_to_dec(list_bin):
    decimal = 0
    for i in range(len(list_bin)):
        digit = list_bin.pop()
        if digit == "1":
            decimal = decimal + pow(2, 1)
    
    return decimal
    
def evaluation(solution):
    w = bin_to_dec(solution[0:4])
    x = bin_to_dec(solution[4:8])
    y = bin_to_dec(solution[8:12])
    z = bin_to_dec(solution[12:16])
    fit = fitness(w, x, y, z)
    return fit
    
def averaging(added, fitness):
    increased = [x + added for x in fitness]
    average = sum(increased)/len(increased)
    averaging = [x/average for x in increased]

    return averaging

# Use for single-point crossover.
def substring_swap(sol1, sol2):
    dimension = len(sol1)
    index = random.randint(0, dimension - 1)
    
    print(f"Index of swapping: {index}")
    offspring1 = sol1[0:index] + sol2[index:] 
    offspring2 = sol2[0:index] + sol1[index:] 
    
    return offspring1, offspring2 
    
def mutation(sol):
    dimension = len(sol)
    index1 = random.randint(0, dimension - 1)

    new_sol = sol
    
    if new_sol[index1] == '1': new_sol[index1] = '0'
    else: new_sol[index1] = '1'
    
    return new_sol

def select_parent(random_number, wheel):
    dimension = len(wheel)
    for i in range(dimension):
        if random_number > wheel[i][0]:
            if random_number < wheel[i][1]:
                return i + 1
            else: continue
""" *********************************************************** """

""" ******************* GENERATING FUNCTION ****************** """
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
""" *********************************************************** """

""" POPULATION GENERATION """
popn = generate_population(n)
print("The Solutions")
for i in range(n):
    print(popn[i])

""" FITNESS VALUE CALCULATION """
fitness_value = []
for i in range(n):
    fit = evaluation(popn[i])
    fitness_value.append(fit)
print("\nThe Evaluation")
print(fitness_value)

""" KEEP TRACK OF BEST """
all_fitness = []
index_best = np.argmax(fitness_value)
super_best_sol = popn[index_best]
super_best_fitness = max(fitness_value)
print("\nBest Solution: ", super_best_sol)
print("\nBest Solution: ", super_best_fitness)
all_fitness.append(super_best_fitness)
super_best_time = []
super_best_time_generation = [] 

# Track what time the iteration started.
start_seconds = time.time()
start_seconds_local_time = time.localtime(start_seconds).tm_sec

for j in range(generations):
    print(f"\nGeneration : {j}")

    # Calculate the strength of each solution.
    ave = averaging(added, fitness_value)

    # Convert averaging into strength percentages.
    strength = [x/sum(ave) for x in ave]
    # print("\nThe Strength")
    # print(strength)

    wheel = generate_wheel(strength)
    # print("\nThe Wheel")
    # print(wheel)

    # Recombination using single-point crossover. 
    new_population = []
    for i in range(int(n/2)):
        parent1 = select_parent(random.random(), wheel)
        parent2 = select_parent(random.random(), wheel)
        print(f"\nParents {parent1} and {parent2}")

        print("\nRecombination: ", i)
        print("Before Swapping")
        print(f"Parent 1 {popn[parent1-1]}")
        print(f"Parent 2 {popn[parent2-1]}")
        print(f"Fitness Parent 1 : {evaluation(popn[parent1-1])}")
        print(f"Fitness Parent 2 : {evaluation(popn[parent2-1])}")
        child1, child2 = substring_swap(popn[parent1-1], popn[parent2-1])
        print("After Swapping")
        print(f"child1 : {child1}")
        print(f"child2 : {child2}")
        print(f"Fitness child1 : {evaluation(child1)}") 
        print(f"Fitness child2 : {evaluation(child2)}") 
        new_population.append(child1)
        new_population.append(child2)

    # print("New Solutions")
    # for i in range(n):
    #     print(new_population[i])

    # CALCULATE FITNESS 
    fitness_value = []
    for i in range(n):
        fit = evaluation(new_population[i])
        fitness_value.append(fit)
    print("\nNew Solution Fitness Evaluation")
    print(fitness_value)

    # MUTATION
    for i in range(n):
        random_number = random.random()
        if random_number < mutation_rate:
            mutatated = mutation(new_population[i])
            new_population[i] = mutatated
    # New population becomes current population.
    popn = new_population

    # print("Mutated Solutions")
    # for i in range(n):
    #     print(new_population[i])

    # CALCULATE FITNESS
    fitness_value = []
    for i in range(n):
        fit = evaluation(new_population[i])
        fitness_value.append(fit)
        
    print("\nMutated Solution Fitness Evaluation")
    print(fitness_value)

    """ DETERMINE THE BEST IN THE GENERATION """
    index_best = np.argmax(fitness_value)
    best_sol_current_gen = new_population[index_best]
    best_fit_current_gen = max(fitness_value)

    """ COMPARE OVERALL BEST """
    if best_fit_current_gen > super_best_fitness: 
        super_best_fitness = best_fit_current_gen
        super_best_sol = best_sol_current_gen
        super_best_time_generation.append(j) 

        # Extract seconds
        seconds = time.time()
        super_best_time_current = time.localtime(seconds).tm_sec

        # Track the time and generation whenever the best is found.
        super_best_time.append(super_best_time_current)

        # Print the time and generation whenever the best is found.
        print(f"Time & Generation the best was found: {super_best_time_current} seconds at Gen {j}")

    print(f"\nBest Solution: {super_best_sol}")
    print(f"Best Fitness: {super_best_fitness}")

    all_fitness.append(super_best_fitness)
    
# Track what time iteration ended.
seconds_end = time.time()
end_seconds_local_time = time.localtime(seconds_end).tm_sec

# Print the time the iteration started.
print(f"\nGenetic Algorithm started local time at {start_seconds_local_time} seconds.\n")

# Print all the Time and Generation where the best was found.
for i in range(len(super_best_time_generation)):
    print(f"Time & Generation the best was found: {super_best_time[i]} seconds at Gen {super_best_time_generation[i]}")

# Print the time the iteration ended.
print(f"\nGenetic Algorithm ended local time at {end_seconds_local_time} seconds.")


print(f"\nAll fitness: {all_fitness}")
plt.plot(all_fitness)
plt.ylabel("Evaluation")
plt.xlabel("Generation No.")
plt.show()