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
        this.cons.push(index);
    }

    Think()
    {
        var centerX = canvas.width / 2;
        var centerY = canvas.height / 2;
  
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI, false);
        ctx.fillStyle = 'white';
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
let target_node;
// </globals>

let Render = () => {
    ctx.fillStyle = 'rgb(0, 0, 0)';
    ctx.fillRect(0, 0, res.x, res.y);

    nodes.forEach(node => {
        node.Think();
    });
};

let GetClosestNode = () => {
    let closest = nodes[0];
    let closest_dist = 9999;

    nodes.forEach(node => {
        let a = node.x - mouse_data.x;
        let b = node.y - mouse_data.y;
        
        let dist = Math.sqrt(a * a + b * b);
        
        if(dist < closest_dist)
        {
            closest_dist = dist;
            closest = node;
        }
    });

    return closest;
};

let OnClick = () => {
    if(target_node == null)
    {
        target_node = GetClosestNode();
    }
    else
    {
        nodes[nodes.length] = new Node(mouse_data.x, mouse_data.y, "", "", nodes.length);
        nodes[nodes.length - 1].ConnectNode(target_node.id);

        nodes[target_node.id].ConnectNode(nodes[nodes.length-1]);

        target_node = null;
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
