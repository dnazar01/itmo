package pokemons;

import moves.audino.CalmMind;
import moves.audino.IceBeam;
import moves.audino.PlayNice;
import moves.audino.TakeDown;
import ru.ifmo.se.pokemon.Pokemon;
import ru.ifmo.se.pokemon.Type;

public class Audino extends Pokemon {
    public Audino(String name, int level) {
        super(name, level);
        super.setType(Type.NORMAL);
        super.setStats(103, 60, 86, 60, 86, 50);
        CalmMind calmMind = new CalmMind(0, 0);
        IceBeam iceBeam = new IceBeam(90, 100);
        PlayNice playNice = new PlayNice(0, 0);
        TakeDown takeDown = new TakeDown(90, 85);
        super.setMove(calmMind,iceBeam,playNice,takeDown);
    }
}
