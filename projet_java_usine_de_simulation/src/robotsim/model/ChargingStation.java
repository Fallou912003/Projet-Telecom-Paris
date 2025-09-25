package robotsim.model;

import fr.tp.inf112.projects.canvas.model.*;
import fr.tp.inf112.projects.canvas.model.impl.RGBColor;

public class ChargingStation extends Component {
    private final double chargingRate;   // energy load per second
    private Robot occupant = null;       // loading robot (not have much time to code that part)
    private static final long serialVersionUID = 1L;
    public ChargingStation(Position pos, Dimension dim, String name, double chargingRate) {
        super(pos, dim, name);
        this.chargingRate = chargingRate;
    }

    public boolean occupy(Robot r) {
        if (occupant == null && r != null) {
            occupant = r;
            changed();  // notifier la vue
            return true;
        }
        return false;
    }

    // notify if it's busy or not
    public void release() {
        if (occupant != null) {
            occupant = null;
            changed();  // notifier la vue
        }
    }

    public boolean isOccupied() {
        return occupant != null;
    }

    public double getChargingRate() {
        return chargingRate;
    }

    /**
     * Comportement de la station : recharge l’occupant si présent.
     */
    @Override
    public void behave() {
        if (occupant != null) {
            // should be completed but the time
            changed();
        }
    }

    @Override
    public Shape getShape() {
        return new RectangleShape() {
            @Override public int getWidth()  { return (int)getDimension().getWidth();  }
            @Override public int getHeight() { return (int)getDimension().getHeigth(); }
        };
    }

    // charging station is blue
    @Override
    public Style getStyle() {
        return new Style() {
            @Override
            public Color getBackgroundColor() {
                return RGBColor.BLUE;
            }

            @Override
            public Stroke getStroke() {
                return new Stroke() {
                    @Override
                    public Color getColor() {
                        return RGBColor.BLACK;
                    }

                    @Override
                    public float getThickness() {
                        return 1.0f;
                    }

                    @Override
                    public float[] getDashPattern() {
                        return null;
                    }
                };
            }
        };
    }

    @Override
    public String toString() {
        return super.toString()
             + " ; chargingRate=" + chargingRate
             + " ; occupied=" + (occupant != null ? occupant.getName() : "none");
    }
}
