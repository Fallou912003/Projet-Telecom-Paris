package robotsim.test;

import robotsim.model.*;

// old class for tests
public class TestRobotizedFactory {
    public static void main(String[] args) {
        Factory usine = new Factory("Usine1", "robot fac", 800, 800);

        for (int i = 1; i <= 3; i++) {
            Room salle = new Room(
                "Salle" + i,
                new Position(0 + 10*i, 0),
                new Dimension(8, 6),
                "Purpose" + i
            );

            AreaProduction aire = new AreaProduction(
                "Aire" + i,
                new Position(1 + 10*i, 1),
                new Dimension(6, 4)
            );

            ProductionMachine machine = new ProductionMachine(
                "Machine" + i,
                new Position(2 + 10*i, 2),
                new Dimension(1, 1),
                "Type" + i,
                5.0
            );

            aire.addMachine(machine);
            salle.addComponent(aire);
            usine.addComponent(salle);
        }

    // robots
        /*for (int i = 1; i <= 3; i++) {
            Robot robot = new Robot(
                new Position(5, 5 + i),
                new Dimension(1, 1),
                "Robot" + i,
                0.0
            );
            usine.addComponent(robot);
        }

        ChargingStation station = new ChargingStation(
            "Charging1",
            new Position(3, 3),
            new Dimension(1, 1),
            0.2
        );
        usine.addComponent(station);*/

        usine.printToConsole();
    }
}
