"""Musical Chairs, Game Theory Coursework by C1515888"""
import nashpy as nash
import numpy as np

def rooms_and_stands(chances_list, number_of_rooms):
    """Function uses probabilities to randomly generate the number of practise
        rooms/music stands available for every day of the week.
    Input: probabilities for each floor for each day of the week (list of lists),
        total number of rooms - only number of free rooms when generating
        number of stands (list/list of lists)
    Return: number of free rooms/stands on each floor for each day of the week(list of lists)"""
    free_or_not = [0, 1] #1 is an available room/stand, 0 is no room/stand
    available_list = [] #list to append the lists of available rooms/stands to
    for k in range(7): #runs once for each day of the week
        floor_list = [] #list to append no. available rooms/stands on each floor to
        if len(number_of_rooms) != 3: #when no. rooms changes each day, use kth entry in list
            no_rooms = number_of_rooms[k]
        else:
            no_rooms = number_of_rooms
        for j in range(3): #generates array with no. rooms/stands for each floor
            room_stand_array = np.random.choice(free_or_not, no_rooms[j],
                                                p=[(1-chances_list[k][j]), chances_list[k][j]])
            numbers_of = 0
            for i in room_stand_array: #adds entries in array to get total no. stands/rooms per floor
                numbers_of += i
            floor_list.append(numbers_of) #list of rooms/stands per floor
        available_list.append(floor_list) #list of lists of rooms/stands per floor per day
    return available_list

def matrices(big_room_number_list, small_room_number_list, stand_number_list):
    """Using the number of available rooms/stands generates the matrices for
        player A and player B for each day of the week.
    Input: number of free big rooms on each floor (list of lists),
        number of free small rooms on each floor (list of lists)
        number of free stands on each floor (list of lists)
    Return: row player matrices (list of 7 arrays),
        column player matrices (list of 7 arrays)"""
    row_matrix_list = []#create lists for the arrays
    col_matrix_list = []
    for l in range(7): #runs once for each day of the week
        big_room = big_room_number_list[l]
        small_room = small_room_number_list[l]
        stand_number = stand_number_list[l]
        A = np.empty([3, 3]) #create empty A matrix
        for m in range(3):
            if small_room[m] > 0: #one or more free rooms
                A[m, :] = 1 #assumption: A gets room
            if big_room[m] > 0: #one or more free big rooms
                A[m, :] = 2 #A takes bigger room instead
            if small_room[m] == 0 and big_room[m] == 0: #no free rooms
                A[m, :] = 0
            for n in range(3):
                if stand_number[m] == 1 and A[m, n] > 0: #only one stand, A has room
                    if n != m: #if B is on a different floor, A gets a stand
                        A[m, n] += 2
                    if n == m and (big_room[m]+small_room[m] < 2): #on same floor, but B doesn't have a room
                        A[m, n] += 2
                if stand_number[m] > 1 and A[m, n] > 0: #at least two stands
                    A[m, n] += 2
        row_matrix_list.append(A)
        B = np.empty([3, 3]) #create empty B matrix
        for p in range(3):
            if small_room[p] > 1: #at least two free rooms
                B[:, p] = 1
            if big_room[p] > 1: #at least two big rooms
                B[:, p] = 2 #B takes bigger room
            if big_room[p] == 0 and small_room[p] == 0: #no free rooms
                B[:, p] = 0
            if big_room[p] == 1: #only one big room
                for q in range(3):
                    if q != p: #if A is on a different floor, B gets room
                        B[q, p] = 2
                    if q == p: #A and B on the same floor
                        if small_room[p] > 0: #small room available
                            B[p, p] = 1
                        else:
                            B[p, p] = 0 #assumption A gets room
            if big_room[p] == 0 and small_room[p] == 1: #only one small room
                for q in range(3):
                    if q != p: #if A is on a different floor, B gets room
                        B[q, p] = 1
                    if q == p: #if a is on the same floor, A gets room
                        B[p, p] = 0
            for i in range(3):
                if stand_number[p] > 1 and B[i, p] > 0: #one or more stands
                    B[i, p] += 2 #assumtion B gets stand
                if stand_number[p] == 1 and B[i, p] > 0: #one stand, B has a room
                    B[i, p] += 2 #assumption B gets stand
        col_matrix_list.append(B)
    return row_matrix_list, col_matrix_list

#list of room probabilities in order from mon-sun
room_chances = [[0.1, 0.1, 0.3], [0.4, 0.3, 0.5], [0.1, 0.1, 0.3],
                [0.4, 0.3, 0.5], [0.5, 0.4, 0.6], [0.7, 0.7, 0.9],
                [0.8, 0.8, 0.9]]
#list of stand proabilities in order from mon-sun
stand_chances = [[0.7, 0.6, 0.8], [0, 0, 0.3], [0.2, 0.4, 0.6],
                 [0.7, 0.5, 0.6], [0.5, 0.5, 0.5], [0.7, 0.7, 0.7],
                 [0.8, 0.9, 0.9]]
no_big_rooms_floor = [3, 5, 5] #total number of big practise rooms per floor
no_small_rooms_floor = [1, 5, 5] #total number of small practise rooms per floor

#call function to find the number of free rooms per day
big_room_number_list = rooms_and_stands(room_chances, no_big_rooms_floor)
small_room_number_list = rooms_and_stands(room_chances, no_small_rooms_floor)
print(big_room_number_list)
print(small_room_number_list)
room_number_list = [] #list of total number of free rooms per day
for s in range(7):
    lists = []
    big = big_room_number_list[s]
    small = small_room_number_list[s]
    for t in range(3):
        rooms = big[t] + small[t]
        lists.append(rooms)
    room_number_list.append(lists)
print(room_number_list)

#call function to find the number of available stands per day
stand_number_list = rooms_and_stands(stand_chances, room_number_list)
print(stand_number_list)

#generate matrices
row_matrix_list, col_matrix_list = matrices(big_room_number_list, small_room_number_list,
                                            stand_number_list)
print(row_matrix_list)
print(col_matrix_list)

for r in range(7):
    A = row_matrix_list[r]
    B = col_matrix_list[r]
    musical_rooms = nash.Game(A, B) #create game
    print(musical_rooms)
    equilibs = musical_rooms.support_enumeration() #find nash equilibria
    print(list(equilibs))
    equilib = musical_rooms.vertex_enumeration() #find nash equilibria
    print(list(equilib))
