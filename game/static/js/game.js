/**
 *
 * Created by tptak on 9/28/13.
 */

$(document).ready(function() {
	var username = $("#username").text();
	var usocket = io.connect('/users');

	usocket.emit('join',{
		'username': username,
		'gamestate': 3,
	});

});


var canvas = new fabric.Canvas('gamecanvas');


var HIDDEN = 0;
var SHOWN = 2;

function Tile(id, locLeft, locTop, size, canvas, game) {

    this.size = size;

    this.startPoints = [
        {x: -size / 2, y: -size / 2},
        {x: size / 2, y: -size / 2},
        {x: size / 2, y: size / 2},
        {x: -size / 2, y: size / 2}
    ];

    this.middlePoints = [
        {x: 0, y: -size * 0.6},
        {x: 0, y: -size * 0.4},
        {x: 0, y: size * 0.4},
        {x: 0, y: size * 0.6}
    ];

    this.endPoints = [
        {x: size / 2, y: -size / 2},
        {x: -size / 2, y: -size / 2},
        {x: -size / 2, y: size / 2},
        {x: size / 2, y: size / 2}
    ];

    this.animationPointsArray = [];
    this.animationPointsArray[0] = this.middlePoints;
    this.animationPointsArray[1] = this.endPoints;
    this.animationPointsArray[2] = this.middlePoints;
    this.animationPointsArray[3] = this.startPoints;
    this.defaultColor = 'green';


    this.canvas = canvas;
    this.locLeft = locLeft;
    this.locTop = locTop;
    this.id = id;
    this.rotationState = 0;

    this.animationTime = game.animationTime;
    this.animationProgress = 0;
    this.inMove = false;
    this.game = game;
//    this.picture = null;

}

Tile.prototype.putOnBoard = function () {
    var clonedStartPoints = this.startPoints.map(function (o) {
        return fabric.util.object.clone(o);
    });
    this.polygon = new fabric.Polygon(clonedStartPoints, {
        left: this.locLeft,
        top: this.locTop,
        fill: this.defaultColor,
        selectable: false,
        id: this.id

    });

    canvas.add(this.polygon);
};

Tile.prototype.removeFromBoard = function () {
    if (this.polygon) {
        this.canvas.remove(this.polygon);
        this.canvas.renderAll();
    }
};

Tile.prototype.addToCallbackCollection = function (collection) {
    collection[this.id] = this;
};


Tile.prototype.fillTile = function (objectToFill) {
    var obj = this;
    var pictureUrl = this.game.getPictureAssignment(objectToFill.id);
    fabric.Image.fromURL(pictureUrl, function (img) {

        img.scaleToWidth(obj.size);
        img.set({
            originX: 'left',
            originY: 'top'
        });

        var patternSourceCanvas = new fabric.StaticCanvas();
        patternSourceCanvas.add(img);

        var imgPattern = new fabric.Pattern({
            source: function () {
                patternSourceCanvas.setDimensions({
                    width: img.getWidth(),
                    height: img.getHeight()
                });
                return patternSourceCanvas.getElement();
            },
            repeat: 'repeat'
        });

        objectToFill.polygon.set('fill', imgPattern);

    });
};


Tile.prototype.animatePoint = function (i, prop, animationTime, endPoints, target) {
    var obj = this;
    fabric.util.animate({
        startValue: target.points[i][prop],
        endValue: endPoints[i][prop],
        duration: animationTime,
        easing: obj.rotationState % 2 ? fabric.util.ease['easeInSine'] : fabric.util.ease['easeOutSine'],
        onChange: function (value) {
            target.points[i][prop] = value;
            // only render once
            if (i === obj.startPoints.length - 1 && prop === 'y') {
                obj.canvas.renderAll();
            }
        },
        onComplete: function () {
            target.setCoords();
            if (i === obj.startPoints.length - 1 && prop === 'y' && target === obj.polygon) {
                // only start animation once
                obj.animationProgress += 1;
                obj.rotationState = (obj.rotationState + 1) % obj.animationPointsArray.length;
                if (obj.animationProgress < 2) {
                    obj.animate();
                } else {
                    obj.movementEnded();
                }

            }
        }
    });
};

Tile.prototype.animate = function () {
    if (this.rotationState == 1) {
//        this.polygon.set('fill', this.defaultColor);///*this.picture = */
        this.fillTile(this);
    } else if (this.rotationState == 3) {
        this.polygon.set('fill', this.defaultColor);
//            this.picture = null;
        }

        for (var i = 0, len = this.startPoints.length; i < len; i++) {

//            if (this.picture !== null) {
//              this.animatePoint(i, 'x', this.animationTime, this.animationPointsArray[this.rotationState], this.picture);
//            this.animatePoint(i, 'y', this.animationTime, this.animationPointsArray[this.rotationState], this.picture);
//
//            }
            this.animatePoint(i, 'x', this.animationTime, this.animationPointsArray[this.rotationState], this.polygon);
            this.animatePoint(i, 'y', this.animationTime, this.animationPointsArray[this.rotationState], this.polygon);
        }
    };

Tile.prototype.restrictedMove = function (fn) {
    if (!this.inMove) {
        this.inMove = true;
        fn();
    }
};

Tile.prototype.movementEnded = function () {
    this.inMove = false;
    this.game.selectionCallback();
};

Tile.prototype.toggle = function () {
    var obj = this;
    this.restrictedMove(function () {
        obj.animationProgress = 0;
        obj.animate();
    });

};

Tile.prototype.show = function () {
    if (this.rotationState === HIDDEN) {
        this.toggle();
    }
};


Tile.prototype.hide = function () {
    if (this.rotationState === SHOWN) {
        this.toggle();
    }
};

