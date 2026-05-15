from fastapi import FastAPI
from aura_risk_engine.app.api.routes import router
from aura_risk_engine.app.config import Settings

# Create the FastAPI application instance.
app = FastAPI(
    title="AURA X Risk Intelligence Engine",
    version="1.0.0",
    description="Real-time urban safety risk intelligence engine with explainable risk scores.",
)

# Attach settings to the application state for reuse.
app.state.settings = Settings()

# Include API routes from the application router.
app.include_router(router)

@app.get("/health", tags=["Health"])
def health_check() -> dict:
    """Health check endpoint for basic liveness verification."""
    return {"status": "healthy", "service": "AURA X Risk Engine"}
