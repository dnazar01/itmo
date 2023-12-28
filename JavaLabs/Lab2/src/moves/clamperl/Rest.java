package moves.clamperl;

import ru.ifmo.se.pokemon.*;

import static ru.ifmo.se.pokemon.Stat.HP;

public class Rest extends StatusMove {
    public Rest(double pow, double acc) {
        super(Type.PSYCHIC, pow, acc);
    }

    @Override
    protected void applySelfEffects(Pokemon p) {

        Effect e = new Effect().turns(2).condition(Status.SLEEP);
        p.setMod(Stat.HP, (int)(p.getHP()-p.getStat(HP)));
        p.addEffect(e);
    }

    @Override
    protected String describe() {
        return "использует Rest";
    }
}