function Game(sizeX, sizeY, canvas) {
    this.sizeX = sizeX;
    this.sizeY = sizeY;
    this.size = 100;
    this.requiredSelection = 2;
    this.canvas = canvas;
    this.animationTime = 400;

    if ((sizeX * sizeY) % this.requiredSelection !== 0) {
        throw Error("Invalid config, cleaning the board will be impossible.");
    }

    this.callbackTiles = {};
    this.pictures = [];
    this.selectedTiles = [];

    this.isCallbackEnabled = true;

    this._preparePictures();

    this._setUpCallback();

    this._populateTiles();

    this._setRandomPictureAssignments();
}

Game.prototype._setRandomPictureAssignments = function () {
    var pics = [];
    var i, j, k;
    for (i = 0; i < this.sizeX * this.sizeY; i++) {
        pics.push(Math.floor(i / this.requiredSelection));
    }

    i = pics.length;
    while (--i) {
        j = Math.floor(Math.random() * (i + 1));
        var temp = pics[i];
        pics[i] = pics[j];
        pics[j] = temp;
    }

    this.assignments = {};
    for (i = 0, k = 0; i < this.sizeX; i++) {
        for (j = 0; j < this.sizeY; j++, k++) {
            this.assignments[j + '-' + i] = pics[k];
        }
    }
};

Game.prototype.getPictureAssignment = function (id) {
    return this.pictures[this.assignments[id]];
};


Game.prototype.selectionCallback = function () {
    var obj = this;
    if (this.selectedTiles.length >= this.requiredSelection) {
        setTimeout(function () {
            obj.removeOrHide.apply(obj)
        }, 500);
    }
};

Game.prototype.removeOrHide = function () {
    this.isCallbackEnabled = false;
    var obj = this;
    var timeout = (this.selectedTiles.length + 1) * this.animationTime / 2;
    if (this.requiredSelection < this.selectedTiles.length) {
        Console.log(this.selectedTiles.length + " tiles selected, " + this.requiredSelection + " expected");
    }

    var allEqual = this.areSelectedTilesEqual();

    if (allEqual) {
        this.manipulateTiles(Tile.prototype.removeFromBoard);

    } else {
        this.manipulateTiles(Tile.prototype.hide);

    }
    setTimeout(function () {
        obj.isCallbackEnabled = true;
    }, timeout);

};

Game.prototype.areSelectedTilesEqual = function () {

    var allEqual = true;

    var tmpVal = null;

    for (var i = 0; i < this.selectedTiles.length; i++) {
        var id = this.getPictureAssignment(this.selectedTiles[i].id);
        if (tmpVal) {
            if (id !== tmpVal) {
                allEqual = false;
                break;
            }
        } else {
            tmpVal = id;
        }
    }
    return allEqual;
};

Game.prototype.manipulateTiles = function (fn) {
    for (var i = 0; i < this.selectedTiles.length; i++) {
        var tile = this.selectedTiles[i];
        (function (tile) {
            setTimeout(function () {
                fn.call(tile);
            }, i * tile.animationTime / 2)
        })(tile);
    }
    this.selectedTiles.splice(0, this.selectedTiles.length);

};
//removeFromBoard
Game.prototype._populateTiles = function () {

    for (var c = 0, r = 0; r < this.sizeY;) {

        var tile = new Tile(r + '-' + c, this.size / 2 + c * this.size, this.size / 2 + r * this.size, 0.95 * this.size, this.canvas, this);
        tile.putOnBoard();
        tile.addToCallbackCollection(this.callbackTiles);

        c++;
        if (c === this.sizeX) {
            r++;
            c = 0;
        }
    }

};

Game.prototype._setUpCallback = function () {

    var obj = this;

    canvas.on('mouse:down', function (options) {
        if (options.target) {
            var target = obj.callbackTiles[options.target['id']];

            if (target && obj.isCallbackEnabled && obj.selectedTiles.length < obj.requiredSelection) {
                obj.selectedTiles.push(target);
                target.show();
            }
        }
    });

};

Game.prototype._preparePictures = function () {
    var im = ['ant.png', 'basketball.png', 'bike.png', 'bird.png', 'car.png', 'castanets.png', 'cat.png', 'chick.png', 'cow.png', 'cyclist.png', 'daffodil.png', 'deersign.png', 'earth.png', 'elephant.png', 'flipflops.png', 'food.png', 'grasshockey.png', 'halloween-bat.png', 'hammerthrow.png', 'heart.png', 'hendrix.png', 'hen.png', 'horse.png', 'iceskate.png', 'ladybug.png', 'leaf.png', 'morrison.png', 'oldcan.png', 'paderewski.png', 'sign.png', 'spider.png', 'stallman.png', 'swan.png', 'tabletennisracquet.png', 'target.png', 'turkey.png', 'vinyl.png', 'warn.png', 'weightlifting.png', 'whale.png'];
    var p = this.pictures;
    for (var i = 0; i < im.length; i++) {
        p.push('/static/img/tiles/' + im[i]);
    }
};


function sampleFill(canvas) {

    var tiles = {};

    canvas.on('mouse:down', function (options) {
        if (options.target) {
            var target = tiles[options.target['id']];
            target.toggle();
        }
    });

    var rows = 8;
    var cols = 10;

    for (var c = 0, r = 0; r < rows;) {

        var tile = new Tile(r + '-' + c, 50 + c * 100, 50 + r * 100, 95, canvas, null);
        tile.putOnBoard();
        tile.addToCallbackCollection(tiles);

        if (c === cols) {
            r++;
            c = 0;
        } else {
            c++;
        }
    }
}

//sampleFill(canvas);
var game = new Game(5, 4, canvas);
