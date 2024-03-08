from fastapi import FastAPI

from session_auth.core.configs import settings
from session_auth.api.v1.api import api_router


app = FastAPI(title="API da Guida", version="0.0.1", description="My first aPI")
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)

"""
# token user 6:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzA5NzU1NjU4LCJpYXQiOjE3MDkxNTA4NTgsInN1YiI6IjYifQ.7cYNSDduAJRc2JGrT-JkZa6OZMUuKvpqpohdlOaQQQc
# token user 8
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzA5NzU3Njk4LCJpYXQiOjE3MDkxNTI4OTgsInN1YiI6IjgifQ.fiokrV0y3ws85ifbURpX8sbVI3Pyhwr5E3b1JNuseHc
"""
