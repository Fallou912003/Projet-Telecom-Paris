package robotsim.model;

import fr.tp.inf112.projects.canvas.model.Color;
import fr.tp.inf112.projects.canvas.model.RectangleShape;
import fr.tp.inf112.projects.canvas.model.Shape;
import fr.tp.inf112.projects.canvas.model.Stroke;
import fr.tp.inf112.projects.canvas.model.Style;
import fr.tp.inf112.projects.canvas.model.impl.RGBColor;

import java.util.List;
import java.util.ArrayList;

// the conveyer have a speed of functioning
public class ConveyorBelt extends Component {
    private double speed;
    private final List<Disk> carried = new ArrayList<>();
    private static final long serialVersionUID = 1L;

    public ConveyorBelt(Position pos, Dimension dim, String name, double speed) {
        super(pos, dim, name);
        this.speed = speed;
    }

    @Override
    public void behave() {
        for (Disk d : carried) {
            // to move the disk on the conveyer don't have enough time to finish it
            Position p = d.getPosition();
            p.setX(p.getX() + speed);
        }
    }

    public void load(Disk d) {
        carried.add(d);
        changed();
    }

    public void unload(Disk d) {
        if (carried.remove(d)) {
            changed();
        }
    }

    @Override
    public Shape getShape() {
        return new RectangleShape() {
            @Override public int getWidth()  { return (int)getDimension().getWidth(); }
            @Override public int getHeight() { return (int)getDimension().getHeigth(); }
        };
    }
 // color gray for the conveyer
    public Style getStyle() {
        return new Style() {
            @Override
            public Color getBackgroundColor() {
                return RGBColor.GRAY;
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
                    	return new float[]{6f, 6f};
                    }
                };
            }
        };
    }


    @Override
    public String toString() {
        return super.toString()
             + " ; speed=" + speed
             + " ; carried=" + carried.size();
    }
}