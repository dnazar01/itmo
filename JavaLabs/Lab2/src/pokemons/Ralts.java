package pokemons;

import moves.ralts.Hypnosis;
import moves.ralts.ThunderWave;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;

public class Ralts extends Pokemon {
    public Ralts(String name, int level){
        super(name,level);
        setType(Type.PSYCHIC,Type.FAIRY);
        setStats(28,25,25,45,35,40);
        setMove(new ThunderWave(0,90), new Hypnosis(0,60));
    }
}
