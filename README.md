# MarketSeer
[![Generic badge](https://img.shields.io/badge/Development-COMPLETE-<COLOR>.svg)](https://shields.io/) 

## Installing and running the software toolkit 

### Creating the database 
	> You need to install docker, if installing Docker for windows you will need an Oracle VM (https://www.virtualbox.org/)
	
	> Once docker is installed, run the following command: 
		 docker create --name postgres-demo -e POSTGRES_PASSWORD=Welcome -p 5432:5432 postgres:11.5-alpine
	
	> Once the docker image is created and running, you will need to access the image with the following command:
		docker exec -it postgres-demo bash 
		psql -h localhost -p 5432 -U postgres -W
	
	> Now create the database 
		create database springdatabase;
		\c springdatabase; 

	> Now create the tables required to store the data
		CREATE TABLE Weekly_Timeseries_Unadjusted (
			id			  SERIAL 		PRIMARY KEY, 
			weekly_symbol	  VARCHAR(10)	NOT NULL,
			stock_open		  NUMERIC(10,4)   NOT NULL,
			stock_high          NUMERIC(10,4)   NOT NULL,
			stock_low           NUMERIC(10,4)   NOT NULL,
			stock_close     	  NUMERIC(10,4)   NOT NULL,
			stock_adj_close     NUMERIC(10,4)   NOT NULL,
			stock_volume        BIGINT          NOT NULL,
			dividend_amount	  NUMERIC(10,4)   NOT NULL,
			cobdate_partition	DATE			NOT NULL);


### Running the MarketSeer Engine (Backend)
	> Navigate into the MarketSeerEngine folder using the CLI  
	
	> Execute the following command from the CLI 
		virtualenv venv 
	
	> Using pip, install the following packages:
		numpy 
		pandas 
		django
		optuna 
		hyperopt
		scikit-learn
		scikit-optimize
		scipy
	
	> Once these dependencies are successfully installed, you can run the backend engine directly from the cli using the following: 
		python manage.py runserver 

	> The server should start running at server 8000
		

### Running the MarketSeer Frontend Dashboard 
	> Navigate into the MarketSeerFrontend folder using the CLI

	> Execute the following command from the CLI 
		virtualenv venv 
	
	> Using pip, install the following packages:
		numpy 
		pandas 
		bokeh

	> Once these dependencies are successfully installed, you can run the dashboard from the cli using the following: 
		bokeh serve --session-token-expiration 900000 --show main.py
