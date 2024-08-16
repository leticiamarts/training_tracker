# Training Tracker
A simple training tracker using Python, Streamlit and PostgreSQL.

## Environment
Personally recommend to use a `venv`.
On windows:
```
python -m venv .venv
```

```
source .venv/Scripts/activate
```

## Database
Setup a PostgreSQL database with a simple docker-compose like:
```
services:
  postgres:
    image: postgres:latest
    container_name: your_container_name
    environment:
      POSTGRES_USER: username
      POSTGRES_PASSWORD: password
      POSTGRES_DB: database_name
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - postgres_network
    restart: always

volumes:
  postgres_data:
    driver: local

networks:
  postgres_network:
    driver: bridge
```
Make sure to change the following contents for your names of preference `POSTGRES_DB`, `POSTGRES_PASSWORD`, `POSTGRES_USER`, `container_name`.


## Run

Run the application with the script below at the root of the project:
```
python initialize_db.py
```

```
streamlit run app.py
```
