'use client';

import { ChangeEvent } from 'react';
import { Input } from "@/app/table/components/Input";
import { Button } from "@/components/Button";
import { COURT_OPTIONS } from "@/app/constants/courtOptions";
import { MultiSelect } from './MultiSelect';

interface Side {
    Name?: string;
    Inn?: string;
    ExactMatch?: boolean;
  }

export interface Filters {
  CaseType?: string;
  Courts?: string[];
  DateFrom?: string;
  DateTo?: string;
  Sides?: Side[];
  Judges?: string[];
  CaseNumbers?: string[];
  WithVKSInstances?: boolean;
  Page?: number;
}

export default function Filter({
  filters,
  setFilters
}: {
  filters: Filters;
  setFilters: (filters: Filters) => void;
}) {

  const handleArrayChange = (
    e: ChangeEvent<HTMLInputElement>,
    field: keyof Filters
  ) => {
    setFilters({ ...filters, [field]: e.target.value });
  };

  const handleArrayBlur = (field: keyof Filters) => {
    const value = filters[field] as unknown as string;
    if (typeof value === 'string') {
      const values = value.split(',').map(v => v.trim()).filter(v => v);
      setFilters({ ...filters, [field]: values });
    }
  };

  const handleSideChange = (
    e: ChangeEvent<HTMLInputElement>,
    index: number,
    field: keyof Side
  ) => {
    const newSides = [...(filters.Sides || [])];
    const target = e.target;
    let value: string | number | boolean | undefined;
  
    if (field === 'Inn') {
      value = target.value || undefined;
    } else if (field === 'ExactMatch') {
      value = target.checked;
    } else {
      value = target.value || undefined;
    }
  
    newSides[index] = { ...newSides[index], [field]: value };
    setFilters({ ...filters, Sides: newSides });
  };

  const addSide = () => {
    setFilters({ ...filters, Sides: [...(filters.Sides || []), {}] });
  };

  const removeSide = (index: number) => {
    const newSides = [...(filters.Sides || [])];
    newSides.splice(index, 1);
    setFilters({ ...filters, Sides: newSides });
  };

  return (
    <div className="space-y-4 p-4 border rounded-lg bg-background shadow-sm">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Даты */}
        <div className="space-y-2">
          <label className="block text-sm font-medium">Период</label>
          <div className="flex gap-2">
            <Input
              type="date"
              value={filters.DateFrom || ''}
              onChange={e => setFilters({ ...filters, DateFrom: e.target.value })}
            />
            <Input
              type="date"
              value={filters.DateTo || ''}
              onChange={e => setFilters({ ...filters, DateTo: e.target.value })}
            />
          </div>
        </div>

        {/* Номера дел */}
        <div className="space-y-2">
          <label className="block text-sm font-medium">Номера дел (через запятую)</label>
          <Input
            value={Array.isArray(filters.CaseNumbers) ? filters.CaseNumbers.join(', ') : filters.CaseNumbers || ''}
            onChange={e => handleArrayChange(e, 'CaseNumbers')}
            onBlur={() => handleArrayBlur('CaseNumbers')}
          />
        </div>

        {/* Суды */}
        <div className=''>
          <div className="space-y-2">
            <label className="block text-sm font-medium">Суды</label>
            <MultiSelect
              value={filters.Courts || []}
              onChange={(courts) => setFilters({ ...filters, Courts: courts })}
              options={COURT_OPTIONS}
              placeholder="Выберите суд..."
            />
          </div>
        </div>

        {/* Судьи */}
        <div className="space-y-2">
          <label className="block text-sm font-medium">Судьи (через запятую)</label>
          <Input
            value={Array.isArray(filters.Judges) ? filters.Judges.join(', ') : filters.Judges || ''}
            onChange={e => handleArrayChange(e, 'Judges')}
            onBlur={() => handleArrayBlur('Judges')}
          />
        </div>

        {/* Тип дела */}
        <div className="space-y-2">
          <label className="block text-sm font-medium">Тип дела</label>
          <select
            name="caseType"
            value={filters.CaseType}
            onChange={e => setFilters({ ...filters, CaseType: e.target.value })}
            className="border rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="" className='text-foreground bg-background'>Не выбрано</option>
            <option value="administrative" className='text-foreground bg-background'>Административные</option>
            <option value="civil" className='text-foreground bg-background'>Гражданские</option>
            <option value="bankruptcy" className='text-foreground bg-background'>Банкротные</option>
          </select>
        </div>

        {/* ВКС */}
        <div className="space-y-2">
          <label className="block text-sm font-medium">С участием ВКС</label>
          <input
            type="checkbox"
            checked={filters.WithVKSInstances || false}
            onChange={e => setFilters({ ...filters, WithVKSInstances: e.target.checked })}
            className="border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {/* Пагинация */}
        <div className="space-y-2">
          <label className="block text-sm font-medium">Старница</label>
          <input 
            type="number"
            min='1'
            value={filters.Page || ''}
            onChange={e => setFilters({ ...filters, Page: parseInt(e.target.value) || 1 })}
            className='border rounded px-3 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500'></input>
        </div>
      </div>

      {/* Стороны */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-sm font-medium">Стороны дела</label>
          <Button onClick={addSide}>
            Добавить сторону
          </Button>
        </div>
        
        {filters.Sides?.map((side, index) => (
          <div key={index} className="flex gap-2 items-center">
            <Input
            placeholder="Наименование"
            value={side.Name || ''}
            onChange={e => handleSideChange(e, index, 'Name')}
            />
            <Input
            placeholder="ИНН"
            type="number"
            value={side.Inn ?? ''}
            onChange={e => handleSideChange(e, index, 'Inn')}
            />
            <Button
              onClick={() => removeSide(index)}
            >
              Удалить
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
}