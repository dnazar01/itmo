package pokemons;

import moves.gorebyss.ShadowBall;
import ru.ifmo.se.pokemon.Type;

public class Gorebyss extends Clamperl{
    public Gorebyss(String name, int level) {
        super(name, level);
        super.setType(Type.WATER);
        super.setStats(35, 64, 85, 74, 55, 32);
        ShadowBall shadowBall = new ShadowBall(80,100);
        super.setMove(shadowBall);
    }
}
