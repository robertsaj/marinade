import { Component } from '@angular/core';
import {
  ARCHITECTURE1, ARCHITECTURE2, ARCHITECTURE3, ARCHITECTURE4, ARCHITECTURE5, ARCHITECTURE6, ARCHITECTURE7,
  ARCHITECTURE8, ARCHITECTURE9
} from './simulator.model';

@Component({
  selector: 'marinade-simulator',
  styleUrls: ['./simulator.component.sass'],
  templateUrl: './simulator.component.html',
})
export class SimulatorComponent {

  private static readonly DEFAULT_VIEWBOX_HEIGHT: number = 905;
  private static readonly DEFAULT_VIEWBOX_SCALE: number = 1;
  private static readonly DEFAULT_VIEWBOX_UPPER_LEFT_X: number = 0;
  private static readonly DEFAULT_VIEWBOX_UPPER_LEFT_Y: number = 0;
  private static readonly DEFAULT_VIEWBOX_WIDTH: number = 1600;

  private static readonly MAX_SCALE: number = 2.5;
  private static readonly MIN_SCALE: number = 1.0;

  private mouseStartX: number = -1;
  private mouseStartY: number = -1;
  private tracking: boolean = false;
  private viewBoxHeight: number = 905;
  private viewBoxUpperLeftX: number = 0;
  private viewBoxUpperLeftY: number = 0;
  private viewBoxWidth: number = 1600;

  public architecture: string = ARCHITECTURE1 + ARCHITECTURE2 + ARCHITECTURE3 + ARCHITECTURE4 + ARCHITECTURE5 +
                                ARCHITECTURE6 + ARCHITECTURE7 + ARCHITECTURE8 + ARCHITECTURE9;
  public scale: number = 1;
  public viewBox: string = '0 0 1600 905';

  private updateViewBox(): void {
    if (this.viewBoxUpperLeftX < -1200) {
      this.viewBoxUpperLeftX = -1200;
    }
    if (this.viewBoxUpperLeftX > 1200) {
      this.viewBoxUpperLeftX = 1200;
    }
    if (this.viewBoxUpperLeftY < -600) {
      this.viewBoxUpperLeftY = -600;
    }
    if (this.viewBoxUpperLeftY > 600) {
      this.viewBoxUpperLeftY = 600;
    }
    this.viewBox = this.viewBoxUpperLeftX + ' ' + this.viewBoxUpperLeftY + ' ' +
                   this.viewBoxWidth + ' ' + this.viewBoxHeight;
  }

  /**
   * Start tracking the mouse drag motion
   * @param {MouseEvent} event The MouseEvent that caused the click function to fire
   */
  public onClick(event: MouseEvent): void {
    // Note the original location of the cursor
    this.mouseStartX = event.x;
    this.mouseStartY = event.y;
    // Allow movements to move the canvas
    this.tracking = true;
  }

  /**
   * Pan the canvas based on the direction of the cursor movements
   * @param {MouseEvent} event The MouseEvent that caused the move function to fire
   */
  public onMove(event: MouseEvent): void {
    // If a click is being held
    if (this.tracking) {
      // Adjust the top left corner (origin point) based on the location deltas and the scale
      this.viewBoxUpperLeftX = this.viewBoxUpperLeftX - (event.x - this.mouseStartX) / this.scale;
      this.viewBoxUpperLeftY = this.viewBoxUpperLeftY - (event.y - this.mouseStartY) / this.scale;
      // Refresh the viewbox with the new properties
      this.updateViewBox();
      // Create a new reference point for tracking
      this.mouseStartX = event.x;
      this.mouseStartY = event.y;
    }
  }

  /**
   * Stop tracking the mouse drag motion
   */
  public onRelease(): void {
    // Reset the mouse tracking locations
    this.mouseStartX = 0;
    this.mouseStartY = 0;
    // Prevent movements from moving the canvas
    this.tracking = false;
  }

  public onWheel(event: WheelEvent): void {
    let oldScale: number = this.scale;
    this.scale += event.deltaY / 400;
    if (this.scale < SimulatorComponent.MIN_SCALE) {
      this.scale = SimulatorComponent.MIN_SCALE;
    }
    if (this.scale > SimulatorComponent.MAX_SCALE) {
      this.scale = SimulatorComponent.MAX_SCALE;
    }
    if (event.deltaY < 0) {
      this.viewBoxUpperLeftX = (this.viewBoxWidth + this.viewBoxUpperLeftX) / oldScale * (this.scale - oldScale);
      this.viewBoxUpperLeftY = (this.viewBoxHeight + this.viewBoxUpperLeftY) / oldScale * (this.scale - oldScale);
    } else {
      this.viewBoxUpperLeftX += (event.layerX - this.viewBoxUpperLeftX) / oldScale * (this.scale - oldScale);
      this.viewBoxUpperLeftY += (event.layerY - this.viewBoxUpperLeftY) / oldScale * (this.scale - oldScale);
    }
    this.viewBoxHeight = SimulatorComponent.DEFAULT_VIEWBOX_HEIGHT / this.scale;
    this.viewBoxWidth = SimulatorComponent.DEFAULT_VIEWBOX_WIDTH / this.scale;
    this.updateViewBox();
  }

  /**
   * Reset the viewBox to the default view (scale 1.0; top-left corner at 0, 0)
   */
  public reset(): void {
    // Reset the height and width properties to remove any zooming
    this.viewBoxHeight = SimulatorComponent.DEFAULT_VIEWBOX_HEIGHT;
    this.viewBoxWidth = SimulatorComponent.DEFAULT_VIEWBOX_WIDTH;
    // Reset the upper left corner to remove any panning
    this.viewBoxUpperLeftX = SimulatorComponent.DEFAULT_VIEWBOX_UPPER_LEFT_X;
    this.viewBoxUpperLeftY = SimulatorComponent.DEFAULT_VIEWBOX_UPPER_LEFT_Y;
    // Reset the scale used for calculations
    this.scale = SimulatorComponent.DEFAULT_VIEWBOX_SCALE;
    // Refresh the viewBox with the new properties
    this.updateViewBox();
  }

}
