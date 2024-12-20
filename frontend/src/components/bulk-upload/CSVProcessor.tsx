'use client'

import { useState, useEffect } from 'react'
import { Table } from '@/components/ui/table'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { toast } from '@/components/ui/use-toast'
import Papa from 'papaparse'

interface Order {
  id: string
  customerName: string
  address: string
  phoneNumber: string
  items: string
  notes?: string
}

interface CSVProcessorProps {
  data: string
  onProcessComplete: (orders: Order[]) => void
  onError: (error: string) => void
}

export function CSVProcessor({ data, onProcessComplete, onError }: CSVProcessorProps) {
  const [orders, setOrders] = useState<Order[]>([])
  const [validationErrors, setValidationErrors] = useState<string[]>([])

  useEffect(() => {
    const parseCSV = () => {
      const requiredHeaders = ['id', 'customerName', 'address', 'phoneNumber', 'items']
      const errors: string[] = []

      // Log raw data
      console.log('Raw CSV data:', data)

      Papa.parse(data, {
        header: true,
        skipEmptyLines: true,
        delimiter: ',', // Explicitly set delimiter
        quoteChar: '"', // Explicitly set quote character
        transformHeader: (header) => header.trim(),
        transform: (value) => value.trim(),
        step: (row, parser) => {
          console.log('Processing row:', row.data)
        },
        complete: (results) => {
          // Log all parse results
          console.log('Papa Parse Results:', {
            data: results.data,
            errors: results.errors,
            meta: results.meta
          })

          if (results.errors.length > 0) {
            console.error('Papa Parse Errors:', results.errors)
            onError('CSV parsing errors detected')
            return
          }

          if (!results.data || results.data.length === 0) {
            console.error('No data parsed from CSV')
            onError('No data could be parsed from the CSV file')
            return
          }

          // Validate headers
          const headers = Object.keys(results.data[0] || {})
          console.log('Detected headers:', headers)
          console.log('Required headers:', requiredHeaders)
          
          const missingHeaders = requiredHeaders.filter(h => !headers.includes(h))
          if (missingHeaders.length > 0) {
            console.error('Missing headers:', missingHeaders)
            onError(`Missing required headers: ${missingHeaders.join(', ')}`)
            return
          }

          // Validate and transform rows
          const parsedOrders: Order[] = []
          
          results.data.forEach((row: any, index: number) => {
            console.log(`Processing row ${index + 1}:`, row)
            
            // Validate required fields
            const missingFields = requiredHeaders.filter(field => !row[field])
            if (missingFields.length > 0) {
              const error = `Line ${index + 2}: Missing required fields: ${missingFields.join(', ')}`
              console.error(error)
              errors.push(error)
              return
            }

            const order = {
              id: row.id,
              customerName: row.customerName,
              address: row.address,
              phoneNumber: row.phoneNumber,
              items: row.items,
              notes: row.notes
            }
            console.log(`Parsed order ${index + 1}:`, order)
            parsedOrders.push(order)
          })

          console.log('Final parsed orders:', parsedOrders)
          console.log('Validation errors:', errors)

          setOrders(parsedOrders)
          setValidationErrors(errors)

          if (errors.length === 0 && parsedOrders.length > 0) {
            onProcessComplete(parsedOrders)
          } else if (errors.length > 0) {
            onError(`Found ${errors.length} validation errors`)
          }
        },
        error: (error) => {
          console.error('CSV Parse Error:', error)
          onError('Failed to parse CSV file')
        }
      })
    }

    parseCSV()
  }, [data, onProcessComplete, onError])

  return (
    <div className="space-y-4">
      {validationErrors.length > 0 && (
        <Card className="p-4 bg-destructive/10 text-destructive">
          <h3 className="font-semibold mb-2">Validation Errors</h3>
          <ul className="list-disc list-inside space-y-1">
            {validationErrors.map((error, index) => (
              <li key={index}>{error}</li>
            ))}
          </ul>
        </Card>
      )}

      {orders.length > 0 && (
        <div className="rounded-md border">
          <Table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Customer</th>
                <th>Address</th>
                <th>Phone</th>
                <th>Items</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td>{order.id}</td>
                  <td>{order.customerName}</td>
                  <td>{order.address}</td>
                  <td>{order.phoneNumber}</td>
                  <td>{order.items}</td>
                  <td>{order.notes}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      )}

      {orders.length > 0 && validationErrors.length === 0 && (
        <div className="flex justify-end">
          <Button
            onClick={() => {
              toast({
                title: "Processing Orders",
                description: `Processing ${orders.length} orders for route optimization...`,
              })
              onProcessComplete(orders)
            }}
          >
            Continue to Route Planning
          </Button>
        </div>
      )}
    </div>
  )
}
