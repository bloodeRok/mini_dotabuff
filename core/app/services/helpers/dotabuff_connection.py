from typing import Any, Tuple, Optional
from bs4 import BeautifulSoup
from bs4.element import Tag
from datetime import datetime, time

import requests

from core.app.api_exceptions.not_acceptable import NotAcceptable
from core.app.api_exceptions.not_found import (
    PlayerNotFound,
    PlayerProfileNotFound,
)
from core.constants.defaults import (
    DOTABUFF_GAME_URL,
    FAKE_USER_AGENT,
    DOTABUFF_PROFILE_URL,
    DOTABUFF_PROFILE_MATCHES_URL,
)
from core.constants.formats import (
    LONG_GAME_DURATION_FORMAT,
    GAME_DURATION_FORMAT,
)


class DotabuffConnect:
    """
    Connects to dotabuff and parsed page.

    :raises NotAcceptable: when user_id is invalid
    :raises PlayerProfileNotFound: when user_id was not found in game.
    """

    @staticmethod
    def get_parsed_page(url: str) -> BeautifulSoup:
        session = requests.Session()
        session.headers.update(FAKE_USER_AGENT)

        try:
            response = session.get(url=url)
        except requests.exceptions.RequestException:
            raise NotAcceptable("DOTABUFF URL is not available.")

        if response.status_code != 200:
            raise NotAcceptable(
                f"DOTABUFF URL returned status code: {response.status_code}."
            )

        return BeautifulSoup(response.text, "lxml")


class GameData:
    data: dict[str, Any]

    def __init__(self, game_id: int) -> None:
        """
        Connects to dotabuff and takes the game information from there.

        :raises NotAcceptable: when game_id is invalid
        :raises PlayerNotFound: when nickname was not found in game.
        """

        parsed_page = DotabuffConnect.get_parsed_page(
            url=DOTABUFF_GAME_URL.format(game_id=str(game_id))
        )
        self.game_id = game_id
        self.data = {
            "radiant": list(parsed_page.find("section", "radiant").
                            find("tbody")),
            "dire": list(parsed_page.find("section", "dire").find("tbody")),
            "winner": parsed_page.find("div", class_="match-result").text.
            split()[0].lower(),
            "date": parsed_page.find("time").attrs["datetime"],
            "duration": parsed_page.find("span", class_="duration").text
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

    def __find_player(self, user_id: int, nickname: str) -> Tuple[Optional[Tag], Optional[str]]:
        """
        TODO

        :raises PlayerNotFound: when player with requested dotabuff ID was
                not found.
        """
        game_id = self.game_id
        for team in [self.data["radiant"], self.data["dire"]]:
            for player in team:
                try:
                    player_id = player \
                        .find("td", class_="tf-pl single-lines") \
                        .find("a").attrs["href"].split("/")[-1]
                except AttributeError:
                    print(game_id)
                    return None, None
                if str(user_id) == player_id:
                    team_name = list(self.data.keys())[
                               list(self.data.values()).index(team)
                           ]
                    return player, team_name

        raise PlayerNotFound(user_id=user_id, nickname=nickname, game_id=self.game_id)

    def get_player_results(
            self,
            nickname: str,
            user_id: int
    ) -> Optional[dict[str, Any]]:
        """
        Gets player results from parsed data in class.

        :raises PlayerNotFound: when player with requested dotabuff ID was
                not found.
        """

        player_results = {}
        player, team = self.__find_player(user_id=user_id, nickname=nickname)
        if player is None or team is None:
            return

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


class PlayerData:

    @staticmethod
    def get_nickname(dotabuff_user_id: int) -> str:
        """
        Connects to dotabuff and takes the player information from there.

        :raises NotAcceptable: when user_id is invalid
        :raises PlayerProfileNotFound: when user_id was not found in game.
        """

        parsed_page = DotabuffConnect.get_parsed_page(
            url=DOTABUFF_PROFILE_URL.format(user_id=str(dotabuff_user_id)))
        return str(
            parsed_page.find("div", class_="header-content-title").
            find("h1").next
        )


class GamesData:

    @staticmethod
    def get_last_games_ids(
            dotabuff_user_id: int,
    ) -> list[int]:
        """
        TODO
        """

        parsed_page = DotabuffConnect.get_parsed_page(
            url=DOTABUFF_PROFILE_MATCHES_URL.format(
                user_id=str(dotabuff_user_id)
            )
        )
        all_games = parsed_page.find("tbody").find_all("tr")
        all_games_ids = []
        for game in all_games:
            all_games_ids.append(
                int(
                    game.find("td", class_="cell-large")
                    .find("a").attrs["href"].split("/")[-1]
                )
            )
        return all_games_ids
