package robotsim.model;

import fr.tp.inf112.projects.canvas.model.*;
import fr.tp.inf112.projects.canvas.model.impl.RGBColor;

// can specify the type of product, the cycle of production
public class ProductionMachine extends Component {
    private final String productType;
    private final double cycleTime;
    private boolean busy = false;
    private double timer = 0;
    private static final long serialVersionUID = 1L;

    // for calculating distances 
    private int producedCount = 0;
    private final double diskDiameter = 3.0;   // correspond à Disk dimension
    private final double margin = 1.0;         // space between disks

    public ProductionMachine(String name, Position pos, Dimension dim,
                             String productType, double cycleTime) {
        super(pos, dim, name);
        this.productType = productType;
        this.cycleTime   = cycleTime;
    }

    @Override
    public Shape getShape() {
        return new RectangleShape() {
            @Override public int getWidth()  { return (int) getDimension().getWidth();  }
            @Override public int getHeight() { return (int) getDimension().getHeigth(); }
        };
    }
    
    @Override
    public Style getStyle() {
        return new Style() {
            @Override
            public Color getBackgroundColor() {
                return RGBColor.GREEN;
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
    public void behave() {
        if (!busy) {
            busy = true;
            timer = 0;
            changed();
        } else {
            timer += 1; // tick
            if (timer >= cycleTime) {
                busy = false;
                timer = 0;

                // Calculate number of disk per row
                int disksPerRow = (int) ((getDimension().getWidth() + margin)
                                        / (diskDiameter + margin));
                if (disksPerRow < 1) disksPerRow = 1;

                // Calculate rows and cols offsets 
                int row = producedCount / disksPerRow;
                int col = producedCount % disksPerRow;
                double offsetX = col * (diskDiameter + margin);
                double offsetY = row * (diskDiameter + margin);

                // created disk on the good position
                Disk d = new Disk(
                    "",
                    new Position(
                        getPosition().getX() + offsetX,
                        getPosition().getY() + offsetY
                    ),
                    new Dimension(diskDiameter, diskDiameter),
                    productType,
                    0.1
                );
                producedCount++;
                changed();
                getFactory().addComponent(d);
            }
        }
    }

    @Override
    public String toString() {
        return super.toString()
             + " ; produit=" + productType
             + " ; cycleTime=" + cycleTime
             + " ; busy=" + busy
             + " ; count=" + producedCount;
    }
}
