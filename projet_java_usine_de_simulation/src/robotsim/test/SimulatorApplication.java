package robotsim.test;

import robotsim.model.*;
import robotsim.path.*;

import java.util.logging.Logger;
import fr.tp.inf112.projects.canvas.view.*;
import fr.tp.inf112.projects.canvas.model.*;

import java.util.Arrays;
import java.util.List;

// simulation of my factory
// unfortunately I didn't have enough time to finish the part of obstacles 
public class SimulatorApplication {
	private static final Logger LOGGER =
	        Logger.getLogger(SimulatorApplication.class.getName());
	public static void main(String[] args) {
		LOGGER.info("Starting the robot simulator...");
        LOGGER.config("With parameters: " + Arrays.toString(args) + "'.");
        
        // construction of factory
		Factory usine = new Factory("usine1", "Robot factory", 800, 600);
		Room salle1 = new Room("Packaging room 1", new Position(20, 20), new Dimension(200, 300), "Packaging");
		AreaProduction aire1 = new AreaProduction("Packaging Area 1", new Position(50, 50), new Dimension(100, 130));
		ProductionMachine m1 = new ProductionMachine("Machine 1", new Position(80, 80), new Dimension(50, 50), "TypeA",
				10.0);
		Room salle2 = new Room("Packaging room 2", new Position(320, 20), new Dimension(200, 300), "Packaging");
		AreaProduction aire2 = new AreaProduction("Packaging Area 2", new Position(410, 50), new Dimension(100, 130));
		ProductionMachine m2 = new ProductionMachine("Machine 2", new Position(410, 80), new Dimension(40, 40), "TypeB",
				10.0);
		Door door1 = new Door("Door1",
                new Position(320, 60),
                new Dimension(50, 5),
                salle1, salle2, 0, 0);
		Room salle3 = new Room("stock and sorting", new Position(70, 220), new Dimension(300, 400), "Stock and Sorting");
		Door door2 = new Door("Door2",
                new Position(400, 220),
                new Dimension(5, 50),
                salle2, salle3, 0, 0);
		ChargingStation station1 = new ChargingStation(new Position(470, 70), new Dimension(50, 50), "Charging point 1", 100);
		ChargingStation station2 = new ChargingStation(new Position(280, 150), new Dimension(50, 20), "Charging point 2", 70);
		
		ConveyorBelt conveyor = new ConveyorBelt(new Position(60, 470), new Dimension(40, 350), "Conveyor", 1.0);
		Door door3 = new Door("Door3",
                new Position(80, 220),
                new Dimension(5, 50),
                salle1, salle3, 0, 0);
		AreaProduction aire3 = new AreaProduction("Costumer delivery area", new Position(20, 460), new Dimension(60, 40));
		AreaProduction aire4 = new AreaProduction("Stock Area 1", new Position(400, 420), new Dimension(100, 60));
		AreaProduction aire5 = new AreaProduction("Stock Area 2", new Position(300, 320), new Dimension(100, 60));
		AreaProduction aire6 = new AreaProduction("Sorting Area", new Position(120, 320), new Dimension(100, 60));
		Room salle4 = new Room("Chilling room", new Position(470, 220), new Dimension(100, 100), "Charging");
		usine.addComponent(salle4);
		Door door4 = new Door("Door4",
                new Position(470, 230),
                new Dimension(50, 5),
                salle3, salle4, 0, 0);
		usine.addComponent(door4);
		salle3.addComponent(door4);
		salle4.addComponent(door4);
		Door door5 = new Door("Door5",
                new Position(500, 220),
                new Dimension(5, 50),
                salle2, salle4, 0, 0);
		ChargingStation station3 = new ChargingStation(new Position(500, 250), new Dimension(50, 50), "Charging point 3", 100);
		Door door6 = new Door("Door6",
                new Position(260, 220),
                new Dimension(5, 50),
                salle1, salle3, 0, 0);
		usine.addComponent(door6);
		salle1.addComponent(door6);
		salle3.addComponent(door6);
		usine.addComponent(station3);
		salle4.addComponent(station3);
		usine.addComponent(door5);
		salle3.addComponent(door5);
		salle4.addComponent(door5);
		usine.addComponent(aire4);
		usine.addComponent(aire5);
		usine.addComponent(aire6);
		usine.addComponent(aire3);
		salle3.addComponent(aire4);
		salle3.addComponent(aire5);
		salle3.addComponent(aire6);
		salle1.addComponent(door3);
		salle3.addComponent(door3);
		usine.addComponent(door3);
		usine.addComponent(conveyor);
		usine.addComponent(salle3);
		salle3.addComponent(door2);
		salle2.addComponent(station1);
		aire2.addMachine(station1);
		usine.addComponent(station1);
		salle2.addComponent(station2);
		aire2.addMachine(station2);
		usine.addComponent(station2);
		usine.addComponent(door1);
		usine.addComponent(door2);
		salle1.addComponent(door1);
		salle2.addComponent(door2);
		aire1.addMachine(m1);
		aire2.addMachine(m2);
		salle1.addComponent(aire1);
		salle2.addComponent(aire2);
		usine.addComponent(salle1);
		usine.addComponent(aire1);
		usine.addComponent(m1);
		usine.addComponent(salle2);
		usine.addComponent(m2);
		usine.addComponent(aire2);
		GraphPathFinder pf = new GraphPathFinder(usine, 20);
		Robot r1 = new Robot(new Position(250, 90), new Dimension(20, 20), "Robot1", 3.0, pf);
		Robot r2 = new Robot(new Position(350, 90), new Dimension(15, 15), "Robot2", 2.0, pf);
		Robot r3 = new Robot(new Position(250, 250), new Dimension(25, 25), "Robot3", 4.0, pf);
		Robot r4 = new Robot(new Position(300, 250), new Dimension(20, 20), "Robot4", 5.0, pf);
		Robot r5 = new Robot(new Position(410, 200), new Dimension(10, 10), "Robot5", 3.0, pf);
		Robot r6 = new Robot(new Position(150, 300), new Dimension(17, 17), "Robot6", 5.0, pf);
		usine.addComponent(r1);
		usine.addComponent(r2);
		usine.addComponent(r3);
		usine.addComponent(r4);
		usine.addComponent(r5);
		usine.addComponent(r6);
		r1.setRoute(List.of(m1, aire6, aire5, station3));
		r2.setRoute(List.of(m2, station1, m1, aire4));
		r3.setRoute(List.of(station3, m2, m1, m2, station2, aire6, m2));
		r4.setRoute(List.of(m2, m1, m2, station2, aire4, aire5, aire6, station3));
		r5.setRoute(List.of(station1, m1, m2, m1, aire5, m1));
		r6.setRoute(List.of(station2, m2, m1, station2, aire6, aire5));

		//instances for canva 
		CanvasChooser chooser = new FileCanvasChooser("sim", "Simulation");
		FileCanvasPersistenceManager pm = new FileCanvasPersistenceManager(chooser, 20);
		SimulatorController controller = new SimulatorController(usine, pm);
		CanvasViewer viewer = new CanvasViewer(controller);
		controller.addObserver(viewer);
		usine.printToConsole();
	}
}
