package robotsim.path;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import robotsim.model.*;

import fr.tp.inf112.projects.graph.*;
import fr.tp.inf112.projects.graph.Vertex;
import fr.tp.inf112.projects.graph.impl.*;

// Graph is used. 
public class GraphPathFinder implements FactoryPathFinder {

    private final Factory factory;
    private final int cellSize;

    public GraphPathFinder(Factory factory, int cellSize) {
        this.factory  = factory;
        this.cellSize = cellSize;
    }

    @Override
    public List<Position> findPath(Component source, Component target) {
        int cols = (factory.getWidth()  + cellSize - 1) / cellSize;
        int rows = (factory.getHeight() + cellSize - 1) / cellSize;

        // creation of graph sommets
        GridGraph graph = new GridGraph();
        Map<String,GridVertex> vertexMap = new HashMap<>();
        for (int x = 0; x < cols; x++) {
            for (int y = 0; y < rows; y++) {
                String label = x + "," + y;
                GridVertex v = new GridVertex(label, x, y);
                graph.addVertex(v);
                vertexMap.put(label, v);
            }
        }

        // 3) creation of aretes
        for (GridVertex v : vertexMap.values()) {
            int x = v.getxCoordinate(), y = v.getyCoordinate();
            String lbl;
            // droite
            if (x+1 < cols) {
                lbl = (x+1)+","+y;
                addGridEdge(graph, v, vertexMap.get(lbl));
            }
            // gauche
            if (x-1 >= 0) {
                lbl = (x-1)+","+y;
                addGridEdge(graph, v, vertexMap.get(lbl));
            }
            // bas
            if (y+1 < rows) {
                lbl = x+","+(y+1);
                addGridEdge(graph, v, vertexMap.get(lbl));
            }
            // haut
            if (y-1 >= 0) {
                lbl = x+","+(y-1);
                addGridEdge(graph, v, vertexMap.get(lbl));
            }
        }

        // 4) identify start and finish
        int sx = (int)source.getPosition().getX() / cellSize;
        int sy = (int)source.getPosition().getY() / cellSize;
        int tx = (int)target.getPosition().getX() / cellSize;
        int ty = (int)target.getPosition().getY() / cellSize;

        GridVertex start  = vertexMap.get(sx+","+sy);
        GridVertex finish = vertexMap.get(tx+","+ty);
        graph.setTargetVertex(finish);

        // Dijkstra algorithm
        List<Vertex> vertexPath = DijkstraAlgorithm.findShortestPath(graph, start, finish);

        // 6) Conversion path to list of positions
        List<Position> path = new ArrayList<>();
        for (Vertex v : vertexPath) {
            GridVertex gv = (GridVertex)v;
            double px = gv.getxCoordinate() * cellSize;
            double py = gv.getyCoordinate() * cellSize;
            path.add(new Position(px, py));
        }

        return path;
    }

    private void addGridEdge(Graph graph, GridVertex v1, GridVertex v2) {
        Edge e = new GridEdge((GridGraph)graph, v1, v2, 1);
        graph.addEdge(e);
        v1.addEdge(e);
        v2.addEdge(e);
    }
}