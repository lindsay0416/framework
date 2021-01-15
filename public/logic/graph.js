var nodeIds, shadowState, nodesArray, nodes, edgesArray, edges, network;

function startNetwork() {
    // this list is kept to remove a random node.. we do not add node 1 here because it's used for changes
    nodeIds = [2, 3, 4, 5];
    shadowState = false;

    // create an array with nodes
    nodesArray = [
        // {id: 1, label: "Node 1"},
        // {id: 2, label: "Node 2"},
        // {id: 3, label: "Node 3"},
        // {id: 4, label: "Node 4"},
        // {id: 5, label: "Node 5"},
    ];
    nodes = new vis.DataSet(nodesArray);

    // create an array with edges
    edgesArray = [
        // {id: "1", from: 1, to: 3},
        // {id: "2", from: 1, to: 2},
        // {id: "3", from: 2, to: 4},
        // {id: "4", from: 2, to: 5},
    ];
    edges = new vis.DataSet(edgesArray);

    // create a network
    var container = document.getElementById("mynetwork");
    var data = {
        nodes: nodes,
        edges: edges,
    };
    var options = {
    };
    network = new vis.Network(container, data, options);
}

function addNode() {
    var newId = (Math.random() * 1e7).toString(32);
    nodes.add({id: newId, label: "I'm new!"});
    nodeIds.push(newId);
    //add a link === added by Leo
    edges.add([
        {from: 1, to: newId},
        {from: 1, to: newId},
        {from: 2, to: newId},
        {from: 2, to: newId},
    ]);
}

function changeNode1() {
    var newColor =
        "#" + Math.floor(Math.random() * 255 * 255 * 255).toString(16);
    nodes.update([{id: 1, color: {background: newColor}}]);
}

function removeRandomNode() {
    var randomNodeId = nodeIds[Math.floor(Math.random() * nodeIds.length)];
    nodes.remove({id: randomNodeId});

    var index = nodeIds.indexOf(randomNodeId);
    nodeIds.splice(index, 1);
}

function changeOptions() {
    shadowState = !shadowState;
    network.setOptions({
        nodes: {shadow: shadowState},
        edges: {shadow: shadowState},
    });
}

function resetAllNodes() {
    nodes.clear();
    edges.clear();
    nodes.add(nodesArray);
    edges.add(edgesArray);
}

function resetAllNodesStabilize() {
    resetAllNodes();
    network.stabilize();
}

function setTheData() {
    nodes = new vis.DataSet(nodesArray);
    edges = new vis.DataSet(edgesArray);
    network.setData({nodes: nodes, edges: edges});
}

function resetAll() {
    if (network !== null) {
        network.destroy();
        network = null;
    }
    startNetwork();
}

function updateData(data) {
    nodes.clear();
    edges.clear();
    nodes.add(data["nodes"]);
    edges.add(data["edges"]);
    //network.setSelection(data["selection"]["nodes"]);
    //network.selectEdges(data["selection"]["edges"]);
    ops = {highlightEdges: false}
    network.setSelection(data["selection"],ops)
    console.log(data["selection"])
}

//牛皮 🐂 🍺
function helloWorld() {
    console.log("Hello World!")
} 

startNetwork();
