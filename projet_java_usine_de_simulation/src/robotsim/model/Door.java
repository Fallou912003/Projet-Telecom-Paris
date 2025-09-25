package robotsim.model;

import fr.tp.inf112.projects.canvas.model.*;
import fr.tp.inf112.projects.canvas.model.impl.RGBColor;
// a door can be open or close but I didn't finish it at all
public class Door extends Component {
    private Room roomA, roomB;
    private boolean isOpen;
    private double openTime, closeTime;
    private static final long serialVersionUID = 1L; 

    public Door(String name,
                Position pos,
                Dimension dim,
                Room roomA,
                Room roomB,
                double openTime,
                double closeTime)
    {
        super(pos, dim, name);
        this.roomA     = roomA;
        this.roomB     = roomB;
        this.setOpenTime(openTime);
        this.setCloseTime(closeTime);
        this.isOpen    = false;
    }

    public void open()   { isOpen = true; }
    public void close()  { isOpen = false; }
    public boolean isOpen() { return isOpen; }

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
                return RGBColor.BLACK;
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
                        return new float[] {5.0f, 5.0f};
                    }
                };
            }
        };
    }

    @Override
    public String toString() {
        return super.toString()
             + " ; relie=" + roomA.getName() + "↔" + roomB.getName()
             + " ; état="  + (isOpen ? "ouverte" : "fermée");
    }

	public double getCloseTime() {
		return closeTime;
	}

	public void setCloseTime(double closeTime) {
		this.closeTime = closeTime;
	}

	public double getOpenTime() {
		return openTime;
	}

	public void setOpenTime(double openTime) {
		this.openTime = openTime;
	}
}
