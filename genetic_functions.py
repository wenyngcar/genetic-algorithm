import random

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

def substring_swap(sol1, sol2):
    dimension = len(sol1)
    index1 = random.randint(0, dimension - 1)
    index2 = random.randint(0, dimension - 1)

    # Positions should not be the same.
    while index1 ==  index2:
        index1 = random.randint(0, dimension - 1)

    if index1 < index2:
        left = index1
        right = index2
    else:
        left = index2
        right = index1
    
    baby1 = sol1[0:left] + sol2[left:right + 1] + sol1[right+1:dimension]
    baby2 = sol2[0:left] + sol1[left:right + 1] + sol2[right+1:dimension]

    return baby1, baby2
    
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