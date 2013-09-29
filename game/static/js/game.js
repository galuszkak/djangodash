/**
 *
 * Created by tptak on 9/28/13.
 */


var canvas = new fabric.Canvas('gamecanvas');

function Tile(id, locLeft, locTop, size, canvas) {

    const HIDDEN = 0;
    const SHOWN = 2;

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

    this.rotationState = 0;
    this.animationTime = 400;
    this.animationProgress = 0;
//    this.picture = null;

    this.pictureUrl = 'https://si0.twimg.com/profile_images/1144713032/Red_Star_Stamp.jpg';


    var clonedStartPoints = this.startPoints.map(function (o) {
        return fabric.util.object.clone(o);
    });

    this.polygon = new fabric.Polygon(clonedStartPoints, {
        left: locLeft,
        top: locTop,
        fill: this.defaultColor,
        selectable: false,
        id: id

    });

    canvas.add(this.polygon);

    this.addToCallbackCollection = function (collection) {
        collection[id] = this;
    };


    this.fillObject = function (objectToFill, pictureUrl) {

        fabric.Image.fromURL(pictureUrl, function (img) {

            img.scaleToWidth(size);
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

            objectToFill.set('fill', imgPattern);

        });
    };


    this.animatePoint = function (i, prop, animationTime, endPoints, target) {
        var obj = this;
        fabric.util.animate({
            startValue: target.points[i][prop],
            endValue: endPoints[i][prop],
            duration: animationTime,
            easing: this.rotationState % 2 ? fabric.util.ease['easeInSine'] : fabric.util.ease['easeOutSine'],
            onChange: function (value) {
                target.points[i][prop] = value;
                // only render once
                if (i === obj.startPoints.length - 1 && prop === 'y') {
                    canvas.renderAll();
                }
            },
            onComplete: function () {
                console.log("ONCOMPLETE");
                target.setCoords();
                if (i === obj.startPoints.length - 1 && prop === 'y' && target === obj.polygon) {
                    // only start animation once
                    obj.animationProgress += 1;
                    obj.rotationState = (obj.rotationState + 1) % obj.animationPointsArray.length;
                    console.log(obj.rotationState);
                    if (obj.animationProgress < 2) {
                        obj.animate();
                    }

                }
            }
        });
    };

    this.animate = function () {
        console.log("START ANIMATE");
        if (this.rotationState == 1) {
            this.polygon.set('fill', /*this.picture = */this.fillObject(this.polygon, this.pictureUrl));
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
        console.log("END ANIMATE");
    };

    this.toggle = function () {
        this.animationProgress = 0;
        this.animate();
    };

    this.show = function () {
        if (this.rotationState = HIDDEN) {
            this.toggle();
        }
    };

    this.hide = function () {
        if (this.rotationState = SHOWN) {
            this.toggle();
        }
    };
}

function Game() {

}


function sampleFill(canvas) {

    var tiles = {};

    canvas.on('mouse:down', function (options) {
        if (options.target) {
            console.log('an object was clicked! ', options.target.type);
            var target = tiles[options.target['id']];
            target.toggle();
        }
    });

    var rows = 8;
    var cols = 10;

    for (var c = 0, r = 0; r < rows;) {

        var tile = new Tile(r + '-' + c, 50 + c * 100, 50 + r * 100, 95, canvas);
        tile.addToCallbackCollection(tiles);

        if (c === cols) {
            r++;
            c = 0;
        } else {
            c++;
        }
    }
}

sampleFill(canvas);
