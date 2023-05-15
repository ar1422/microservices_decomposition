# Microservices Extraction 

This application is designed for extraction of Microservices from the given Monoltihic

## Features of the Application – 
   * User can specify the application Github link which is the input to the application.
   * User can any coupling strategy from Logical Coupling, Semantic Coupling, Contributor Coupling and Structural 
   similarity coupling.
   * User can specify the number of clusters the output should have.
   
   
## Technical details of the application - 

   * Python is used to develop the application.
        
      
 ## Structure and design of the code - 
   
   * The coupling_logic directory contains all the coupling strategy code.
   * The clustering.py is used for performing clustering step using Minimum Spanning Tree(MST)
   * app.py is the entry function for the application
   
## Installation

#### Requirements
 * GitPython==3.1.31
 * nltk==3.4.5
 * scikit_learn==1.2.2
 * networkx~=2.4
 * scikit-learn~=0.22.1

     
## Usage


To start the web-services, please run the command - 
```python
    python app.py <localpath>
```
    