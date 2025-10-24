from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel, Field
from typing import Literal
import joblib
from categorify import Categorify


class PatientPredictionRequest(BaseModel):
    avg_personal_medico_general: float
    avg_personal_medico_esp: float
    avg_ginecoobstetras: float
    avg_pediatras: float
    avg_cirujanos: float
    avg_internistas: float
    avg_anestesiologos: float
    avg_odontologos: float
    avg_pasantes: float
    avg_personal_hospital: float
    avg_enfermeras_general: float
    avg_enfermeras_esp: float
    avg_camas_hospitalizacion: float
    avg_camas_atencion_temporal: float
    avg_labs: float
    avg_dias_estancia: float
    total_atencion_medica: float
    lag_1: float
    delta_1: float
    rolling_mean_3: float
    year: int = Field(..., ge=2000, le=2100)
    quarter: Literal[1, 2, 3, 4]
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    weekday: Literal[0, 1, 2, 3, 4, 5, 6]
    nombre_entidad: str
    nombre_municipio: str
    nombre_localidad: str
    codigo_postal: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "avg_personal_medico_general": 3000,
                    "avg_personal_medico_esp": 1500,
                    "avg_ginecoobstetras": 120,
                    "avg_pediatras": 100,
                    "avg_cirujanos": 110,
                    "avg_internistas": 60,
                    "avg_anestesiologos": 130,
                    "avg_odontologos": 10,
                    "avg_pasantes": 20,
                    "avg_personal_hospital": 3500,
                    "avg_enfermeras_general": 600,
                    "avg_enfermeras_esp": 130,
                    "avg_camas_hospitalizacion": 700,
                    "avg_camas_atencion_temporal": 250,
                    "avg_labs": 10,
                    "avg_dias_estancia": 40,
                    "total_atencion_medica": 9000,
                    "lag_1": 80,
                    "delta_1": 5,
                    "rolling_mean_3": 85,
                    "year": 2024,
                    "quarter": 4,
                    "month": 10,
                    "day": 15,
                    "weekday": 1,
                    "nombre_entidad": "Ciudad De México",
                    "nombre_municipio": "Benito Juarez",
                    "nombre_localidad": "Alvaro Obregon",
                    "codigo_postal": "72570"
                }
            ]
        }
    }


description = """
API REST que predice la cantidad de pacientes esperados en hospitales según fecha, ubicación, tipo de servicio y variables externas como clima o eventos. Utiliza modelos de series temporales entrenados con datos históricos para optimizar la planificación de recursos y personal sanitario. Ideal para integrar con dashboards y sistemas de gestión hospitalaria.
"""

MODEL_PATH = '../models/outputs'

tags_metadata = [
    {
        'name': 'predictions',
        'description': 'Execute predictions'
    }
]

app = FastAPI(
    title='Health Resources Prediction',
    description=description,
    version='0.0.1',
    openapi_tags=tags_metadata
)


@app.post('/v1/predict/', tags=['predictions'])
async def get_prediction(data: PatientPredictionRequest):
    test = pd.DataFrame([data.model_dump()])
    model = joblib.load(f'{MODEL_PATH}/model.pkl')
    prediction = model.predict(test)
    return {'No. of Patients': float(prediction[0])}
