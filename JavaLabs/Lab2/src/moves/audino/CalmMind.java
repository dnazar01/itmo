package moves.audino;

import ru.ifmo.se.pokemon.*;

public class CalmMind extends StatusMove {
    public CalmMind(double pow, double acc) {
        super(Type.PSYCHIC, pow, acc);
    }

    @Override
    protected void applySelfEffects(Pokemon p) {
        super.applySelfEffects(p);
        p.setMod(Stat.SPECIAL_DEFENSE, +1);
        p.setMod(Stat.SPECIAL_ATTACK, +1);
    }

    @Override
    protected String describe() {
        return "использует Calm Mind";
    }
}
