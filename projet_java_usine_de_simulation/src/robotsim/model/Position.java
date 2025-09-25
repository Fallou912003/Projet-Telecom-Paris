package robotsim.model;

import java.io.Serializable;

public class Position implements Serializable{
	
	private double x, y;
	private Component owner;
	private static final long serialVersionUID = 1L;

    public Position (double x, double y) {
        this.x = x; this.y = y;
    }

    void setOwner(Component owner) {
        this.owner = owner;
    }

    public void setX(double x) {
        this.x = x;
        if (owner != null) owner.changed();
    }
    public void setY(double y) {
        this.y = y;
        if (owner != null) owner.changed();
    }
    public double getX() {
		return x;
	}

	public double getY() {
		return y;
	}
	

}
