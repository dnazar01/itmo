package pokemons;

import moves.clamperl.Blizzard;
import moves.clamperl.Rest;
import moves.clamperl.WaterPulse;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;

public class Clamperl extends Pokemon {
    public Clamperl(String name, int level) {
        super(name, level);
        super.setType(Type.WATER);
        super.setStats(35, 64, 85, 74, 55, 32);
        Blizzard blizzard = new Blizzard(110, 70);
        Rest rest = new Rest(0, 0);
        WaterPulse waterPulse = new WaterPulse(60, 100);
        super.setMove(blizzard, rest, waterPulse);
    }
}
