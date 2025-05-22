from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from app.services import Services


# Model for ESPN Fantasy credentials
class ESPNCredentials(BaseModel):
    league_id: int
    year: int
    espn_s2: str
    swid: str


# Simple in-memory storage for user sessions (would use a database in production)
active_sessions = {}


# Model for login response
class SessionToken(BaseModel):
    session_id: str
    message: str = "Authentication successful"


# Model for wrapped data
class WrappedSession(BaseModel):
    model_config = {"arbitrary_types_allowed": True}  # Add this line

    credentials: ESPNCredentials
    services: Optional[Services] = None


# OAuth2 password bearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Function to validate the session token
async def get_current_session(token: str = Depends(oauth2_scheme)):
    if token not in active_sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return active_sessions[token]