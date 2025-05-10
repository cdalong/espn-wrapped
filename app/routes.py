from fastapi import APIRouter, Depends
from app import services

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to Fantasy Wrapped!"}

@router.get("/find-trae")
def find_trae_young_route(team):
    return services.find_trae_young(team) # im like 90% sure this is wrong

@router.get("/team-points")
def get_team_points_route(team):
    return services.get_total_points(team) # im like 90% sure this is wrong