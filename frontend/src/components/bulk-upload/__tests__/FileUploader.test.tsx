import React from 'react'
import { test, expect, describe, beforeEach, mock } from 'bun:test'
import { render, screen, fireEvent } from '@testing-library/react'
import { FileUploader } from '../FileUploader'

// Mock react-dropzone
const mockUseDropzone = mock(() => ({
  getRootProps: () => ({
    onClick: mock(() => {}),
  }),
  getInputProps: () => ({
    onChange: mock(() => {}),
  }),
  isDragActive: false,
}))

// Mock the module
globalThis.require = mock(() => ({
  useDropzone: mockUseDropzone
}))

describe('FileUploader', () => {
  const mockOnFileAccepted = mock(() => Promise.resolve())
  const defaultProps = {
    onFileAccepted: mockOnFileAccepted,
    maxSize: 5 * 1024 * 1024,
    accept: ['.csv'],
  }

  beforeEach(() => {
    mockOnFileAccepted.mockReset()
    mockUseDropzone.mockReset()
  })

  test('renders upload area with correct text', () => {
    render(<FileUploader {...defaultProps} />)
    
    expect(screen.getByText('Upload your CSV file')).toBeDefined()
    expect(screen.getByText('Drag and drop your file here, or click to select')).toBeDefined()
    expect(screen.getByRole('button', { name: 'Select File' })).toBeDefined()
  })

  test('shows progress bar when uploading', async () => {
    render(<FileUploader {...defaultProps} />)
    
    // Simulate file upload
    const file = new File(['test content'], 'test.csv', { type: 'text/csv' })
    const input = screen.getByTestId('file-input')
    
    await fireEvent.change(input, { target: { files: [file] } })
    
    expect(screen.getByRole('progressbar')).toBeDefined()
    expect(screen.getByText('Uploading...')).toBeDefined()
  })

  test('shows error message when upload fails', async () => {
    mockOnFileAccepted.mockImplementation(() => Promise.reject(new Error('Upload failed')))
    
    render(<FileUploader {...defaultProps} />)
    
    const file = new File(['test content'], 'test.csv', { type: 'text/csv' })
    const input = screen.getByTestId('file-input')
    
    await fireEvent.change(input, { target: { files: [file] } })
    
    expect(screen.getByText('Failed to upload file')).toBeDefined()
  })

  test('shows complete status after successful upload', async () => {
    mockOnFileAccepted.mockImplementation(() => Promise.resolve())
    
    render(<FileUploader {...defaultProps} />)
    
    const file = new File(['test content'], 'test.csv', { type: 'text/csv' })
    const input = screen.getByTestId('file-input')
    
    await fireEvent.change(input, { target: { files: [file] } })
    
    expect(screen.getByText('Upload complete!')).toBeDefined()
  })

  test('changes style when file is dragged over', () => {
    const { container } = render(<FileUploader {...defaultProps} />)
    
    fireEvent.dragEnter(container.firstChild as Element)
    
    expect(container.firstChild).toHaveClass('border-primary')
  })
})
