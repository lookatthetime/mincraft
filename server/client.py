class GameClient:
    def get_world(self):
        pass

    def get_world_version(self):
        pass

    def get_world_edits(self) -> list[list[any]]:
        pass

    def get_players(self):
        pass

    def send_block(self, position, tex):
        pass

    def send_player(self, position, tex):
        pass

    def send_destroy(self, position, tex):
        pass
