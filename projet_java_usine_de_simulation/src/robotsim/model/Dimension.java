package robotsim.model;

import java.io.Serializable;
// the dimension of the components (serializable for the factory part)
public class Dimension implements Serializable{
    private double heigth, width;
    private Component owner;
    private static final long serialVersionUID = 1L;

    public Dimension(double heigth, double width) {
        this.heigth = heigth; this.width = width;
    }

    void setOwner(Component owner) { this.owner = owner; }

    public double getHeigth() { return heigth; }
    public void setHeigth(double heigth) {
        this.heigth = heigth;
        if (owner != null) owner.changed();
    }

    public double getWidth() { return width; }
    public void setWidth(double width) {
        this.width = width;
        if (owner != null) owner.changed();
    }
}