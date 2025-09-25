package robotsim.model;

import fr.tp.inf112.projects.canvas.model.RectangleShape;

// not really used for the canva
public class Wall extends Component {
    private String material;
    private double thickness;
    private static final long serialVersionUID = 1L;

    public Wall(String name, Position pos, Dimension dim,
                String material, double thickness)
    {
        super(pos, dim, name);
        this.material  = material;
        this.thickness = thickness;
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
             + " ; material=" + material
             + " ; thickness=" + thickness;
    }
}
