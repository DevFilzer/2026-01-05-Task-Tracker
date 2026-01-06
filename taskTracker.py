import json

from os import path
from datetime import datetime

def main():

    args = []
    tasks = loadTask()
    id = idGenerator(tasks)

    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")

        userInput = ""
        while not userInput:
            userInput = input("?  ")

        if userInput.strip().lower() == "exit":
            break

        args = userInput.split()

        match args[0]:
            case "add":
                  addTask(tasks, id, args, now)
                  new_id = max([task["id"] for task in tasks])
                  print(f"Task added successfuly (ID: {new_id})")
            case "update":
                  updateTask(tasks, args, now)
            case "delete":
                  deleteTask(tasks, args)
            case "mark-done":
                  markTaskDone(tasks, args)
            case "mark-in-progress":
                  markTaskInProgress(tasks, args)
            case "list":
                  listTask(tasks, args)
            case _:
                  print("Usage:\n" \
                  "add {task-description}\n" \
                  "update {task-id} {task-description}\n" \
                  "delete {task-id}\n" \
                  "mark-done {task-id}\n" \
                  "mark-in-progress {task-id}\n" \
                  "list (list all tasks)\n" \
                  "list done\n" \
                  "list todo\n" \
                  "list in-progress\n" \
                  "exit")

        userInput = ""
        

def idGenerator(tasks):
    if len(tasks) == 0:
         i = 0
    else:
         i = max([task["id"] for task in tasks])
    while True:
        i += 1
        yield i

def loadTask():
    if path.exists("tasks.json"):
                with open("tasks.json", "r") as taskFile:
                    tasks = json.load(taskFile)
                    return tasks
    else:
         return []

def storeTask(tasks):
    with open("tasks.json", "w") as taskFile:
        json.dump(tasks, taskFile, indent=4)

def addTask(tasks, id, args, time):
    newTask = {
                "id" : next(id),
                "description" : " ".join(args[1:]),
                "status" : "todo",
                "createdAt" : time,
                "updatedAt" : time
            }
    tasks.append(newTask)
    storeTask(tasks)

def updateTask(tasks, args, time):
    for task in tasks:
        if int(args[1]) == task["id"]:
            task["description"] = " ".join(args[2:])
            task["updatedAt"] = time
            storeTask(tasks)

def deleteTask(tasks, args):
    tasks[:] = [task for task in tasks if task["id"] != int(args[1])]
    storeTask(tasks)

def markTaskDone(tasks, args):
    for task in tasks:
        if int(args[1]) == task["id"]:
            task["status"] = "done"
            storeTask(tasks)

def markTaskInProgress(tasks, args):
    for task in tasks:
        if int(args[1]) == task["id"]:
            task["status"] = "in-progress"
            storeTask(tasks)

def listTask(tasks, args):
    if len(args) == 0:
        print("No tasks found.")
    elif len(args) == 1:
        for task in tasks:
            print(f"Task id: [{task['id']}]\n Description: [{task['description']}]\n Status: [{task['status']}]")
    elif len(args) > 1:
        updatedList = [task for task in tasks if task["status"] == args[1]]
        for items in updatedList:
                print(f"Task id: [{items['id']}]\n Description: [{items['description']}]\n Status: [{items['status']}]")
                 
          
if __name__ == "__main__":
    main()