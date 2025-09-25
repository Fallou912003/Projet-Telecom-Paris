package robotsim.path;

import java.util.List;
import robotsim.model.Component;
import robotsim.model.Position;

public interface FactoryPathFinder {
    List<Position> findPath(Component source, Component target);
}
