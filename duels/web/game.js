// <constants>
const res = { x: 1280, y: 720};
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const talents = "";
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
        ctx.fillText(this.id, this.x, this.y + this.radius + 10);

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
// </globals>

let Render = () => {
    ctx.fillStyle = 'rgb(0, 0, 0)';
    ctx.fillRect(0, 0, res.x, res.y);

    nodes.forEach(node => {
        node.Think();
    });
};

let SetupGlobals = () => {
    nodes = [];
    mouse_data = {x: 0, y: 0};
    bounds = canvas.getBoundingClientRect();
};

let Think = () => {
    Render();
};

let Init = () => {
    SetupGlobals();

    //SetupListeners();

    setInterval(Think, 16.7);
};

Init();