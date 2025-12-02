class RoomsDB:
    def __init__(self):
        self.rooms = {}  # room_id -> {"user1": id, "user2": id}

    def create_room(self, creator_id: int) -> int:
        room_id = max(self.rooms.keys(), default=1000) + 1
        self.rooms[room_id] = {"user1": creator_id, "user2": None}
        return room_id

    def join_room(self, room_id: int, user_id: int) -> bool:
        room = self.rooms.get(room_id)
        if not room:
            return False
        if room["user2"] is None:
            room["user2"] = user_id
            return True
        return False

    def get_partner(self, room_id: int, user_id: int):
        room = self.rooms.get(room_id)
        if not room:
            return None
        if room["user1"] == user_id:
            return room["user2"]
        if room["user2"] == user_id:
            return room["user1"]
        return None

    def end_room(self, room_id: int):
        if room_id in self.rooms:
            del self.rooms[room_id]


DB = RoomsDB()
