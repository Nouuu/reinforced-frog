import copy

from arcade import Sprite


class WorldEntity:

    def __init__(self, width: int, height: int, token: str, sprite: Sprite):
        self.__width = width
        self.__height = height
        self.__token = token
        self.__sprite = sprite

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def token(self) -> str:
        """
        Return the token of the entity\n
        Return (token: str)
        """
        return self.__token

    @property
    def sprite(self) -> Sprite:
        """
        Return the sprite of the entity\n
        Return (sprite: Sprite)
        """
        return Sprite(texture=self.__sprite.texture, scale=self.__sprite.scale)
