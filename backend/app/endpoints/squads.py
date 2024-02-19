from app.models.squad import Squad
from app.models.user import User
from app.permissions.squads import SquadPermissions
from app.repositories import SquadRepository, UserRepository
from app.schemas.files import FileResponse
from app.schemas.squads import (
    SquadInvitationRequest,
    SquadReplyRequest,
    SquadResponse,
    SquadUpdateRequest,
    SquadUpsertRequest,
)
from app.schemas.users import UserResponse
from app.security.auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, UploadFile

router = APIRouter(dependencies=[Depends(get_current_user)])


def get_squad(squad_id: int, squad_repository: SquadRepository = Depends()):
    """
    Returns the squad of the corresponding squad_id.
    Does not check for ownership.
    Raises 404 if squad is not found
    """
    squad = squad_repository.get_squad(squad_id)

    if squad is None:
        raise HTTPException(status_code=404, detail="Squad not found")

    return squad


def get_owned_squad(
    squad: Squad = Depends(get_squad), current_user: User = Depends(get_current_user)
):
    """
    Returns the squad of the corresponding squad_id only if the current user owns it.
    Raises 404 if squad is not found
    Raises 403 if user is not owner
    """
    if squad.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not the owner of this squad"
        )

    return squad


@router.get("/", response_model=list[SquadResponse])
def get_squads(
    squad_repository: SquadRepository = Depends(),
):
    return squad_repository.get_squads()


@router.get("/{squad_id}", response_model=SquadResponse)
def get_squad(
    squad: Squad = Depends(get_squad),
):
    return squad


@router.get("/{squad_id}/members", response_model=list[UserResponse])
def get_squad_members(
    squad: Squad = Depends(get_squad),
):
    return squad.members


@router.get("/{squad_id}/photos", response_model=list[FileResponse])
def get_squad_photos(
    squad: Squad = Depends(get_squad),
):
    return squad.photos


@router.post("/{squad_id}/photos", response_model=list[FileResponse])
def add_squad_photos(
    photos: list[UploadFile],
    squad: Squad = Depends(get_owned_squad),
    squad_repository: SquadRepository = Depends(),
):
    return squad_repository.add_squad_photos(squad, photos)


@router.post("/{squad_id}/avatar")
def add_squad_avatar(
    avatar: UploadFile,
    squad_repository: SquadRepository = Depends(),
    squad: Squad = Depends(get_owned_squad),
):
    return squad_repository.add_squad_avatar(squad, avatar)


@router.post("/", response_model=SquadResponse)
def create_squad(
    payload: SquadUpsertRequest,
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(),
):
    if squad_repository.get_count_by_name(payload.name):
        raise HTTPException(status_code=400, detail="Squad already exists")

    if (
        squad_repository.get_count_by_owner(current_user.id)
        >= SquadPermissions.MAX_OWNED
    ):
        raise HTTPException(
            status_code=400,
            detail=f"You can't create more than {SquadPermissions.MAX_OWNED} squads",
        )

    squad = Squad(
        **payload.model_dump(), owner_id=current_user.id, members=[current_user]
    )

    return squad_repository.upsert_squad(squad)


@router.put("/{squad_id}", response_model=SquadResponse)
def update_squad(
    payload: SquadUpdateRequest,
    squad_repository: SquadRepository = Depends(),
    squad: Squad = Depends(get_owned_squad),
):
    return squad_repository.update_squad(squad, payload)


@router.post("/{squad_id}/invites")
def invite_user(
    payload: SquadInvitationRequest,
    squad: Squad = Depends(get_owned_squad),
    squad_repository: SquadRepository = Depends(),
    user_repository: UserRepository = Depends(),
):
    user = user_repository.get_by_email(payload.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user in squad.members:
        raise HTTPException(status_code=400, detail="User is already a member")

    if user in squad.applications:
        # User already applied, should be automatically accepted
        squad_repository.accept_user(squad, user)
        return {"message": "User joined the squad"}

    if user in squad.invitations:
        squad_repository.touch(squad)
        return {"message": "User invited"}

    squad_repository.invite_user(squad, user)

    return {"message": "User invited"}


@router.put("/{squad_id}/invites")
def update_invite(
    payload: SquadReplyRequest,
    squad: Squad = Depends(get_squad),
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(),
):
    if current_user not in squad.invitations:
        raise HTTPException(status_code=400, detail="User is not invited")

    if payload.accept:
        squad_repository.accept_user(squad, current_user)
    else:
        squad_repository.decline_user(squad, current_user)

    return {"message": "Invitation updated"}


@router.put("/{squad_id}/applies/{user_id}")
def update_application(
    user_id: int,
    payload: SquadReplyRequest,
    squad: Squad = Depends(get_owned_squad),
    squad_repository: SquadRepository = Depends(),
    user_repository: UserRepository = Depends(),
):
    user = user_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user not in squad.applications:
        raise HTTPException(status_code=400, detail="User didn't apply to this squad")

    if payload.accept:
        squad_repository.accept_user(squad, user)
    else:
        squad_repository.decline_user(squad, user)

    return {"message": "Application updated"}


@router.put("/{squad_id}/apply")
def apply_to_squad(
    squad: Squad = Depends(get_squad),
    current_user: User = Depends(get_current_user),
    squad_repository: SquadRepository = Depends(),
):
    if current_user in squad.members:
        raise HTTPException(status_code=400, detail="User is already in squad")

    if current_user in squad.invitations:
        # User is already invited, should be automatically accepted
        squad_repository.accept_user(squad, current_user)
        return {"message": "User joined the squad"}

    squad_repository.apply_to_squad(squad, current_user)

    return {"message": "Application created"}


@router.get("/{squad_id}/invites", response_model=list[UserResponse])
def get_invited_users(
    squad: Squad = Depends(get_squad),
):
    return squad.invitations


@router.get("/{squad_id}/applies", response_model=list[UserResponse])
def get_squad_applications(
    squad: Squad = Depends(get_squad),
):
    return squad.applications


@router.delete("/{squad_id}", status_code=204)
def delete_squad(
    squad: Squad = Depends(get_owned_squad),
    squad_repository: SquadRepository = Depends(),
):
    squad_repository.delete_squad(squad)
