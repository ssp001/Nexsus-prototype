## pdf Qna Assistant

A prototype vector db less rag agent using pageindex.

- Prerequisites:
1/ it's need docker to run this prototype
2/ install all libraryes in reqierment.txt
3/ make a .env file first then make some reqiered enviourmental key varriables  
4/ run your own minio image using docker command 



# Tech stack

file:
``` reqierment.txt```

- Nessary system provisioning

- to run the prototype 
- to sun the server
```bash uvicorn app.api.api:app --reload ```

- this command will auto matically run the server on the terminal. but before that 

- to run the minio server
```bash docker compose up -d ```

- to make the env file 
```bash echo .env ```
- in that file make key values like 
/*
pageindex_api_key="your pageindex api key"
minio_secretkey="admin1234"
minio_username="admin"
minio_localhost="localhost:9000"
minio_bucket_name="test"
*/

- to install the tech stack
```bash uv add -r .\reqierment.txt```
- run this command to install all neessary libraryes to prevent any errors.
- then run the server  

- then after that run the frontend
```bash streamlit run frontned/streamlit_app.py```

you are good to go 😈

first give a good pdf and ask what to want to know reagarding that pdf

- file strucher

+---app
|   +---api
|   |   \---__pycache__
|   +---bucket
|   |   \---__pycache__
|   \---document_processing
|       \---__pycache__
+---config
|   \---__pycache__
+---frontned
|   \---__pycache__
+---tests
|   \---__pycache__
+---tmp
\---utils
    \---__pycache__

