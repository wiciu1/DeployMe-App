import { ChangeDetectorRef, Component, EventEmitter, inject, Output } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-filter',
  imports: [ReactiveFormsModule],
  templateUrl: './filter.component.html',
  styleUrl: './filter.component.scss'
})
export class FilterComponent {
  
  @Output() 
  filtersChanged = new EventEmitter<any>();

  filterForm: FormGroup;
  
  private cdr = inject(ChangeDetectorRef)

  constructor(private fb: FormBuilder) {
    this.filterForm = this.fb.group({
      location: [''],
      experience: [''],
      skill: ['']
    });
  }

  applyFilters() {
    const formValue = this.filterForm.value;
    const filters = {
      location: formValue.location ? formValue.location.split(',').map((l: string) => l.trim()) : [],
      experience: formValue.experience ? formValue.experience.split(',').map((e: string) => e.trim()) : [],
      skill: formValue.skill ? formValue.skill.split(',').map((s: string) => s.trim()) : [],
    };

    this.filtersChanged.emit(filters);
    this.cdr.detectChanges();
  }

  resetFilters() {
    this.filterForm.reset();
    this.filtersChanged.emit({
      location: [],
      experience: [],
      skill: [],
    });
  }
  

}
