package moves.kirlia;

import ru.ifmo.se.pokemon.*;

public class Charm extends StatusMove {
    public Charm(double pow, double acc) {
        super(Type.FAIRY, pow, acc);
    }

    @Override
    protected void applyOppEffects(Pokemon p) {

        super.applyOppEffects(p);
        p.setMod(Stat.ATTACK, -2);
    }


    @Override
    protected String describe() {
        return "использует Charm";
    }
}
