// <constants>
const res = { x: 1280, y: 720};
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
// </constants>

// <classes>
class Node {
    constructor(x, y, name, label, id)
    {
        this.x = x;
        this.y = y;
        this.name = name;
        this.label = label;
        this.id = id;
        this.cons = [];
        this.radius = 10;
    }
    
    ConnectNode(index)
    {
        if(!this.cons.includes(index)){
            this.cons.push(index);
        }
    }

    Think()
    {
        var centerX = canvas.width / 2;
        var centerY = canvas.height / 2;
  
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
        ctx.fillStyle = this == target_node ? 'red' : 'white';
        ctx.fill();
        ctx.stroke();

        for(let i = 0; i < this.cons.length; i++)
        {
            // ctx.beginPath();
            // ctx.moveTo(this.x, this.y);
            // ctx.lineTo(nodes[this.cons[i]].x, nodes[this.cons[i]].y);
            // ctx.stroke();

            if(nodes[this.cons[i]] != undefined)
            {
                ctx.beginPath();
                ctx.moveTo(this.x, this.y);
                ctx.lineTo(nodes[this.cons[i]].x, nodes[this.cons[i]].y);
                ctx.fillStyle = 4;
                ctx.strokeStyle = "white";
                ctx.stroke();
                //console.log(nodes[this.cons[i]]);
            }
        }
    }
};
// </classes>

// <globals>
let nodes;
let mouse_data;
let bounds;
let put_mode;
// </globals>

let Render = () => {
    ctx.fillStyle = 'rgb(0, 0, 0)';
    ctx.fillRect(0, 0, res.x, res.y);

    nodes.forEach(node => {
        node.Think();
    });
};

function calc_dist(obja, objb){
    let a = obja.x - objb.x;
    let b = obja.y - objb.y;
    return Math.sqrt(a**2 + b**2);
}

function connect_pair(node_a, node_b){
    node_a.ConnectNode(node_b.id);
    node_b.ConnectNode(node_a.id);
}

let GetClosestNode = () => {
    let closest = nodes[0];
    let closest_dist = 9999;

    nodes.forEach(node => {
        let dist = calc_dist(node, mouse_data);
        
        if(dist < closest_dist)
        {
            closest_dist = dist;
            closest = node;
        }
    });

    return closest;
};

let OnClick = () => {
    if(put_mode){
        var close_node = GetClosestNode();
        var dist = calc_dist(close_node, mouse_data);
        if(dist < 30){
            connect_pair(target_node, close_node);
            // target_node = close_node; // set target to connected node
        }
        else{
            var nid = nodes.length; // new id
            nodes[nid] = new Node(mouse_data.x, mouse_data.y, "", "", nid);
            connect_pair(nodes[nid], target_node);
            // target_node = nodes[nid]; // set target to new node
        }
    }
    else{
        target_node = GetClosestNode();
    }
};

let SetupListeners = () => {
    canvas.addEventListener("mousemove", (evt) => {
        mouse_data.x = evt.clientX - bounds.left;
        mouse_data.y = evt.clientY - bounds.top;
    }, false);

    canvas.addEventListener("mousedown", function(evt) {
        OnClick();
    })
};

let SetupGlobals = () => {
    put_mode = true;
    nodes = [];
    nodes[0] = new Node(res.x / 2 - 10, res.y / 2 - 10, "", "", nodes.length);
    target_node = nodes[0];
    mouse_data = {x: 0, y: 0};
    bounds = canvas.getBoundingClientRect();
};

let Think = () => {
    Render();
};

let Init = () => {
    SetupGlobals();

    SetupListeners();

    setInterval(Think, 16.7);
};

Init();

function toggle_mode(){
    // toggle put mode and update page text
    if(put_mode){
        put_mode = false;
        document.getElementById("status").innerHTML = "SELECT";
    }
    else{
        put_mode = true;
        document.getElementById("status").innerHTML = "PUT";
    }
}

document.addEventListener("keypress", function onEvent(event) {
    if (event.key === "f") {
        toggle_mode();
    }
});
