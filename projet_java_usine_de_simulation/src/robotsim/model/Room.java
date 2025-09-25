package robotsim.model;

import java.util.ArrayList;
import java.util.List;

import fr.tp.inf112.projects.canvas.model.Color;
import fr.tp.inf112.projects.canvas.model.RectangleShape;
import fr.tp.inf112.projects.canvas.model.Stroke;
import fr.tp.inf112.projects.canvas.model.Style;
import fr.tp.inf112.projects.canvas.model.impl.RGBColor;

// room can have everything beside factory
public class Room extends Component {
    private String purpose;
    private final List<Component> components = new ArrayList<>();
    private static final long serialVersionUID = 1L;

    public Room(String name, Position pos, Dimension dim, String purpose) {
        super(pos, dim, name);
        this.purpose = purpose;
    }

    public boolean addComponent(Component a) { return components.add(a); }
    public List<Component> getComponents()   { return components; }
    
    @Override
    public RectangleShape getShape() {
        return new RectangleShape() {
            @Override public int getWidth()  { return (int) getDimension().getWidth(); }
            @Override public int getHeight() { return (int) getDimension().getHeigth(); }
        };
    }
    
    @Override
    public Style getStyle() {
        return new Style() {
            @Override
            public Color getBackgroundColor() {
                // Gris clair pour la porte
                return null;
            }

            @Override
            public Stroke getStroke() {
                return new Stroke() {
                    @Override public Color getColor() {
                        return RGBColor.BLACK;
                    }
                    @Override public float getThickness() {
                        return 1.0f;
                    }
                    @Override public float[] getDashPattern() {
                        // tirets de longeur 5, espace 5
                        return new float[] {1.0f, 1.0f};
                    }
                };
            }
        };
    }

    @Override
    public String toString() {
        return super.toString()
             + " ; purpose=" + purpose
             + " ; nombreAires=" + components.size();
    }
}
