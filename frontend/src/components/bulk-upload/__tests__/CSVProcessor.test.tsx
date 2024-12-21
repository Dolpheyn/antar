import React from 'react'
import { test, expect, describe, beforeEach, mock } from 'bun:test'
import { render, screen } from '@testing-library/react'
import { CSVProcessor } from '../CSVProcessor'

// Mock Papa Parse
const mockParse = mock((data: string, config: any) => {
  if (data.includes('valid')) {
    config.complete({
      data: [
        {
          id: 'ORD001',
          customerName: 'John Smith',
          address: '123 Main St',
          phoneNumber: '+1234567890',
          items: '2x Laptop',
          notes: 'Handle with care',
        },
      ],
      errors: [],
    })
  } else {
    config.error(new Error('Failed to parse CSV'))
  }
})

// Mock the module
globalThis.require = mock(() => ({
  parse: mockParse
}))

describe('CSVProcessor', () => {
  const mockOnProcessComplete = mock(() => {})
  const mockOnError = mock(() => {})
  const defaultProps = {
    onProcessComplete: mockOnProcessComplete,
    onError: mockOnError,
  }

  beforeEach(() => {
    mockOnProcessComplete.mockReset()
    mockOnError.mockReset()
    mockParse.mockReset()
  })

  test('processes valid CSV data correctly', async () => {
    const validCSV = 'id,customerName,address,phoneNumber,items,notes\nORD001,John Smith,123 Main St,+1234567890,2x Laptop,Handle with care'
    
    render(<CSVProcessor data={validCSV} {...defaultProps} />)
    
    expect(mockOnProcessComplete).toHaveBeenCalledWith([
      {
        id: 'ORD001',
        customerName: 'John Smith',
        address: '123 Main St',
        phoneNumber: '+1234567890',
        items: '2x Laptop',
        notes: 'Handle with care',
      },
    ])
    
    expect(screen.getByText('ORD001')).toBeDefined()
    expect(screen.getByText('John Smith')).toBeDefined()
    expect(screen.getByText('123 Main St')).toBeDefined()
  })

  test('shows validation errors for missing required fields', async () => {
    const invalidCSV = 'id,customerName\nORD001,John Smith'
    
    render(<CSVProcessor data={invalidCSV} {...defaultProps} />)
    
    expect(screen.getByText(/Missing required fields/)).toBeDefined()
    expect(mockOnError).toHaveBeenCalled()
  })

  test('handles CSV parsing errors', async () => {
    const invalidCSV = 'invalid,csv,data'
    
    render(<CSVProcessor data={invalidCSV} {...defaultProps} />)
    
    expect(mockOnError).toHaveBeenCalledWith('Failed to parse CSV file')
  })

  test('shows the "Continue to Route Planning" button after successful processing', async () => {
    const validCSV = 'id,customerName,address,phoneNumber,items,notes\nORD001,John Smith,123 Main St,+1234567890,2x Laptop,Handle with care'
    
    render(<CSVProcessor data={validCSV} {...defaultProps} />)
    
    expect(screen.getByText('Continue to Route Planning')).toBeDefined()
  })

  test('does not show the continue button when there are validation errors', async () => {
    const invalidCSV = 'id,customerName\nORD001,John Smith'
    
    render(<CSVProcessor data={invalidCSV} {...defaultProps} />)
    
    expect(() => screen.getByText('Continue to Route Planning')).toThrow()
  })
})
