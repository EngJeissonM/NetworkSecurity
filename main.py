from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import ModelTrainerConfig
 
 

import sys

#this block will be executed only when we run this file directly, not when we import it
if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig() #creating object of TrainingPipelineConfig class
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig) 
        #creating object of DataIngestionConfig class and passing trainingpipelineconfig object to it
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)

        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.initiate_data_validation() #this function will return DataValidationArtifact object
        logging.info("data Validation Completed")
        print(data_validation_artifact)

        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)        
        DataTransformation=DataTransformation(data_validation_artifact,data_transformation_config)
        logging.info("Initiate the Data Transformation")
        data_transformation_artifact=DataTransformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")
        print(data_transformation_artifact)

        logging.info("Model Training started")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()


    except Exception as e:
           raise NetworkSecurityException(e,sys)
