### GET
def get_club_users_success(club_id: int):
    ...

def get_club_users_club_not_found(club_id: int):
    ...

### GET BY ID
def get_club_user_by_id_success(club_id: int, user_id: int):
    ...

def get_club_user_by_id_user_not_found(club_id: int, user_id: int):
    ...

### CREATE
def create_club_user_success(club_id: int, user_id: int):
    ...

def create_club_user_forbidden(club_id: int, user_id: int):
    ...

def create_club_user_club_not_found(club_id: int, user_id: int):
    ...

def create_club_user_user_not_found(club_id: int, user_id: int):
    ...

### UPDATE
def update_club_user_success(club_id: int, user_id: int):
    ...

def update_club_user_forbidden(club_id: int, user_id: int):
    ...

### DELETE
def delete_club_user_success(club_id: int, user_id: int):
    ...

def delete_club_user_forbidden(club_id: int, user_id: int):
    ...
