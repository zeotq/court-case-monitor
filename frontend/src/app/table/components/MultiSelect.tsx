'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { Input } from "@/app/table/components/Input";

interface Option {
  label: string;
  value: string;
}

interface MultiSelectProps {
  value: string[];
  onChange: (value: string[]) => void;
  options: Option[];
  placeholder?: string;
}

export function MultiSelect({
  value = [],
  onChange,
  options,
  placeholder = "Выберите значение...",
}: MultiSelectProps) {
  const [inputValue, setInputValue] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const containerRef = useRef<HTMLDivElement>(null);

  const filteredOptions = options.filter(option =>
    option.label.toLowerCase().includes(inputValue.toLowerCase()) &&
    !value.includes(option.value)
  );

  const handleClickOutside = useCallback((event: MouseEvent) => {
    if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
      setIsOpen(false);
    }
  }, []);

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [handleClickOutside]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!isOpen) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setHighlightedIndex(prev => Math.min(prev + 1, filteredOptions.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setHighlightedIndex(prev => Math.max(prev - 1, 0));
        break;
      case 'Enter':
        e.preventDefault();
        if (filteredOptions[highlightedIndex]) {
          handleSelect(filteredOptions[highlightedIndex].value);
        }
        break;
      case 'Escape':
        e.preventDefault();
        setIsOpen(false);
        break;
    }
  };

  const handleSelect = (selectedValue: string) => {
    onChange([...value, selectedValue]);
    setInputValue('');
    setIsOpen(false);
    setHighlightedIndex(-1);
  };

  const removeItem = (val: string) => {
    onChange(value.filter(v => v !== val));
  };

  return (
    <div className="relative gap-2" ref={containerRef}>
      <div className="relative mb-2">
        <Input
          value={inputValue}
          onChange={(e) => {
            setInputValue(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          aria-haspopup="listbox"
        />
        <button 
          className="absolute right-2 top-3 transform rotate-180"
          onClick={() => setIsOpen(!isOpen)}
          aria-label={isOpen ? "Скрыть список" : "Показать список"}
        >
          ▲
        </button>
      </div>

      <div className="flex flex-wrap gap-2">
        {value.map(val => {
          const item = options.find(opt => opt.value === val);
          return (
            <div 
              key={val}
              className="bg-background border border-gray-300 px-2 py-1 rounded-md flex items-center text-sm"
            >
              <span>{item?.label || val}</span>
              <button 
                onClick={() => removeItem(val)}
                className="ml-2 text-gray-500 hover:text-gray-700"
                aria-label="Удалить"
              >
                ×
              </button>
            </div>
          );
        })}
      </div>
      
      {isOpen && (
        <div 
          role="listbox"
          className="absolute z-10 mt-1 w-full bg-background border border-gray-300 rounded-md shadow-lg max-h-60 overflow-auto"
        >
          {filteredOptions.map((option, index) => (
            <div
              key={option.value}
              role="option"
              aria-selected={highlightedIndex === index}
              className={`px-4 py-2 cursor-pointer ${
                highlightedIndex === index
                  ? 'bg-foreground text-background'
                  : 'hover:bg-background hover:text-foreground'
              } ${value.includes(option.value) ? 'bg-foreground' : ''}`}
              onClick={() => handleSelect(option.value)}
              onMouseEnter={() => setHighlightedIndex(index)}
            >
              {option.label}
            </div>
          ))}

          {filteredOptions.length === 0 && (
            <div className="px-4 py-2 text-gray-500 hover:bg-background">
              Ничего не найдено
            </div>
          )}
        </div>
      )}
    </div>
  );
}
