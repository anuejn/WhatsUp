/**
 * Created by jaro on 07.01.17.
 */

var num_nodes = 200;
var max_node_size = 50;
var distance_function = (a, b) => 1.0 / Math.pow(Math.abs(a - b), 0.001);
var num_min_links = 2;
var num_top_links = num_nodes;
var layout_params = {
    /**
     * Ideal length for links (springs in physical model).
     */
    springLength: 35,

    /**
     * Hook's law coefficient. 1 - solid spring.
     */
    springCoeff: 0.0008,

    /**
     * Coulomb's law coefficient. It's used to repel nodes thus should be negative
     * if you make it positive nodes start attract each other :).
     */
    gravity: -2.5,

    /**
     * Theta coefficient from Barnes Hut simulation. Ranged between (0, 1).
     * The closer it's to 1 the more nodes algorithm will have to go through.
     * Setting it to one makes Barnes Hut simulation no different from
     * brute-force forces calculation (each node is considered).
     */
    theta: 1,

    /**
     * Drag force coefficient. Used to slow down system, thus should be less than 1.
     * The closer it is to 0 the less tight system will be.
     */
    dragCoeff: 0.03,

    /**
     * Default time step (dt) for forces integration
     */
    timeStep : 5,

    /**
     * Maximum movement of the system which can be considered as stabilized
     */
    stableThreshold: 0.09
};
