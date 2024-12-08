import numpy as np
from genetic_functions import *
from functions import *

n = 16 # No. of solutions in the population.
added = 2000 # Arbitrary no. added to fitness/evaluation.
mutation_rate = 0.75
generations = 30 #N No. of generations/loop

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

""" Keep track of best """
all_fitness = []
index_best = np.argmax(fitness_value)
super_best_sol = popn[index_best]
super_best_fitness = max(fitness_value)
print("\nBest Solution: ", super_best_sol)
print("\nBest Solution: ", super_best_fitness)
all_fitness.append(super_best_fitness)

for j in range(generations):
    print(f"\nGeneration : {j}")

    # Calculate the strength of each solution.
    ave = averaging(added, fitness_value)

    # Convert averaging into strength percentages.
    strength = [x/sum(ave) for x in ave]
    print("\nThe Strength")
    print(strength)

    wheel = generate_wheel(strength)
    print("\nThe Wheel")
    print(wheel)

    # Recombination
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

    print("New Solutions")
    for i in range(n):
        print(new_population[i])

    # CALCULATE FITNESS 
    fitness_value = []
    for i in range(n):
        fit = evaluation(new_population[i])
        fitness_value.append(fit)
    print("\nThe Evaluation")
    print(fitness_value)

    # MUTATION
    for i in range(n):
        random_number = random.random()
        if random_number < mutation_rate:
            mutatated = mutation(new_population[i])
            new_population[i] = mutatated
    # New population becomes current population.
    popn = new_population

    print("Mutated Solutions")
    for i in range(n):
        print(new_population[i])

    # CALCULATE FITNESS
    fitness_value = []
    for i in range(n):
        fit = evaluation(new_population[i])
        fitness_value.append(fit)
        
    print("\nEvaluation")
    print(fitness_value)

    # DETERMINE THE BEST IN THE GENERATIONk
    index_best = np.argmax(fitness_value)
    best_sol_current_gen = new_population[index_best]
    best_fit_current_gen = max(fitness_value)

    # COMPARE OVERALL BEST
    if best_fit_current_gen > super_best_fitness: 
        super_best_fitness = best_fit_current_gen
        super_best_sol = best_sol_current_gen

    print(f"\nBest Solution: {super_best_sol}")
    print(f"Best Fitness {super_best_fitness}")

    all_fitness.append(super_best_fitness)

print(all_fitness)