from app.models.video import Video
from app.models.model_utilities import date_to_str
from datetime import datetime, timedelta
import random

from app.db import db

def load():
    titles = [
        "Creature Of The Vacuum",
        "Soldier Of War",
        "Volunteer Of Aliens",
        "Director In The Portal",
        "Emperor Of The New World",
        "Commander Of The Flight",
        "Captain Of The Moon",
        "Foreigner Of New Earth",
        "Officer Of Darkness",
        "Mercenary Of Mars",
        "Droid Of The Stars",
        "Cyborg Of Our Destiny",
        "Traitor Of Time",
        "Beast Of The Worlds",
        "Director With Four Eyes",
        "Human With A Spaceship",
        "Robot Of The Worlds",
        "Mercenary Of Our Legacy",
        "Hero Of Outer Space",
        "Foreigner Of Our Future",
        "Defenders From The Portal",
        "Cyborgs Of The Past",
        "Medics In The Center Of The Earth",
        "Pilots Of The Universe",
        "Visitors Of Everywhere",
        "Enemies Of New Earth",
        "Women From The Portal",
        "Clones Of Our Ship",
        "Soldiers Of The Sands",
        "Defenders Of Death",
        "Strangers Of Our Culture",
        "Pilots In The Past",
        "Creators Of Everywhere",
        "Friends Of Our Legacy",
        "Guardians Of Our Ship",
        "Medics Of Men's Legacy",
        "Humans Of Mars",
        "Creatures Of The Void",
        "Martians Of The Sun",
        "Men With A UFO",
        "Girls And Androids",
        "Veterans And Friends",
        "Mercenaries And Beasts",
        "Doctors And Humans",
        "Figures And Invaders",
        "Mercenaries And Defenders",
        "Friends And Friends",
        "And Martians",
        "Veterans And Foreigners",
        "Friends And Figures",
        "Doctors And Boys",
        "Commanders And Strangers",
        "Assassins And Friends",
        "Beasts And Pilots",
        "Friends And Rebels",
        "Emperors And Visitors",
        "Robots And Defenders",
        "Emperors And Guests",
        "Enemies And Medics",
        "Androids And Robots",
        "Destiny Of The Orbit",
        "Border Of The Ocean",
        "Creation Of Earth",
        "Statue Of Eternity",
        "Hatred Of The Universe",
        "Honor Of The Sun",
        "Of The Ocean",
        "Planet Of Death",
        "Corruption Of The Sands",
        "Rise Of The Galaxy",
        "Inspiration Of Mars",
        "Inception Of Outer Space",
        "Extinction Of Time",
        "Star Of The Universe",
        "Love On Mars",
        "Nation Of The Worlds",
        "Origin Of The Past",
        "Moon Of The Worlds",
        "Scourge Of Death",
        "Ascension Of Outer Space",
        "Security Of The Galaxy",
        "Closed For The Vacuum",
        "Crazy Of Time Travel",
        "Understanding The End",
        "Lonely In The Secrets",
        "Better Solar Flares",
        "Abandoned By The New Age",
        "Limits Of The Depths",
        "Glory Of The Mists",
        "Defenseless Against My Planet",
        "Greed Of A Nuclear War",
        "Blind By Outer Space",
        "Lost In The Robotic Police",
        "Closed For The Moon",
        "Origin Of New Earth",
        "Afraid Of The Robotic Police",
        "Mystery Of Orbit",
        "Life After Eternity",
        "Complexity Of The New Age",
        "Hidden By A Nuclear Winter",
    ]

    def get_release_date(base_date=None):
        base_date = base_date or datetime.now()
        offset = random.randint(0, 365 * 60)
        return base_date + timedelta(days=offset)

    def get_total_inventory():
        return random.randint(1, 10)

    base_date = datetime(1950, 1, 1)

    for title in titles:
        params = dict(
            title=title,
            total_inventory=get_total_inventory(),
            release_date=date_to_str(get_release_date(base_date)),
        )

        v = Video(**params)
        db.session.add(v)

    db.session.commit()