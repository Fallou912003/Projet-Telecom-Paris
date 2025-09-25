package robotsim.test;

import fr.tp.inf112.projects.canvas.model.Canvas;
import fr.tp.inf112.projects.canvas.model.CanvasChooser;
import fr.tp.inf112.projects.canvas.model.Figure;
import fr.tp.inf112.projects.canvas.model.impl.AbstractCanvasPersistenceManager;
import robotsim.model.Factory;
import robotsim.model.Robot;
import robotsim.path.GraphPathFinder;

import java.io.*;
import java.util.Collection;

//Persistance of Canvas (Factory) on the disk by serialization.
 
public class FileCanvasPersistenceManager
    extends AbstractCanvasPersistenceManager {

    //length of cells
    private final int cellSize;

    public FileCanvasPersistenceManager(CanvasChooser canvasChooser, int cellSize) {
        super(canvasChooser);
        this.cellSize = cellSize;
    }

    @Override
    public void persist(Canvas canvasModel) throws IOException {
        String path = canvasModel.getId();
        if (!path.toLowerCase().endsWith(".sim")) {
            path = path + ".sim";
            canvasModel.setId(path);
        }
        try ( ObjectOutputStream out =
                  new ObjectOutputStream(new FileOutputStream(path)) ) {
            out.writeObject(canvasModel);
        }
    }

    @Override
    public Canvas read(String canvasId) throws IOException {
        Factory usine;
        try ( ObjectInputStream in =
                  new ObjectInputStream(new FileInputStream(canvasId)) ) {
            Object obj = in.readObject();
            usine = (Factory) obj;
        }
        catch (ClassNotFoundException e) {
            throw new IOException("Type de donnée inattendu dans " + canvasId, e);
        }

        // path to robot
        GraphPathFinder pf = new GraphPathFinder(usine, cellSize);
        Collection<Figure> figs = usine.getFigures();
        for (Figure f : figs) {
            if (f instanceof Robot) {
                ((Robot)f).setPathFinder(pf);
            }
        }

        return usine;
    }

    @Override
    public boolean delete(Canvas canvasModel) throws IOException {
        String path = canvasModel.getId();
        File file = new File(path);
        if (file.exists()) {
            if (!file.delete()) {
                throw new IOException("Impossible de supprimer le fichier " + path);
            }
            return true;
        }
        return false;
    }
}
