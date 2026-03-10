from fastapi import FastAPI, Request
from fastapi.responses import Response
import httpx

app = FastAPI()

AUTH_SERVICE = "http://auth-service:8000"
QUESTION_SERVICE = "http://question-service:8001"
QUIZ_SERVICE = "http://quiz-service:8002"
RESULT_SERVICE = "http://result-service:8003"
AI_SERVICE = "http://ai-service:8004"


@app.get("/")
def home():
    return {"message": "API Gateway Running"}

# Add Route for Auth Service
@app.post("/token/")
async def login(request: Request):

    data = await request.json()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{AUTH_SERVICE}/api/token/",
            json=data
        )

    return response.json()
# Add Route for Questions Service
@app.get("/questions/")
async def get_questions(request: Request):

    headers = dict(request.headers)
    # remove problematic headers
    headers.pop("content-length", None)
    headers.pop("host", None)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{QUESTION_SERVICE}/api/questions/",
            headers=headers
        )

    return response.json()

@app.post("/questions/")
async def create_question(request: Request):

    body = await request.json()

    headers = {
        "Authorization": request.headers.get("Authorization")
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{QUESTION_SERVICE}/api/questions/",
            json=body,
            headers=headers
        )

    return response.json()   
# Add Route for Quiz 
@app.post("/quiz/generate/")
async def generate_quiz(request: Request):

    headers = dict(request.headers)
    # remove problematic headers
    headers.pop("content-length", None)
    headers.pop("host", None)
    body = await request.json()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{QUIZ_SERVICE}/api/quiz/generate/",
            headers=headers,
            json=body
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type="application/json"
    )

# Add Route for Quiz Submit
@app.post("/quiz/submit/")
async def submit_quiz(request: Request):

    headers = dict(request.headers)
    # remove problematic headers
    headers.pop("content-length", None)
    headers.pop("host", None)
    body = await request.json()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{QUIZ_SERVICE}/api/quiz/submit/",
            headers=headers,
            json=body
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type="application/json"
    )
# Add Route for Result Service
@app.get("/results/")
async def get_results(request: Request):

    headers = dict(request.headers)
    # remove problematic headers
    headers.pop("content-length", None)
    headers.pop("host", None)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{RESULT_SERVICE}/api/results/",
            headers=headers
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type="application/json"
    )
    
#Add Route for Leaderboard
@app.get("/leaderboard/")
async def leaderboard(request: Request):

    headers = dict(request.headers)
    # remove problematic headers
    headers.pop("content-length", None)
    headers.pop("host", None)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{RESULT_SERVICE}/api/results/leaderboard/",
            headers=headers
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type="application/json"
    )


# Add Route for AI Service
@app.post("/ai/analyze/")
async def analyze(request: Request):

    headers = dict(request.headers)
    # remove problematic headers
    headers.pop("content-length", None)
    headers.pop("host", None)
    body = await request.json()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{AI_SERVICE}/api/ai/analyze/",
            headers=headers,
            json=body
        )

    return Response(
        content=response.content,
        status_code=response.status_code,
        media_type="application/json"
    )