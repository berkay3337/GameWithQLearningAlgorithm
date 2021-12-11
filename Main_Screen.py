from tkinter import Tk, Label, Text, Button
import numpy as np
import random
import numpy as np
from matplotlib import pyplot as plt



def is_terminal_state(current_row_index, current_column_index):
    
    if output_matrix[current_row_index, current_column_index] == -1:
        return False
    else:
        return True

def get_starting_location():
    
    current_row_index = np.random.randint(environment_rows)
    current_column_index = np.random.randint(environment_columns)
    
    while is_terminal_state(current_row_index, current_column_index):
        current_row_index = np.random.randint(environment_rows)
        current_column_index = np.random.randint(environment_columns)
    return current_row_index, current_column_index

def get_next_action(current_row_index, current_column_index, epsilon):
    
    if np.random.random() < epsilon:
        return np.argmax(q_values[current_row_index, current_column_index])
    else:  
        return np.random.randint(8)

def get_next_location(current_row_index, current_column_index, action_index):
    
    new_row_index = current_row_index
    new_column_index = current_column_index

    if actions[action_index] == 'north' and current_row_index > 0:
        new_row_index -= 1
    elif actions[action_index] == 'east' and current_column_index < environment_columns - 1:
        new_column_index += 1
    elif actions[action_index] == 'south' and current_row_index < environment_rows - 1:
        new_row_index += 1
    elif actions[action_index] == 'west' and current_column_index > 0:
        new_column_index -= 1
    elif actions[action_index] == 'northeast' and current_row_index > 0 and current_column_index < environment_columns - 1:
        new_row_index -= 1
        new_column_index += 1
    elif actions[action_index] == 'southeast' and current_row_index < environment_rows - 1 and current_column_index < environment_columns - 1:
        new_row_index += 1
        new_column_index += 1
    elif actions[action_index] == 'southwest' and current_row_index < environment_rows - 1 and current_column_index > 0:
        new_row_index += 1
        new_column_index -= 1
    elif actions[action_index] == 'northwest' and current_row_index > 0 and current_column_index > 0:
        new_row_index -= 1
        new_column_index -= 1

    return new_row_index, new_column_index

def get_shortest_path(start_row_index, start_column_index):
    
    print(start_row_index, start_column_index)
    if is_terminal_state(start_row_index, start_column_index):
        return []
    else:  
        current_row_index, current_column_index = start_row_index, start_column_index
        shortest_path = []
        shortest_path.append([current_row_index, current_column_index])
        
        while not is_terminal_state(current_row_index, current_column_index):
            
            action_index = get_next_action(current_row_index, current_column_index, 1.)
            current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
            shortest_path.append([current_row_index, current_column_index])
        return shortest_path


