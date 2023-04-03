# cpxctl

```cpxctl``` is a python application that lets you query CPX Server from the command line. You can use ```cpxctl``` to output various information about the services in CPX Server.

## Setup cpxctl
### Create virtual environment
Set up a virtual environment, follow [instructions](https://docs.python.org/3/library/venv.html).

### Install libraries
To install required libraries, run:
```
$ pip install -r requirements.txt
```
## Run cpxctl
To run:
```
$ ./cpxcptl.py <Argument> <Options>
```
### Example commands
1. Print running services to stdout (similar to the table below) 
```
$ cpxctl.py get --all
```
2. Print out average CPU/Memory of services of the same type
```
$ cpxctl.py get --avg
```
3. Flag services which have fewer than 2 healthy instances running 
4. Have the ability to track and print CPU/Memory of all instances of a given service over
time (until the command is stopped, e.g. ctrl + c).
```
$ cpxctl.py get --service <SERVICE_NAME> --w 5
```

## Choices, Trade-offs and Future Improvements

### Choices and Trade-offs
- Selected an iterative process to get info about each server.
- Created a core sort() function which arranges all common service in a list of dictionary with the key as the service name.
- Used sort() as the data source and other functions to process the data and output the result.
- Used argparser library to execute relevant functions based on input.

### Improvements
- Finish challenge command 3 by adding count logic for every healthy server and exit if count > 2. 
- Tidy challenge command 4 by using the --w flag.
- Explore multi-threading to send a batch of REST API calls.
- When adding more functions to CLI, refine the functions to be more modular and re-usable.
- Compile the program into a binary.