from fastapi import FastAPI


## create an instance of fastapi
app = FastAPI()

## set the base url 
@app.get("/")
def display_something():
    """
    function to display an output
    """
    return {"data": {"greetings": "Hello World!"}}

## set the about page url
@app.get("/about")
def about_page():
    return {'data': 'About Page'}