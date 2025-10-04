from setuptools import find_packages,setup
from typing import List #is for type hinting

def get_requirements()->List[str]:
   
    #Thiss function will return list of requirements
    
    requirement_lst:List[str]=[] 
    try:
        with open('requirements.txt','r') as file:
            #Read lines from the file
            lines=file.readlines()
            ## Process each line
            for line in lines:
                requirement=line.strip() #strip whitespace
                ## ignore empty lines and -e .
                if requirement and requirement!= '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_lst

#setting our metadata, metadata is data about data, here 
#we are gonna find all pacjkages and call the function to get requirements

setup(
    name="NetworkSecurityOct2025",
    version="0.0.1",
    author="Jeisson Morales",
    author_email="jsmoraleshengineer@gmail.com",
    packages=find_packages(), #find all packages in the directory
    install_requires=get_requirements() #call the function to get requirements
)