from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import eda_functions # Import the new module

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Auto EDA backend is running!"}

@app.post("/api/analyze")
async def analyze_data(file: UploadFile = File(...), prompt: str = Form(None)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        
        summary = df.describe(include="all").to_dict()
        plot_base64 = None

        if prompt:
            plot_base64 = eda_functions.get_plot_from_prompt(df, prompt)

        if not plot_base64:
            numeric_cols = df.select_dtypes(include=['number']).columns
            if not numeric_cols.empty:
                plot_base64 = eda_functions.plot_histogram(df, numeric_cols[0])

        return {
            "filename": file.filename,
            "message": "Analysis successful!",
            "summary": summary,
            "plot": plot_base64
        }
    except Exception as e:
        return {"message": f"An error occurred: {e}"}