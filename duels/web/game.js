// <constants>
const res = { x: 1280, y: 720};
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const talents = [{"x":630,"y":350,"name":"","label":"","id":0,"cons":[1,3,9,14],"radius":10},{"x":739.0028409957886,"y":240.00284099578857,"name":"","label":"","id":1,"cons":[0,2,7],"radius":10},{"x":779.0028409957886,"y":145.00284099578857,"name":"","label":"","id":2,"cons":[1],"radius":10},{"x":471.0028409957886,"y":315.0028409957886,"name":"","label":"","id":3,"cons":[0,4],"radius":10},{"x":356.0028409957886,"y":217.00284099578857,"name":"","label":"","id":4,"cons":[3,5],"radius":10},{"x":335.0028409957886,"y":109.00284099578857,"name":"","label":"","id":5,"cons":[4,6],"radius":10},{"x":226.00284099578857,"y":40.002840995788574,"name":"","label":"","id":6,"cons":[5],"radius":10},{"x":874.0028409957886,"y":216.00284099578857,"name":"","label":"","id":7,"cons":[1,8],"radius":10},{"x":1001.0028409957886,"y":133.00284099578857,"name":"","label":"","id":8,"cons":[7],"radius":10},{"x":553.0028409957886,"y":245.00284099578857,"name":"","label":"","id":9,"cons":[0,10,12,13],"radius":10},{"x":603.0028409957886,"y":94.00284099578857,"name":"","label":"","id":10,"cons":[9,11],"radius":10},{"x":468.0028409957886,"y":45.002840995788574,"name":"","label":"","id":11,"cons":[10],"radius":10},{"x":443.0028409957886,"y":212.00284099578857,"name":"","label":"","id":12,"cons":[9],"radius":10},{"x":514.0028409957886,"y":165.00284099578857,"name":"","label":"","id":13,"cons":[9],"radius":10},{"x":485.0028409957886,"y":375.0028409957886,"name":"","label":"","id":14,"cons":[0,15],"radius":10},{"x":495.0028409957886,"y":440.0028409957886,"name":"","label":"","id":15,"cons":[14,16,20],"radius":10},{"x":189.00284099578857,"y":289.0028409957886,"name":"","label":"","id":16,"cons":[15,16,16,17,19],"radius":10},{"x":9.002840995788574,"y":407.0028409957886,"name":"","label":"","id":17,"cons":[16,18],"radius":10},{"x":40.002840995788574,"y":222.00284099578857,"name":"","label":"","id":18,"cons":[17],"radius":10},{"x":123.00284099578857,"y":266.0028409957886,"name":"","label":"","id":19,"cons":[16],"radius":10},{"x":230.00284099578857,"y":421.0028409957886,"name":"","label":"","id":20,"cons":[15,21,22],"radius":10},{"x":156.00284099578857,"y":491.0028409957886,"name":"","label":"","id":21,"cons":[20],"radius":10},{"x":287.0028409957886,"y":522.0028409957886,"name":"","label":"","id":22,"cons":[20],"radius":10}];
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

    Load(obj)
    {
        this.x = obj.x;
        this.y = obj.y;
        this.name = obj.name;
        this.label = obj.label;
        this.id = obj.id;
        this.cons = obj.cons;
        this.radius = obj.radius;
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
        ctx.fillStyle = 'white';
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

let Unpack = () => {
    for(let i = 0; i < talents.length; i++)
    {
        let node = new Node(0, 0, "", "", 0);
        node.Load(talents[i]);
        nodes.push(node);
    }
};

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

    Unpack();

    setInterval(Think, 16.7);
};

Init();