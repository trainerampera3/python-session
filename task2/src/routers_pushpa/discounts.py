from fastapi import FastAPI
 
app = FastAPI()
 
 
@app.get("/")
def root():
    return {
        "message": "Store API is running"
    }

@app.get("/discounts")
def get_discounts():
    # query your database
    # return the table data
    return {
        "discounts": "discounts are running"}