def Take_input():
    
    start = t1.get("1.0", "end-1c")
    reward_array = []
    total_reward= 0
    end = t2.get("1.0", "end-1c")
    shortest_way = []
    loop = 0
    step = []
    output = open("‪output.txt", "w")
    print(start, end)
    labels[int(start)-1].config(bg="green")
    labels[int(end)-1].config(bg="green")
    output_matrix[(int(end) % 600)-1][24] = 100
    epsilon = 0.9
    discount_factor = 0.9  
    learning_rate = 0.9  


    for episode in range(5000):
       
        row_index, column_index = get_starting_location()
        step.append(loop)
        reward_array.append(total_reward)
        total_reward = 0
        loop = 0

        while not is_terminal_state(row_index, column_index):
            
            action_index = get_next_action(row_index, column_index, epsilon)

          
            old_row_index, old_column_index = row_index, column_index
            row_index, column_index = get_next_location(row_index, column_index, action_index)

           
            reward = output_matrix[row_index, column_index]
            total_reward = total_reward + reward
            old_q_value = q_values[old_row_index, old_column_index, action_index]
            temporal_difference = reward + \
            (discount_factor *np.max(q_values[row_index, column_index])) - old_q_value

            
            new_q_value = old_q_value + \
                (learning_rate * temporal_difference)
            q_values[old_row_index, old_column_index,action_index] = new_q_value
            loop = loop+1
    

    print('Training complete!')

    shortest_way = get_shortest_path(int(start)-1, 0)
    print(shortest_way)

    for i in range(25):
        for j in range(25):
            if(output_matrix[i][j] == -100):
                output.write("(")
                output.write(str(i))
                output.write(",")
                output.write(str(j))
                output.write("Kırmızı")
                output.write(")")
                output.write(" ")
            if(output_matrix[i][j] == -1):
                output.write("(")
                output.write(str(i))
                output.write(",")
                output.write(str(j))
                output.write("Beyaz")
                output.write(")")
                output.write(" ")
            if(output_matrix[i][j] == 100):
                output.write("(")
                output.write(str(i))
                output.write(",")
                output.write(str(j))
                output.write("Yeşil")
                output.write(")")
                output.write(" ")
        output.write("\n")

    for i in range(len(shortest_way)):
        for j in range(len(shortest_way)):
            for k in range(len(shortest_way)):
                if ([j, i] == shortest_way[k]):
                    labels_matrix[i][j].config(bg="yellow")

    
    plt.plot(range(0, 5000), step)
    plt.ylabel('Adım Sayısı')
    plt.xlabel('Episode')
    plt.show()

    plt.plot(range(0, 5000), reward_array)
    plt.ylabel('Maliyet')
    plt.xlabel('Episode')
    plt.show()

                    

output_matrix = np.empty((25, 25))
labels_matrix = np.empty((25, 25))
labels = []
ran_num = []
start_end = []
index = 0
goal = 0
control = 0
number = 1
x = 5
y = 5
start = 0
environment_rows = 25
environment_columns = 25
q_values = np.zeros((environment_rows, environment_columns, 8))
barrier = "red"
route = "white"
end = 0
actions = ['north', 'east', 'south', 'west',
           'northeast', 'southeast', 'southwest', 'northwest']


for i in range(250):

    ran_num.append(random.randint(1, 625))


start_end.append(random.randint(1, 25))
start_end.append(random.randint(601, 625))


window = Tk()
window.geometry("1750x900")

for l in range(625):
    w = Label(window, text=str(l+1),
              fg="black",
              bg="white",
              width=5,
              height=1,
              font="Verdana 10 bold")
    w.place(x=x, y=y)
    y = y + 25
    control = control+1
    labels.append(w)
    if(control == 25):
        x = x+70
        y = 5
        control = 0

t1 = Text(window, height=2, width=20)
t1_lbl = Label(window, text="Başlangıç Noktası", height=2, width=15)
t1.place(x=600, y=670)
t1_lbl.place(x=600, y=630)

t2 = Text(window, height=2, width=20)
t2_lbl = Label(window, text="Bitiş Noktası", height=2, width=15)
t2.place(x=900, y=670)
t2_lbl.place(x=900, y=630)

for i in range(250):
    labels[ran_num[i]-1].config(bg="red")
    labels[start_end[0]-1].config(bg="white")
    labels[start_end[1]-1].config(bg="white")

labels_matrix = np.reshape(labels, (25, 25))

for i in range(25):
    for j in range(25):
        if(labels_matrix[j][i].cget("background") == "red"):
            output_matrix[i][j] = -100
        if(labels_matrix[j][i].cget("background") == "white"):
            output_matrix[i][j] = -1
        if(labels_matrix[j][i].cget("background") == "green"):

            if(control == 0):
                output_matrix[i][j] = -1

            if(control == 1):
                output_matrix[i][j] = -1

            control = control + 1

btn = Button(window, text='Seç',
             fg="black",
             bg="yellow",
             width=5,
             height=2,
             font="Verdana 10 bold",
             command=lambda: Take_input())

btn.place(x=800, y=720)
window.mainloop()
