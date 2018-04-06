from scrapy.item import Item, Field

class Halftime(Item):
    # Identifier
    identifier = Field()
    accessed = Field()

    # Team names
    home_team = Field()
    away_team = Field()
    provider = Field()

    # Time and date
    date = Field()
    time = Field()

    # Odds
    home_home = Field()
    away_away = Field()
    draw_home = Field()
    draw_draw = Field()
    draw_away = Field()
    home_draw = Field()
    away_draw = Field()
    away_home = Field()
    home_away = Field()

    # Summary
    sum_odds = Field()
