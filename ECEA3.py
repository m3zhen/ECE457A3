import math

max_iterations = 10
N = 20
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
        for j in range(i+1, N):
            cost += flow[permutation[i]][permutation[j]] * distance[i][j]
    return cost

for k in range(max_iterations):
    tabu = [[0 for x in range(N)] for y in range(N)] 
    solution_set = []
    for i in solution:
        for j in range(i+1, N):
            # swap positions of solution
            solution_copy = solution
            solution_copy[i], solution_copy[j] = solution_copy[j], solution_copy[i]

            # store calculated cost in solution_set array in the for {(swapped flow indices): cost}
            solution_set.append({"swapped" : (min(solution_copy[i],solution_copy[j]), max(solution_copy[i],solution_copy[j])), "cost" : calculate_cost(solution_copy)})
            solution_set = sorted(solution_set, key=lambda d: d['cost'])

    # decrement all tabu values by 1
    for i in range(N):
        for j in range(N):
            if tabu[i][j] > 0:
                tab[i][j] -= 1

    # take lowest cost swap from solution_set (which isn't in tabu) and apply swap
    for i in range(len(solution_set)):
        idx1 = solution_set[i]["swapped"][0]
        idx2 = solution_set[i]["swapped"][1]
        if tabu[idx1][idx2] == 0:
            # perform swap and set tabu value
            solution[idx1], solution[idx2] = solution[idx2], solution[idx1]
            tabu[idx1][idx2] += ban_count
            break

    print("iteration", k)
    print(solution)
    print(calculate_cost(solution))
