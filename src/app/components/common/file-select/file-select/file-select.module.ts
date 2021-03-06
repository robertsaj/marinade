import { NgModule, ModuleWithProviders } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';

import { CovalentHighlightModule } from '@covalent/highlight';
import { CovalentMarkdownModule } from '@covalent/markdown';

import { TdContainerDirective } from '@components/common/file-select/container/container.directive';
import { TdFileSelectComponent } from '@components/common/file-select/file-select';

@NgModule({
  imports: [
    CommonModule,
    CovalentHighlightModule,
    CovalentMarkdownModule,
    MatIconModule,
    MatListModule,
    MatButtonModule,
  ],
  declarations: [
    TdFileSelectComponent,
    TdContainerDirective,
  ],
  exports: [
    TdFileSelectComponent,
  ],
})
export class CovalentFileSelectModule {
  static forRoot(): ModuleWithProviders {
    return {
      ngModule: CovalentFileSelectModule,
      providers: [ ],
    };
  }
}
