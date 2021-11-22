import math
import random

random.seed(10)

max_iterations = 50
N = 20
best_so_far_criteria = False
best_neighbourhood_criteria = False
dynamic_tabu_list = False
ban_count = math.floor(math.sqrt(N))

flow = [
    [0,0,5,0,5,2,10,3,1,5,5,5,0,0,5,4,4,0,0,1],
    [0,0,3,10,5,1,5,1,2,4,2,5,0,10,10,3,0,5,10,5],
    [5,3,0,2,0,5,2,4,4,5,0,0,0,5,1,0,0,5,0,0],
    [0,10,2,0,1,0,5,2,1,0,10,2,2,0,2,1,5,2,5,5],
    [5,5,0,1,0,5,6,5,2,5,2,0,5,1,1,1,5,2,5,1],
    [2,1,5,0,5,0,5,2,1,6,0,0,10,0,2,0,1,0,1,5],
    [10,5,2,5,6,5,0,0,0,0,5,10,2,2,5,1,2,1,0,10],
    [3,1,4,2,5,2,0,0,1,1,10,10,2,0,10,2,5,2,2,10],
    [1,2,4,1,2,1,0,1,0,2,0,3,5,5,0,5,0,0,0,2],
    [5,4,5,0,5,6,0,1,2,0,5,5,0,5,1,0,0,5,5,2],
    [5,2,0,10,2,0,5,10,0,5,0,5,2,5,1,10,0,2,2,5],
    [5,5,0,2,0,0,10,10,3,5,5,0,2,10,5,0,1,1,2,5],
    [0,0,0,2,5,10,2,2,5,0,2,2,0,2,2,1,0,0,0,5],
    [0,10,5,0,1,0,2,0,5,5,5,10,2,0,5,5,1,5,5,0],
    [5,10,1,2,1,2,5,10,0,1,1,5,2,5,0,3,0,5,10,10],
    [4,3,0,1,1,0,1,2,5,0,10,0,1,5,3,0,0,0,2,0],
    [4,0,0,5,5,1,2,5,0,0,0,1,0,1,0,0,0,5,2,0],
    [0,5,5,2,2,0,1,2,0,5,2,1,0,5,5,0,5,0,1,1],
    [0,10,0,5,5,1,0,2,0,5,2,2,0,5,10,2,2,1,0,6],
    [1,5,0,5,1,5,10,10,2,2,5,5,5,0,10,0,0,1,6,0],
]

distance = [
    [0,1,2,3,4,1,2,3,4,5,2,3,4,5,6,3,4,5,6,7],
    [1,0,1,2,3,2,1,2,3,4,3,2,3,4,5,4,3,4,5,6],
    [2,1,0,1,2,3,2,1,2,3,4,3,2,3,4,5,4,3,4,5],
    [3,2,1,0,1,4,3,2,1,2,5,4,3,2,3,6,5,4,3,4],
    [4,3,2,1,0,5,4,3,2,1,6,5,4,3,2,7,6,5,4,3],
    [1,2,3,4,5,0,1,2,3,4,1,2,3,4,5,2,3,4,5,6],
    [2,1,2,3,4,1,0,1,2,3,2,1,2,3,4,3,2,3,4,5],
    [3,2,1,2,3,2,1,0,1,2,3,2,1,2,3,4,3,2,3,4],
    [4,3,2,1,2,3,2,1,0,1,4,3,2,1,2,5,4,3,2,3],
    [5,4,3,2,1,4,3,2,1,0,5,4,3,2,1,6,5,4,3,2],
    [2,3,4,5,6,1,2,3,4,5,0,1,2,3,4,1,2,3,4,5],
    [3,2,3,4,5,2,1,2,3,4,1,0,1,2,3,2,1,2,3,4],
    [4,3,2,3,4,3,2,1,2,3,2,1,0,1,2,3,2,1,2,3],
    [5,4,3,2,3,4,3,2,1,2,3,2,1,0,1,4,3,2,1,2],
    [6,5,4,3,2,5,4,3,2,1,4,3,2,1,0,5,4,3,2,1],
    [3,4,5,6,7,2,3,4,5,6,1,2,3,4,5,0,1,2,3,4],
    [4,3,4,5,6,3,2,3,4,5,2,1,2,3,4,1,0,1,2,3],
    [5,4,3,4,5,4,3,2,3,4,3,2,1,2,3,2,1,0,1,2],
    [6,5,4,3,4,5,4,3,2,3,4,3,2,1,2,3,2,1,0,1],
    [7,6,5,4,3,6,5,4,3,2,5,4,3,2,1,4,3,2,1,0],
]

