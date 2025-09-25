package robotsim.model;

import fr.tp.inf112.projects.canvas.model.Color;
import fr.tp.inf112.projects.canvas.model.OvalShape;
import fr.tp.inf112.projects.canvas.model.Stroke;
import fr.tp.inf112.projects.canvas.model.Style;
import fr.tp.inf112.projects.canvas.model.impl.RGBColor;
// a disk have a weight and maybe different types
public class Disk extends Component {
    private String diskType;
    private double weight;
    private boolean processed;
    private static final long serialVersionUID = 1L;

    public Disk(String name, Position pos, Dimension dim,
                String diskType, double weight)
    {
        super(pos, dim, name);
        this.diskType = diskType;
        this.weight   = weight;
    }

    @Override
    public OvalShape getShape() {
        return new OvalShape() {
            @Override public int getWidth()  { return (int) getDimension().getWidth(); }
            @Override public int getHeight() { return (int) getDimension().getHeigth(); }
        };
    }
    
    @Override
    public Style getStyle() {
        return new Style() {
            @Override
            public Color getBackgroundColor() {
                return RGBColor.RED;
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
    
    public void setProcessed(boolean processed) {
        this.processed = processed;
        changed();
    }

    @Override
    public String toString() {
        return super.toString()
             + " ; type=" + diskType
             + " ; weight=" + weight
             + " ; processed=" + processed;
    }
}
