# receipt-processor-challenge

### Endpoint: Process Receipts

* Path: `/receipts/process`
* Method: `POST`
* Payload: Receipt JSON
* Response: JSON containing an id for the receipt.

Takes in a JSON receipt and returns a JSON object with an ID generated.

Note:
- Receipts with identical details will always generate the same ID.
- Caches the generated ID and points to avoid redundant computations.

## Endpoint: Get Points

* Path: `/receipts/{id}/points`
* Method: `GET`
* Response: A JSON object containing the number of points awarded.

A simple Getter endpoint that looks up the receipt by the ID and returns an object specifying the points awarded


### Installation

1. Clone github repository

```https://github.com/keerthireddytummalapelly/receipt-processor-challenge.git```

Navigate to the project directory 

```cd receipt-processor-challenge```

2. Build the Docker Image

```docker build -t fastapi-app .```

3. Run the FastAPI Container

```docker run -d -p 8000:8000 fastapi-app```

4. Access the API at `http://localhost:8000` or swagger UI at `http://localhost:8000/docs#`
