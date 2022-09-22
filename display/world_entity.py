from arcade import Sprite


class WorldEntity:
    def size(self) -> (int, int):
        """
        Return the size of the entity\n
        Return (width: :int, height: int)
        """
        pass

    def token(self) -> str:
        """
        Return the token of the entity\n
        Return (token: str)
        """
        pass

    def sprite(self) -> Sprite:
        """
        Return the sprite of the entity\n
        Return (sprite: Sprite)
        """
        pass

    def background(self) -> Sprite | None:
        """
        Return the background of the entity\n
        Return (background: Sprite)
        """
        pass
