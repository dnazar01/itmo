package moves.clamperl;

import ru.ifmo.se.pokemon.*;

public class WaterPulse extends SpecialMove {
    public WaterPulse(double pow, double acc) {
        super(Type.WATER, pow, acc);
    }

    @Override
    protected void applyOppEffects(Pokemon p) {
        super.applyOppEffects(p);
        if(0.2>Math.random()){
            Effect.confuse(p);
        }
    }


    @Override
    protected String describe() {
        return "использует Water Pulse";
    }
}
