from peewee import *

db = SqliteDatabase("fighters.db")


class Boec(Model):
    name = CharField(unique=True)
    power = IntegerField(default=20)
    stun = IntegerField()
    health = IntegerField(default=100)

    class Meta:
        database = db
        table_name = "fighters"


db.create_tables([Boec])


def user_exists(name):
    try:
        Boec.get(Boec.name == name)
        return True
    except Boec.DoesNotExist:
        return False


def get_user(name):
    fighter = Boec.get(Boec.name == name)
    return fighter


def create_user(name):
    fighter = Boec.create(name=name)
    return fighter


def create_fighter(name, power, stun, health):
    fighter = Boec.create(name=name, power=power, stun=stun, health=health)
    fighter.save()
    return fighter


db.close()
