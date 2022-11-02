"use strict ";

class Book {
    constructor(ctx) {
        this.ctx = ctx;
        this.vec3 = glMatrix.vec3;
        this.vt = 0;
        this.viewAngle = 0;
        this.fill = true;
        this.stroke = true;
        this.sliderValue;
        this.sliderControl = false;
    }

    //from github
    lineToTx(loc,Tx)
    {
        var res = this.vec3.create(); 
        this.vec3.transformMat4(res,loc,Tx); 
        this.ctx.lineTo(res[0],res[1]);
    }

    //from github
    moveToTx(loc,Tx)
    {
        var res = this.vec3.create(); 
        this.vec3.transformMat4(res,loc,Tx); 
        this.ctx.moveTo(res[0],res[1]);
    }

    drawObject(color,TxU,scale) {
        var Tx = mat4.clone(TxU);
        mat4.scale(Tx,Tx,[scale,scale,scale]);
        this.ctx.beginPath();
	    this.ctx.fillStyle = color;
	    moveToTx([-.05,-.35,.3],Tx);
	    lineToTx([-.05,.05,0],Tx);
        lineToTx([.05,.05,0],Tx);
      	lineToTx([.1,0,0],Tx);
	    lineToTx([.05,-.05,0],Tx);
	    this.ctx.closePath();
	    this.ctx.fill();
	}

    CameraCurve(viewAngle) {
        var distance = 120.0;
        var eye = this.vec3.create();
        eye[0] = distance*Math.sin(viewAngle);
        eye[1] = 100;
        eye[2] = distance*Math.cos(viewAngle);  
        return [eye[0],eye[1],eye[2]];
    }

    drawSidePlate(TxU,scale) {
        this.ctx.strokeStyle = 'black';
        this.ctx.fillStyle = `rgb(160,160,160)`;
        var Tx = glMatrix.mat4.clone(TxU);
        glMatrix.mat4.scale(Tx,Tx,[scale,scale,scale]);
        this.ctx.beginPath();
        this.moveToTx([-1.4,0.2,.45],Tx);
        this.lineToTx([-2.1,0.9,.45],Tx);
        this.lineToTx([-2.1,0.9,-.45],Tx);
        this.lineToTx([-1.4,0.2,-.45],Tx);
        this.lineToTx([-1.4,0.2,.45],Tx);
        if(this.fill) this.ctx.fill();

        if(this.stroke) this.ctx.stroke();
    }

    drawUpVector(TxU,scale) {
        this.ctx.strokeStyle = 'black';
        var Tx = glMatrix.mat4.clone(TxU);
        glMatrix.mat4.scale(Tx,Tx,[scale,scale,scale]);
        this.ctx.beginPath();
        this.moveToTx([0,0,0],Tx);
        this.lineToTx([0,1,0],Tx);
        this.ctx.stroke();
    }

    drawCube(TxU,scale, x, y, z, xoff, yoff, zoff, color) {
        var fill = this.fill;
        var stroke = this.stroke;
        var Tx = glMatrix.mat4.clone(TxU);
        glMatrix.mat4.scale(Tx,Tx,[scale,scale,scale]);

        this.ctx.strokeStyle = 'black';
        this.ctx.fillStyle = color;
        this.ctx.beginPath();

      
        //base
        this.moveToTx([-x + xoff, 0 + yoff, -z + zoff],Tx);
        this.lineToTx([-x + xoff, 0 + yoff,z + zoff],Tx);
        this.lineToTx([x + xoff, 0 + yoff,z + zoff],Tx); 
        this.lineToTx([x + xoff, 0 + yoff,-z + zoff],Tx);
        this.lineToTx([-x + xoff, 0 + yoff,-z + zoff],Tx);
        if(fill) this.ctx.fill();

        //North side
        this.lineToTx([-x + xoff,y + yoff,-z + zoff],Tx);
        this.lineToTx([-x + xoff,y + yoff,z + zoff],Tx);
        this.lineToTx([-x + xoff,0 + yoff,z + zoff],Tx);
        if(fill) this.ctx.fill();

        //East side
        this.moveToTx([-x + xoff,y + yoff,-z + zoff],Tx);
        this.lineToTx([x + xoff,y + yoff,-z + zoff],Tx);
        this.lineToTx([x + xoff,0 + yoff,-z + zoff],Tx);
        this.lineToTx([-x + xoff,0 + yoff,-z + zoff],Tx);
        if(fill) this.ctx.fill();

        //South side
        this.moveToTx([x + xoff,0 + yoff,z + zoff],Tx);
        this.lineToTx([x + xoff,y + yoff,z + zoff],Tx);
        this.lineToTx([x + xoff,y + yoff,-z + zoff],Tx);
        this.lineToTx([x + xoff,0 + yoff,-z + zoff],Tx);
        this.lineToTx([x + xoff,0 + yoff,z + zoff],Tx);
        if(fill) this.ctx.fill();

        //West side
        this.moveToTx([-x + xoff,y + yoff,z + zoff],Tx);
        this.lineToTx([x + xoff,y + yoff,z + zoff],Tx);
        this.lineToTx([x + xoff,0 + yoff,z + zoff],Tx);
        this.lineToTx([-x + xoff,0 + yoff,z + zoff],Tx);
        this.lineToTx([-x + xoff,y + yoff,z + zoff],Tx);
        if(fill) this.ctx.fill();

        //Top Side
        this.moveToTx([-x + xoff,y + yoff,-z + zoff],Tx);
        this.lineToTx([-x + xoff,y + yoff,z + zoff],Tx);
        this.lineToTx([x + xoff,y + yoff,z + zoff],Tx); 
        this.lineToTx([x + xoff,y + yoff,-z + zoff],Tx);
        this.lineToTx([-x + xoff,y + yoff,-z + zoff],Tx);
        if(fill) this.ctx.fill();

        if(stroke) this.ctx.stroke();
	}
    
