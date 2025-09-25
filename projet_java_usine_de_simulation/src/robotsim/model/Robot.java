package robotsim.model;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import fr.tp.inf112.projects.canvas.model.*;
import fr.tp.inf112.projects.canvas.model.impl.RGBColor;
import robotsim.path.FactoryPathFinder;

/**
 * Un robot mobile dans l'usine.
 * Il se déplace sur une liste de composants et s'arrête après un cycle complet.
 */
public class Robot extends Component implements Serializable {
	private static final long serialVersionUID = 1L;

    private double speed;
    private final List<Component> route = new ArrayList<>();
    private int currentTargetIndex = 0;

    // for the path
    private transient FactoryPathFinder pathFinder;
    private List<Position> path = new ArrayList<>();
    private int pathPosIndex = 0;
    private Component lastTarget = null;
    
    // for making the robot returning on the first task of his list of mission
    private boolean returning = false;
    private boolean stopped   = false;

    public Robot(Position pos,
            Dimension dim,
            String name,
            double speed,
            FactoryPathFinder pathFinder) {
    	super(pos, dim, name);
    	this.speed      = speed;
    	this.pathFinder = pathFinder;
    }

    public double getSpeed() { return speed; }

    public void setSpeed(double speed) {
        this.speed = speed;
        changed();
    }

    public void setRoute(List<Component> newRoute) {
        route.clear();
        if (newRoute != null) {
            route.addAll(newRoute);
        }
        currentTargetIndex = 0;
        returning = false;
        stopped   = false;
        lastTarget = null;
        path.clear();
        pathPosIndex = 0;
    }
    
    public void setPathFinder(FactoryPathFinder pf) {
        this.pathFinder = pf;
    }

    @Override
    public void behave() {
        // conditions of stpo
        if (route.isEmpty() || pathFinder == null || stopped) {
            return;
        }

        // choice of the cible if it is for returning to the fist or not
        Component target = returning 
            ? route.get(0)
            : route.get(currentTargetIndex);

        // if target change since the last tick we recalculate the path
        if (target != lastTarget) {
            lastTarget   = target;
            path         = pathFinder.findPath(this, target);
            pathPosIndex = 0;
        }

        // 4) if the path is done
        if (pathPosIndex >= path.size()) {
            if (!returning) {
                // next component
                if (currentTargetIndex < route.size() - 1) {
                    currentTargetIndex++;
                } else {
                    returning = true;
                }
            } else {
                // to the first component
                stopped = true;
                changed(); 
                return;
            }
            
            return;
        }

        // 5) the way of the path
        Position next    = path.get(pathPosIndex);
        Position current = getPosition();
        double dx = next.getX() - current.getX();
        double dy = next.getY() - current.getY();

        if (Math.abs(dx) > Math.abs(dy)) {
            double step = Math.min(Math.abs(dx), speed);
            current.setX(current.getX() + Math.signum(dx) * step);
        } else {
            double step = Math.min(Math.abs(dy), speed);
            current.setY(current.getY() + Math.signum(dy) * step);
        }

        if ((int)current.getX() == (int)next.getX()
         && (int)current.getY() == (int)next.getY()) {
            pathPosIndex++;
        }
        changed();
    }

// version of moving without path and graphs
    public void moveToward(Component target) {
        Position pos = getPosition();
        double tx = target.getPosition().getX();
        double ty = target.getPosition().getY();
        double dx = tx - pos.getX();
        double dy = ty - pos.getY();

        boolean horizontal = Math.abs(dx) > Math.abs(dy);

        double step = Math.min(speed, horizontal ? Math.abs(dx) : Math.abs(dy));

        if (horizontal) {
            pos.setX(pos.getX() + Math.signum(dx) * step);
        } else {
            pos.setY(pos.getY() + Math.signum(dy) * step);
        }
        changed();
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
                return RGBColor.YELLOW;
            }
            @Override
            public Stroke getStroke() {
                return null;
            }
    	};
    }

    @Override
    public String toString() {
        return "Je m'appelle " + super.getName() +
               " et j'avance à " + speed + " unités/tick.";
    }
}
