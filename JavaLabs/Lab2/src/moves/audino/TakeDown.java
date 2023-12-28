package moves.audino;

import ru.ifmo.se.pokemon.*;

public class TakeDown extends PhysicalMove {
    public TakeDown(double pow, double acc) {
        super(Type.NORMAL, pow, acc);
    }

    @Override
    protected void applySelfDamage(Pokemon p, double v) {

        super.applySelfDamage(p, p.getStat(Stat.ATTACK) * 0.25);
    }

    @Override
    protected String describe() {
        return "использует Take Down";
    }
}
