# About
This repository contains the solution for the Python programming task as 
part of the AI at BioXcel Internship interview.


## Running the Program
To run the program, you need to have Docker installed.

1. Build the Docker container:
```
docker build -t compound-normalizer .
```

2. Run the Docker container using the created code:
```
docker run compound-normalizer
```


## Repository Structure
- `compound_data.xlsx`: Contains additional compound properties for the bonus task.
- `Dockerfile`: Docker configuration file for building the container.
- `name_normalization.py`: Python source code of the task solution.
- `requirements.txt`: List of required Python packages.
- `variants_mapping.json`: JSON template for name normalization.