    draw() {
        // Create Camera (lookAt) transform
        var eyeCamera = this.CameraCurve(this.viewAngle);
        var targetCamera = this.vec3.fromValues(0,0,0); // Aim at the origin of the world coords
        var upCamera = this.vec3.fromValues(0,100,0); // Y-axis of world coords to be vertical
        var TlookAtCamera = glMatrix.mat4.create();
        glMatrix.mat4.lookAt(TlookAtCamera, eyeCamera, targetCamera, upCamera);

        var Tviewport = glMatrix.mat4.create();
        glMatrix.mat4.fromTranslation(Tviewport,[300,300,0]);  // Move the center of the
                                                    // "lookAt" transform (where
                                                    // the camera points) to the
                                                    // canvas coordinates (300,300)
        glMatrix.mat4.scale(Tviewport,Tviewport,[100,-100,1]); // Flip the Y-axis,
                                                    // scale everything by 100x

        var TprojectionCamera;
        var tVP_PROJ_VIEW_Camera;

        TprojectionCamera = glMatrix.mat4.create();
        glMatrix.mat4.ortho(TprojectionCamera, -100,100,-100,100,-1,1)
        tVP_PROJ_VIEW_Camera = glMatrix.mat4.create();
        glMatrix.mat4.multiply(tVP_PROJ_VIEW_Camera,Tviewport,TprojectionCamera);
        glMatrix.mat4.multiply(tVP_PROJ_VIEW_Camera,tVP_PROJ_VIEW_Camera,TlookAtCamera);

        
        //leg
        this.drawCube(tVP_PROJ_VIEW_Camera, 100.0, 0.2, 0.5, 0.1, -1.3, -0.5, 0.5, `rgb(185,90,15)`);
        
        //leg
        this.drawCube(tVP_PROJ_VIEW_Camera, 100.0, 0.2, 0.5, 0.1, -1.3, -0.5, -0.5, `rgb(185,90,15)`);

        //base
        this.drawCube(tVP_PROJ_VIEW_Camera, 100.0, 1.6, 0.2, 0.7, 0, 0, 0, `rgb(185,90,15)`);
    
        //leg
        this.drawCube(tVP_PROJ_VIEW_Camera, 100.0, 0.2, 2, 0.13, 1.1, -0.5, 0.8, `rgb(185,90,15)`);

        //leg
        this.drawCube(tVP_PROJ_VIEW_Camera, 100.0, 0.2, 2, 0.13, 1.1, -0.5, -0.8, `rgb(185,90,15)`);

        //stamp
        this.drawCube(tVP_PROJ_VIEW_Camera, 100.0, 0.4, 0.1, 0.4, 1.1, 0.9, -0, `rgb(160,160,160)`);
    
        //stamp plate
        this.drawCube(tVP_PROJ_VIEW_Camera, 100.0, 0.45, 0.1, 0.45, -0.95, 0.1, 0, `rgb(160,160,160)`);

        //press beam
        this.drawCube(tVP_PROJ_VIEW_Camera, 100.0, 0.2, 0.5, 0.2, 1.1, 1, -0, `rgb(160,160,160)`);

        //support
        this.drawCube(tVP_PROJ_VIEW_Camera, 100.0, 0.27, 0.3, 1.2, 1.1, 1.5, 0, `rgb(185,90,15)`);

        
        this.drawSidePlate(tVP_PROJ_VIEW_Camera,100.0);


        //this.drawUpVector(tVP_PROJ_VIEW_Camera,100.0);
    }

    update() {
        this.vt += 0.02;
        if(this.vt > 360) this.vt = 0;
        if(this.sliderControl) {
            this.viewAngle = this.sliderValue;
        } else {
            this.viewAngle = this.vt*0.02*Math.PI;

        }
    }
}



