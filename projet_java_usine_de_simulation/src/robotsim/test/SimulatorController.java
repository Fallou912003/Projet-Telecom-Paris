package robotsim.test;

import fr.tp.inf112.projects.canvas.controller.CanvasViewerController;
import fr.tp.inf112.projects.canvas.controller.Observer;
import fr.tp.inf112.projects.canvas.model.Canvas;
import fr.tp.inf112.projects.canvas.model.CanvasPersistenceManager;
import robotsim.model.Factory;

// for simulating in canva
public class SimulatorController implements CanvasViewerController {
    private Factory factoryModel;
    private final CanvasPersistenceManager persistenceManager;

    public SimulatorController(Factory factoryModel,
            CanvasPersistenceManager persistenceManager) {
    		this.factoryModel      = factoryModel;
    		this.persistenceManager = persistenceManager;
    }


    //Observable
    @Override
    public boolean addObserver(Observer o) {
        return factoryModel.addObserver(o);
    }

    @Override
    public boolean removeObserver(Observer o) {
        return factoryModel.removeObserver(o);
    }

    //CanvasViewerController
    @Override
    public Canvas getCanvas() {
        return factoryModel;
    }

    @Override
    public void setCanvas(Canvas canvasModel) {
        if (!(canvasModel instanceof Factory)) {
            throw new IllegalArgumentException("Canvas must be a Factory");
        }
        this.factoryModel = (Factory) canvasModel;
    }

    @Override
    public void startAnimation() {
        factoryModel.startSimulation();
    }

    @Override
    public void stopAnimation() {
        factoryModel.stopSimulation();
    }

    @Override
    public boolean isAnimationRunning() {
        return factoryModel.isSimulationRunning();
    }

    @Override
    public CanvasPersistenceManager getPersistenceManager() {
        return persistenceManager;
    }
}
