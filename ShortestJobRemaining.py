#SJF - Shortest Job First
processes = []
number = int(input("Enter number of processes: "))

#Ask for each process
for i in range(number):
    name = input("Enter Process name: ")

    burst = int(input("Enter Burst Time: "))

    processes.append([name,burst])

    #Sort by shortest burst time
    processes.sort(key=lambda x: x[1])

    print("\nExecution Processes:")

for process in processes:
    print(process[0],end=" -> ")

print("\n\nGarnt Chart: ")

time = 0

for process in processes:
    name = process[0]
    burst = process[1]

    print(time, " -> ",name, " -> ", time + burst)
    time += burst