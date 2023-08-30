from typing import Any, Tuple, Optional
import datetime
import time

import requests

from core.app.api_exceptions.not_acceptable import NotAcceptable
from core.app.api_exceptions.not_found import (
    PlayerNotFound,
    PlayerProfileNotFound,
)
from core.constants.defaults import (
    GAME_URL,
    FAKE_USER_AGENT,
    PROFILE_URL,
    PROFILE_MATCHES_URL,
)
from core.constants.formats import (
    LONG_GAME_DURATION_FORMAT,
    GAME_DURATION_FORMAT,
    DATE_FORMAT
)
from core.models import Hero


class OpenDotaConnect:
    """
    Connects to Open dota and parsed page.

    :raises NotAcceptable: when user_id is invalid
    :raises PlayerProfileNotFound: when user_id was not found in game.
    """

    @staticmethod
    def get_data_json(url: str) -> dict[str, Any]:
        session = requests.Session()
        session.headers.update(FAKE_USER_AGENT)

        try:
            response = session.get(url=url)
        except requests.exceptions.RequestException:
            raise NotAcceptable("Open dota URL is not available.")

        if response.status_code != 200:
            raise NotAcceptable(
                f"Open dota URL returned status code: {response.status_code}."
            )

        return response.json()


class GameData:
    data: dict[str, Any]

    def __init__(self, game_id: int) -> None:
        """
        Connects to open dota api and takes the game information from there.

        :raises NotAcceptable: when URL is invalid.
        """

        json_data = OpenDotaConnect.get_data_json(
            url=GAME_URL.format(game_id=str(game_id))
        )
        self.game_id = game_id
        self.data = json_data

    def get_time_fields(self) -> Tuple[datetime.datetime, datetime.time]:

        raw_date = time.gmtime(
            self.data["start_time"]
        )
        game_date = datetime.datetime(
            year=raw_date.tm_year,
            month=raw_date.tm_mon,
            day=raw_date.tm_mday,
            hour=raw_date.tm_hour,
            minute=raw_date.tm_min,
            second=raw_date.tm_sec
        )

        duration_secs = self.data["duration"]
        game_duration = datetime.time(
            hour=duration_secs // 3600,
            minute=duration_secs % 3600 // 60,
            second=duration_secs % 60
        )

        return game_date, game_duration

    def __find_player(
            self,
            dota_id: int,
            nickname: str
    ) -> dict[str, Any]:
        """
        TODO

        :raises PlayerNotFound: when player with requested dota ID was
         not found.
        """

        for player in self.data["players"]:
            if dota_id == player["account_id"]:
                return player

        raise PlayerNotFound(
            dota_id=dota_id,
            nickname=nickname,
            game_id=self.game_id
        )

    def get_player_results(
            self,
            nickname: str,
            dota_id: int
    ) -> Optional[dict[str, Any]]:
        """
        Gets player results from parsed data in class.

        :raises PlayerNotFound: when player with requested DOTA ID was
                not found.
        """

        player_results = {}
        player = self.__find_player(dota_id=dota_id, nickname=nickname)

        player_results["nickname"] = player["personaname"]
        player_results["win"] = bool(player["win"])
        player_results["hero"] = Hero.objects.get(hero_id=player["hero_id"])
        player_results["kills"] = player["kills"]
        player_results["deaths"] = player["deaths"]
        player_results["assists"] = player["assists"]
        player_results["networth"] = player["net_worth"]
        player_results["last_hits"] = player["last_hits"]
        player_results["denies"] = player["denies"]
        player_results["gpm"] = player["gold_per_min"]
        player_results["xpm"] = player["xp_per_min"]
        player_results["damage"] = player["hero_damage"]

        return player_results


class PlayerData:

    @staticmethod
    def get_nickname(dota_user_id: int) -> str:
        """
        Connects to Open dota and takes the player information from there.

        :raises NotAcceptable: when user_id is invalid
        :raises PlayerProfileNotFound: when user_id was not found in game.
        """

        url = PROFILE_URL.format(user_id=str(dota_user_id))
        json_data = OpenDotaConnect.get_data_json(
            url=url
        )
        return json_data["profile"]["personaname"]


class GamesData:

    @staticmethod
    def get_last_games_ids(
            dota_id: int,
            count: Optional[int] = 50
    ) -> list[int]:
        """
        TODO
        """

        games = OpenDotaConnect.get_data_json(
            url=PROFILE_MATCHES_URL.format(
                dota_id=str(dota_id),
                limit=count
            )
        )

        all_games_ids = []
        for game in games:
            all_games_ids.append(game["match_id"])
        return all_games_ids
