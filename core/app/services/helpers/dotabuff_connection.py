from typing import Any, Tuple
from bs4 import BeautifulSoup
from bs4.element import Tag
from datetime import datetime, time

import requests

from core.app.api_exceptions.not_acceptable import NotAcceptable
from core.app.api_exceptions.not_found import PlayerNotFound
from core.constants.defaults import DOTABUFF_GAME_URL, FAKE_USER_AGENT
from core.constants.formats import (
    LONG_GAME_DURATION_FORMAT,
    GAME_DURATION_FORMAT,
)


class GameData:
    data: dict[str, Any]

    def __init__(self, game_id: int) -> None:
        """
        Connects to dotabuff and takes the required information from there.

        :raises NotAcceptable: when game_id is invalid
        :raises PlayerNotFoundException: when nickname was not found in game.
        """

        game_url = DOTABUFF_GAME_URL.format(game_id=str(game_id))
        session = requests.Session()
        session.headers.update(FAKE_USER_AGENT)

        try:
            response = session.get(url=game_url)
        except requests.exceptions.RequestException:
            raise NotAcceptable("DOTABUFF URL is not available.")

        if response.status_code != 200:
            raise NotAcceptable(
                f"DOTABUFF URL returned status code: {response.status_code}."
            )

        bs = BeautifulSoup(response.text, "lxml")
        self.data = {
            "radiant": list(bs.find("section", "radiant").find("tbody")),
            "dire": list(bs.find("section", "dire").find("tbody")),
            "winner": bs.find("div", class_="match-result").text.
            split()[0].lower(),
            "date": bs.find("time").attrs["datetime"],
            "duration": bs.find("span", class_="duration").text
        }

    def get_time_fields(self) -> Tuple[datetime, time]:
        game_date = datetime.fromisoformat(
            self.data["date"]
        )
        duration = self.data["duration"]
        if len(duration.split(":")) == 3:
            game_duration = datetime.strptime(
                duration,
                LONG_GAME_DURATION_FORMAT
            ).time()
            return game_date, game_duration
        game_duration = datetime.strptime(
            duration,
            GAME_DURATION_FORMAT
        ).time()
        return game_date, game_duration

    def __find_player(self, nickname: str) -> Tuple[Tag, str]:
        for team in [self.data["radiant"], self.data["dire"]]:
            for player in team:
                nick_in_game = player. \
                        find("td", class_="tf-pl single-lines").find("a").text
                if nickname == nick_in_game:
                    return player, list(self.data.keys())[list(self.data.values()).index(team)]
        raise PlayerNotFound

    def get_player_results(self, nickname: str) -> dict[str, Any]:
        """
        Gets player results from parsed data in class.
        """

        player_results = {}
        player, team = self.__find_player(nickname=nickname)

        player_results["nickname"] = player. \
            find("td", class_="tf-pl single-lines").find("a").text
        player_results["win"] = team == self.data["winner"]
        player_results["hero"] = player.find("img").attrs["title"]

        player_results["kills"] = int(
            player.find("td", class_="tf-r r-tab r-group-1").text
        )
        player_results["deaths"] = int(
            player.find("td", class_="tf-r r-tab r-group-1 cell-minor").text
        )
        player_results["assists"] = int(
            player.find("td", class_="tf-r r-tab r-group-1").text
        )
        player_results["networth"] = int(float(
            player.
            find("td", class_="tf-r r-tab r-group-1 color-stat-gold").
            string[:-1]) * 1000)

        last_hits = player. \
            find_all("td", class_="tf-r r-tab r-group-2 cell-minor")[0].text
        player_results["last_hits"] = 0 if last_hits == "-" else int(last_hits)

        denies = player. \
            find_all("td", class_="tf-pl r-tab r-group-2 cell-minor")[0].text
        player_results["denies"] = 0 if denies == "-" else int(denies)

        player_results["gpm"] = int(
            player.
            find_all("td", class_="tf-r r-tab r-group-2 cell-minor")[1].text
        )
        player_results["xpm"] = int(
            player.
            find_all("td", class_="tf-pl r-tab r-group-2 cell-minor")[1].text
        )
        player_results["damage"] = int(float(
            player.
            find("td", class_="tf-r r-tab r-group-3 cell-minor").
            text[:-1]) * 1000)

        return player_results
