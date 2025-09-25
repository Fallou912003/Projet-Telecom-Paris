package robotsim.model;

import java.util.ArrayList;
import java.util.List;

import fr.tp.inf112.projects.canvas.model.*;
import fr.tp.inf112.projects.canvas.model.impl.RGBColor;
// in area production we can have machines and also charging points
public class AreaProduction extends Component {
    private final List<Component> machines = new ArrayList<>();
    private static final long serialVersionUID = 1L;

    public AreaProduction(String name, Position pos, Dimension dim) {
        super(pos, dim, name);
    }
// for adding charging points and machines
    public boolean addMachine(Component m) { return machines.add(m); }
    public List<Component> getMachines()   { return machines; }
    
    // it's for patterns in the canva
    @Override
    public Style getStyle() {
        return new Style() {
            @Override
            public Color getBackgroundColor() {
                // pas de fond
                return null;
            }

            @Override
            public Stroke getStroke() {
                return new Stroke() {
                    @Override
                    public Color getColor() {
                        return RGBColor.BLACK;           // couleur du contour
                    }

                    @Override
                    public float getThickness() {
                        return 1.0f;                     // épaisseur
                    }

                    @Override
                    public float[] getDashPattern() {
                        // longueur alternée : 6 unités de trait, 6 unités d’espace
                        return new float[]{6f, 6f};
                    }
                };
            }
        };
    }

    @Override
    public RectangleShape getShape() {
        return new RectangleShape() {
            @Override public int getWidth()  { return (int) getDimension().getWidth(); }
            @Override public int getHeight() { return (int) getDimension().getHeigth(); }
        };
    }

    @Override
    public String toString() {
        return super.toString()
             + " ; nombreMachines=" + machines.size();
    }
}
