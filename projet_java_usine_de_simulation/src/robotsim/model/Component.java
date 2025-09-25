package robotsim.model;

import java.io.Serializable;

import fr.tp.inf112.projects.canvas.model.*;
// for all components
public abstract class Component implements Figure, Serializable {
    private final String name;
    private final Position pos;
    private final Dimension dim;
    private Factory factory;
    private static final long serialVersionUID = 1L;

    public Component(Position pos, Dimension dim, String name) {
        this.name = name;
        this.pos  = pos;
        this.dim  = dim;
    }

    @Override
    public final String getName() {
        return name;
    }
    
    void setFactory(Factory factory) {
        this.factory = factory;
    }
    
    protected void changed() {
        if (factory != null) {
            factory.notifyObservers();
        }
    }
    

    public Factory getFactory() {
		return factory;
	}

	@Override
    public int getxCoordinate() {
        return (int) pos.getX();
    }

    @Override
    public int getyCoordinate() {
        return (int) pos.getY();
    }

    @Override
    public Style getStyle() {
        return null;
    }

    @Override
    public abstract Shape getShape();

    public void behave() {};

    public Position getPosition() { return pos; }
    public Dimension getDimension() { return dim; }

    @Override
    public String toString() {
        return "Component " + name
             + ": position x=" + pos.getX() + " & y=" + pos.getY()
             + " ; dimension heigth=" + dim.getHeigth() + " & width=" + dim.getWidth();
    }
}