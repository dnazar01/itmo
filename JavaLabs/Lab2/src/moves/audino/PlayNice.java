package moves.audino;

import ru.ifmo.se.pokemon.*;

public class PlayNice extends StatusMove {
    public PlayNice(double pow, double acc) {
        super(Type.NORMAL, pow, acc);
    }

    @Override
    protected void applyOppEffects(Pokemon p) {

        super.applyOppEffects(p);
        p.setMod(Stat.ATTACK,-1);
    }


    @Override
    protected String describe() {
        return "использует Play Nice";
    }
}
