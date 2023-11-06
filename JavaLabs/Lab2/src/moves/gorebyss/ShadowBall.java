package moves.gorebyss;

import ru.ifmo.se.pokemon.*;

public class ShadowBall extends SpecialMove {
    public ShadowBall(double pow, double acc) {
        super(Type.GHOST, pow, acc);
    }

    @Override
    protected void applyOppEffects(Pokemon p) {
        if (0.2>Math.random()){
            p.setMod(Stat.SPECIAL_DEFENSE, -1);
        }
    }

    @Override
    protected String describe() {
        return "использует Shadow Ball";
    }
}
