OPEN_DOTA_ROOT = "https://api.opendota.com/api/"
GAME_URL = OPEN_DOTA_ROOT + "matches/{game_id}/"
PROFILE_URL = OPEN_DOTA_ROOT + "players/{user_id}/"
PROFILE_MATCHES_URL = OPEN_DOTA_ROOT + "players/{dota_id}/matches/?limit={limit}"

FAKE_USER_AGENT = {
    "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0)"
        " Gecko/20100101 Firefox/45.0"
}
ADMIN_ACCOUNT = 190947906

ADD_HEROES_MIGRATION_SQL = "INSERT INTO backend_hero (name, hero_id) VALUES " \
                           "('Anti-Mage', 1)," \
                           "('Axe', 2)," \
                           "('Bane', 3)," \
                           "('Bloodseeker', 4)," \
                           "('Crystal Maiden', 5)," \
                           "('Drow Ranger', 6)," \
                           "('Earthshaker', 7)," \
                           "('Juggernaut', 8)," \
                           "('Mirana', 9)," \
                           "('Morphling', 10)," \
                           "('Shadow Fiend', 11)," \
                           "('Phantom Lancer', 12)," \
                           "('Puck', 13)," \
                           "('Pudge', 14)," \
                           "('Razor', 15)," \
                           "('Sand King', 16)," \
                           "('Storm Spirit', 17)," \
                           "('Sven', 18)," \
                           "('Tiny', 19)," \
                           "('Vengeful Spirit', 20)," \
                           "('Windranger', 21)," \
                           "('Zeus', 22)," \
                           "('Kunkka', 23)," \
                           "('Lina', 25)," \
                           "('Lion', 26)," \
                           "('Shadow Shaman', 27)," \
                           "('Slardar', 28)," \
                           "('Tidehunter', 29)," \
                           "('Witch Doctor', 30)," \
                           "('Lich', 31)," \
                           "('Riki', 32)," \
                           "('Enigma', 33)," \
                           "('Tinker', 34)," \
                           "('Sniper', 35)," \
                           "('Necrophos', 36)," \
                           "('Warlock', 37)," \
                           "('Beastmaster', 38)," \
                           "('Queen of Pain', 39)," \
                           "('Venomancer', 40)," \
                           "('Faceless Void', 41)," \
                           "('Wraith King', 42)," \
                           "('Death Prophet', 43)," \
                           "('Phantom Assassin', 44)," \
                           "('Pugna', 45)," \
                           "('Templar Assassin', 46)," \
                           "('Viper', 47)," \
                           "('Luna', 48)," \
                           "('Dragon Knight', 49)," \
                           "('Dazzle', 50)," \
                           "('Clockwerk', 51)," \
                           "('Leshrac', 52)," \
                           "('Nature''s Prophet', 53)," \
                           "('Lifestealer', 54)," \
                           "('Dark Seer', 55)," \
                           "('Clinkz', 56)," \
                           "('Omniknight', 57)," \
                           "('Enchantress', 58)," \
                           "('Huskar', 59)," \
                           "('Stalker', 60)," \
                           "('Broodmother', 61)," \
                           "('Bounty Hunter', 62)," \
                           "('Weaver', 63)," \
                           "('Jakiro', 64)," \
                           "('Batrider', 65)," \
                           "('Chen', 66)," \
                           "('Spectre', 67)," \
                           "('Ancient Apparition', 68)," \
                           "('Doom', 69)," \
                           "('Ursa', 70)," \
                           "('Spirit Breaker', 71)," \
                           "('Gyrocopter', 72)," \
                           "('Alchemist', 73)," \
                           "('Invoker', 74)," \
                           "('Silencer', 75)," \
                           "('Outworld Destroyer', 76)," \
                           "('Lycan', 77)," \
                           "('Brewmaster', 78)," \
                           "('Shadow Demon', 79)," \
                           "('Lone Druid', 80)," \
                           "('Chaos Knight', 81)," \
                           "('Meepo', 82)," \
                           "('Treant Protector', 83)," \
                           "('Ogre Magi', 84)," \
                           "('Undying', 85)," \
                           "('Rubick', 86)," \
                           "('Disruptor', 87)," \
                           "('Nyx Assassin', 88)," \
                           "('Naga Siren', 89)," \
                           "('Keeper of the Light', 90)," \
                           "('Io', 91)," \
                           "('Visage', 92)," \
                           "('Slark', 93)," \
                           "('Medusa', 94)," \
                           "('Troll Warlord', 95)," \
                           "('Centaur Warrunner', 96)," \
                           "('Magnus', 97)," \
                           "('Timbersaw', 98)," \
                           "('Bristleback', 99)," \
                           "('Tusk', 100)," \
                           "('Skywrath Mage', 101)," \
                           "('Abaddon', 102)," \
                           "('Elder Titan', 103)," \
                           "('Legion Commander', 104)," \
                           "('Techies', 105)," \
                           "('Ember Spirit', 106)," \
                           "('Earth Spirit', 107)," \
                           "('Underlord', 108)," \
                           "('Terrorblade', 109)," \
                           "('Phoenix', 110)," \
                           "('Oracle', 111)," \
                           "('Winter Wyvern', 112)," \
                           "('Arc Warden', 113)," \
                           "('Monkey King', 114)," \
                           "('Dark Willow', 119)," \
                           "('Pangolier', 120)," \
                           "('Grimstroke', 121)," \
                           "('Hoodwink', 123)," \
                           "('Void Spirit', 126)," \
                           "('Snapfire', 128)," \
                           "('Mars', 129)," \
                           "('Dawnbreaker', 135)," \
                           "('Marci', 136)," \
                           "('Primal Beast', 137)," \
                           "('Muerta', 138)"
