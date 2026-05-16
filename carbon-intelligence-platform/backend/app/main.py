from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.apis.routes import router
from app.models.database import initialize_database

app = FastAPI(title='Carbon Intelligence Platform', version='0.1.0', description='Local Siemens-inspired industrial carbon analytics and forecasting API.')
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173','http://127.0.0.1:5173'], allow_credentials=False, allow_methods=['*'], allow_headers=['*'])
app.include_router(router)

@app.on_event('startup')
def startup() -> None:
    initialize_database()

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'carbon-intelligence-platform'}
