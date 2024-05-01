from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pickle
import numpy as np

app = FastAPI()
templates = Jinja2Templates(directory="templates")

with open("Thyroid_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/predictresult", response_class=HTMLResponse)
async def predict_result(request: Request, age: float = Form(...), sex: str = Form(...), TSH: float = Form(...), 
                         TT4: float = Form(...), FTI: float = Form(...), on_thyroxine: str = Form(...), 
                         on_antithyroid_medication: str = Form(...), goitre: str = Form(...), 
                         hypopituitary: str = Form(...), psych: str = Form(...), T3_measured: str = Form(...)):
    
    # Convert string inputs to numeric values
    Sex = 1 if sex == "Male" else 0
    On_thyroxine = 1 if on_thyroxine == "True" else 0
    On_antithyroid_medication = 1 if on_antithyroid_medication == "True" else 0
    Goitre = 1 if goitre == "True" else 0
    Hypopituitary = 1 if hypopituitary == "True" else 0
    Psychological_symptoms = 1 if psych == "True" else 0
    T3_measured = 1 if T3_measured == "True" else 0

    arr = np.array([[age, Sex, TSH, TT4, FTI, On_thyroxine, On_antithyroid_medication, 
                     Goitre, Hypopituitary, Psychological_symptoms, T3_measured]])
    
    pred = model.predict(arr)

    if pred == 0:
        res_Val = "Compensated Hypothyroid"
    elif pred == 1:
        res_Val = "No Thyroid"
    elif pred == 2:
        res_Val = 'Primary Hypothyroid'
    elif pred == 3:
        res_Val = 'Secondary Hypothyroid'

    Output = f"Patient has {res_Val}"
    return templates.TemplateResponse("predictresult.html", {"request": request, "output": Output})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
