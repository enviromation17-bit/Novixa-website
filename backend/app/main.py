try:
    from fastapi import FastAPI
except Exception as e:
    raise RuntimeError(
        "FastAPI is not installed or could not be imported. Install it with: pip install fastapi[all]"
    ) from e

app = FastAPI(
    title="Novixa API",
    description="Backend API for the Novixa website",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Novixa API!"
    }


@app.get("/about")
def about():
    return {
        "company": "Novixa",
        "mission": "Engineering Intelligent Digital Systems"
    }


@app.get("/services")
def services():
    return {
        "services": [
            "AI Automation",
            "Web Applications",
            "AI Agents",
            "Business Software"
        ]
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "server": "online"
    }