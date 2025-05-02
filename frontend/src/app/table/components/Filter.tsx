'use client';

import { ChangeEvent } from 'react';
import { Input } from "@/app/home/components/Input";
import { Button } from "@/app/home/components/Button";

interface Side {
    Name?: string;
    Type?: number;
    ExactMatch?: boolean;
  }

export interface Filters {
  Courts?: string[];
  DateFrom?: string;
  DateTo?: string;
  Sides?: Side[];
  Judges?: string[];
  CaseNumbers?: string[];
  WithVKSInstances?: boolean;
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
    const values = e.target.value.split(',').map(v => v.trim());
    setFilters({ ...filters, [field]: values.filter(v => v) });
  };

  const handleSideChange = (
    e: ChangeEvent<HTMLInputElement>,
    index: number,
    field: keyof Side
  ) => {
    const newSides = [...(filters.Sides || [])];
    const target = e.target;
    let value: string | number | boolean | undefined;
  
    if (field === 'Type') {
      value = target.value ? parseInt(target.value) : undefined;
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
            value={filters.CaseNumbers?.join(', ') || ''}
            onChange={e => handleArrayChange(e, 'CaseNumbers')}
          />
        </div>

        {/* Суды */}
        <div className="space-y-2">
          <label className="block text-sm font-medium">Суды (через запятую)</label>
          <Input
            value={filters.Courts?.join(', ') || ''}
            onChange={e => handleArrayChange(e, 'Courts')}
          />
        </div>

        {/* Судьи */}
        <div className="space-y-2">
          <label className="block text-sm font-medium">Судьи (через запятую)</label>
          <Input
            value={filters.Judges?.join(', ') || ''}
            onChange={e => handleArrayChange(e, 'Judges')}
          />
        </div>

        {/* ВКС */}
        <div className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={filters.WithVKSInstances || false}
            onChange={e => setFilters({ ...filters, WithVKSInstances: e.target.checked })}
            className="h-4 w-4"
          />
          <label className="text-sm font-medium">С участием ВКС</label>
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
            placeholder="Тип"
            type="number"
            value={side.Type ?? ''}
            onChange={e => handleSideChange(e, index, 'Type')}
            />
            <label className="flex items-center gap-2">
            <input
                type="checkbox"
                checked={side.ExactMatch || false}
                onChange={e => handleSideChange(e, index, 'ExactMatch')}
            />
            Точное совпадение
            </label>
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