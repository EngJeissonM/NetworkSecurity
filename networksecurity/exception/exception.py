import sys #to get the exception details
from networksecurity.logging import logger #importing the logger from logging package

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys): #error_details is of type sys, 
        self.error_message = error_message #storing the error message
        _,_,exc_tb = error_details.exc_info() #getting the exception details
        
        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename 
    
    #The __str__ method is overridden to format the exception’s output,
    #so when the exception is printed or logged, it displays a clear message
    #including the script name, line number, and error message. 
    #This is especially useful for logging and troubleshooting in larger projects.
    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name, self.lineno, str(self.error_message))
        
if __name__=='__main__':
    try:
        logger.logging.info("Enter the try block") #from logger, we have to call logging function
    
        a=1/0 #example to raise an exception
        print("This will not be printed",a)
    except Exception as e: #except block will catch the exception 
           raise NetworkSecurityException(e,sys) #raising the exception with the help of custom exception class