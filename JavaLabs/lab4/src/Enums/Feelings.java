package Enums;

public enum Feelings {
    SAD("грустно"),
    CALM("спокойно"),
    COMFORT("комфортно"),
    GOOD("хорошо"),
    CONFUSED("растерянно"),
    SOLID("убедительно"),
    COSY("уютно"),
    CLEVER("умно"),
    ANNOYED("раздраженно");

    private final String translation;

    Feelings(String translation) {
        this.translation = translation;
    }

    public String getTranslation() {
        return translation;
    }
}