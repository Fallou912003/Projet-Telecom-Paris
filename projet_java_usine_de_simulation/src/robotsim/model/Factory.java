package robotsim.model;
import fr.tp.inf112.projects.canvas.controller.*;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import fr.tp.inf112.projects.canvas.model.*;
// in the factory we can notify observers if we have any changing 
public class Factory extends Component implements Canvas, Observable, Serializable {
	private String id;
    private final List<Figure> components = new ArrayList<>();
    private volatile boolean simulationRunning = false;
    private static final long serialVersionUID = 1L;
    private transient List<Observer> observers;

    public Factory(String id, String name, int width, int height) {
    	super(new Position(0, 0), new Dimension(height, width), name);
        this.id = id;
    }


    @Override
    public String getId() { return id; }

    @Override
    public void setId(String id) { this.id = id; }
    
    private List<Observer> getObservers() {
        if (observers == null) {
            observers = new ArrayList<>();
        }
        return observers;
    }

    @Override
    public Collection<Figure> getFigures() {
        synchronized (components) {
            // iterate over a stable snapshot
            return new ArrayList<>(components);
        }
    }
    
    @Override public int    getWidth()                     { return (int)getDimension().getWidth(); }
    @Override public int    getHeight()                    { return (int)getDimension().getHeigth(); }

    @Override
    public Style getStyle() {
        return null;
    }
    // rectangle
    @Override
    public Shape getShape() {
        return new RectangleShape() {
            @Override public int getWidth()  { return getWidth(); }
            @Override public int getHeight() { return getHeight(); }
        };
    }

    private boolean isComponentNameUnique(String name) {
        for (Figure f : components) {
            if (f.getName().equals(name)) {
                return false;
            }
        }
        return true;
    }

    // like in first tps
    public boolean addComponent(Component c) {
        if (!isComponentNameUnique(c.getName())) {
            return false;
        }
        boolean added = components.add(c);
        if (added) {
            c.setFactory(this);
            c.getPosition().setOwner(this);
            c.getDimension().setOwner(this);
            notifyObservers();
        }
        return added;
    } 
    
    //for adding disks without making the name visible in the canva
    public boolean addComponent(Disk d) {
        boolean added = components.add(d);
        if (added) {
            d.setFactory(this);
            d.getPosition().setOwner(this);
            d.getDimension().setOwner(this);
            notifyObservers();
        }
        return added;
    } 
    
    @Override
    public void behave() {
        // for ensuring type matching
        List<Figure> snapshot = new ArrayList<>(components);

        for (Figure f : snapshot) {
            // cast for using behave
            if (f instanceof Component) {
                ((Component) f).behave();
            }
        }
        notifyObservers();
    }
    
    @Override
    public boolean addObserver(Observer o) {
        return getObservers().add(o);
    }

    @Override
    public boolean removeObserver(Observer o) {
        return getObservers().remove(o);
    }
    
    public void notifyObservers() {
        for (Observer o : getObservers()) {
            o.modelChanged();
        }
    }
    
    public void startSimulation() {
        simulationRunning = true;
        notifyObservers();
        while (simulationRunning) {
            behave();  // call behave on all components
            try {
                Thread.sleep(200);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }
    
    public void stopSimulation() {
        simulationRunning = false;
        notifyObservers();
    }
    
    public boolean isSimulationRunning() {
        return simulationRunning;
    }


    public void printToConsole() {
        System.out.println("Factory: " + super.getName());
        for (Figure f : components) {
            System.out.println(" - " + f);
        }
    }
}
