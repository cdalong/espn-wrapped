from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services import Services
from espn_api.basketball import League
from fastapi.security import OAuth2PasswordRequestForm
import uuid
from app.auth import ESPNCredentials, SessionToken, active_sessions, get_current_session, WrappedSession



router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to Fantasy Wrapped!"}

@router.post("/login", response_model=SessionToken)
async def login(credentials: ESPNCredentials):
    try:
        # Try to initialize the services to validate credentials
        services = Services(
            league_id=credentials.league_id,
            year=credentials.year,
            espn_s2=credentials.espn_s2,
            swid=credentials.swid
        )
        
        # Verify the credentials work by accessing the team property
        if services.team is None:
            raise HTTPException(status_code=401, detail="Invalid ESPN credentials")
        
        # Create a session ID
        session_id = str(uuid.uuid4())
        
        # Store the session in memory
        active_sessions[session_id] = WrappedSession(
            credentials=credentials,
            services=services
        )
        
        return {"session_id": session_id}
    
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

# end points??
@router.get("/team/find-trae")
async def find_trae_young_route(session: WrappedSession = Depends(get_current_session)):  
    try:
        return session.services.find_trae_young()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/team/weekly-average")
async def get_weekly_average_route(session: WrappedSession = Depends(get_current_session)):
    try:
        return session.services.get_weekly_average()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/team/best-week")
async def get_best_week_route(session: WrappedSession = Depends(get_current_session)):
    try:
        return session.services.get_best_week()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/team/worst-week")
async def get_worst_week_route(session: WrappedSession = Depends(get_current_session)):
    try:
        return session.services.get_worst_week()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/team/longest-streak")
async def get_longest_streak_route(session: WrappedSession = Depends(get_current_session)):
    try:
        return session.services.get_longest_streak()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  
    

@router.get("/team/sleeper")
async def get_sleeper_star_route(session: WrappedSession = Depends(get_current_session)):
    try:
        return session.services.get_sleeper_star()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/team/bust")
async def get_bust_route(session: WrappedSession = Depends(get_current_session)):
    try:
        return session.services.get_bust()   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/team/clutch")
async def find_clutch_player_route(session: WrappedSession = Depends(get_current_session)):
    try:
        return session.services.find_clutch_player()   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/team/best-matchup")
async def find_best_team_matchup_route(session: WrappedSession = Depends(get_current_session)):
    try:
        return session.services.find_best_team_matchup()   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
    

@router.get("/team/worst-matchup")
async def find_worst_team_matchup_route(session: WrappedSession = Depends(get_current_session)):
    try:
        return session.services.find_worst_team_matchup()   
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  
    
@router.post("/logout")
async def logout(session: WrappedSession = Depends(get_current_session)):
    for session_id, stored_session in list(active_sessions.items()):
        if stored_session == session:
            del active_sessions[session_id]
            return {"message": "Logged out successfully"}
    
    raise HTTPException(status_code=400, detail="No active session found")