# index of solution represents the location number
# values of the solution represents the facility number
solution = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

def calculate_cost(permutation):
    cost = 0
    for i in range(len(permutation)):
        for j in range(len(permutation)):
            cost += flow[permutation[i]][permutation[j]] * distance[i][j]
    return cost

def TS():
    change_count = 10
    dynamic_ban_count = random.randint(1,10)

    best_so_far = float('inf')

    tabu = [[0 for x in range(N)] for y in range(N)] 
    for k in range(max_iterations):
        solution_set = []

        print("****************Iteration", k, " ***************************")
        print(solution)
        print(calculate_cost(solution))

        for i in solution:
            for j in range(i+1, N):
                # swap positions of solution
                solution_copy = list(solution)
                solution_copy[i], solution_copy[j] = solution_copy[j], solution_copy[i]

                # store calculated cost in solution_set array in the for {(swapped flow indices): cost}
                solution_set.append({"swap department values" : (min(solution_copy[i],solution_copy[j]), max(solution_copy[i],solution_copy[j])), "swap indices" : (i,j), "cost" : calculate_cost(solution_copy)})
                solution_set = sorted(solution_set, key=lambda d: d['cost'])
        print("top candidates: ", solution_set[:5])
        # decrement all tabu values by 1
        for i in range(N):
            for j in range(N):
                if tabu[i][j] > 0:
                    print("tabu index: ", (i,j), "tabu value: ", tabu[i][j])
                    tabu[i][j] -= 1

        # take lowest cost swap from solution_set (which isn't in tabu) and apply swap
        for i in range(len(solution_set)):
            idx1 = solution_set[i]["swap indices"][0]
            idx2 = solution_set[i]["swap indices"][1]
            val1 = solution_set[i]["swap department values"][0]
            val2 = solution_set[i]["swap department values"][1]
            if tabu[val1][val2] == 0 or best_neighbourhood_criteria or (best_so_far_criteria and solution_set[i]["cost"] <= best_so_far):
                print("swapped index: ", idx1, ",", idx2)
                print("swapped value: ", val1, ",", val2)

                # perform swap and set tabu value
                solution[idx1], solution[idx2] = solution[idx2], solution[idx1]

                if(not dynamic_tabu_list):
                    tabu[val1][val2] = ban_count
                else:
                    if(change_count == 0): 
                        dynamic_ban_count = random.randint(1,10)
                        change_count = 10
                    change_count -= 1

                    tabu[val1][val2] = dynamic_ban_count
                    

                if(best_so_far_criteria and solution_set[i]["cost"] <= best_so_far):
                    best_so_far = solution_set[i]["cost"]
                break
        
    print("--------------------------------------------------------------------------------")
    return(calculate_cost(solution))

# Base TS Function
ts = TS()

# # 10 variations of initial solution
initial_variations = []
for l in range(10):
    random.shuffle(solution)
    initial_variations.append(TS())

# # check with varying tabu tenure
solution = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
ban_count = 2
tenureLow = TS()
solution = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
ban_count = 9
tenureHigh = TS()

#check with dynamic tabu list size
solution = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
dynamic_tabu_list = True
dynamicTabu = TS()

# check with aspiration criterias
solution = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
best_neighbourhood_criteria = True
best_neighbourhood_res = TS()
best_neighbourhood_criteria = False

solution = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
best_so_far_criteria = True
best_so_far_res = TS()
best_so_far_criteria = False


print("base ts function: ", ts)

print("Costs of variations: ", initial_variations)

print("Costs with tenure 2: ", tenureLow)

print("Costs with tenure 9: ", tenureHigh)

print("Dyamic tabu list size: ", dynamicTabu)

print("best in neighbourhood aspiration: ", best_neighbourhood_res)

print("best so far aspiration: ", best_so_far_res)