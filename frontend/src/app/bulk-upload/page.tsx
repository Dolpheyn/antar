'use client'

import { useState } from 'react'
import { FileUploader } from '@/components/bulk-upload/FileUploader'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { CSVProcessor } from '@/components/bulk-upload/CSVProcessor'
import { toast } from '@/components/ui/use-toast'

export default function BulkUploadPage() {
  const [isProcessing, setIsProcessing] = useState(false)
  const [csvData, setCsvData] = useState<string | null>(null)

  const handleFileUpload = async (file: File) => {
    try {
      setIsProcessing(true)
      console.log('File received:', file)
      const text = await file.text()
      console.log('File content:', text)
      console.log('File content length:', text.length)
      setCsvData(text)
    } catch (error) {
      console.error('Error reading file:', error)
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to read the uploaded file",
      })
    } finally {
      setIsProcessing(false)
    }
  }

  const handleProcessComplete = (orders: any[]) => {
    toast({
      title: "Success",
      description: `Successfully processed ${orders.length} orders`,
    })
    // TODO: Implement route optimization
  }

  const handleProcessError = (error: string) => {
    toast({
      variant: "destructive",
      title: "Processing Error",
      description: error,
    })
  }

  return (
    <div className="container mx-auto py-8">
      <Card>
        <CardHeader>
          <CardTitle>Bulk Order Upload</CardTitle>
          <CardDescription>
            Upload your CSV file containing multiple delivery orders to process them in bulk
          </CardDescription>
        </CardHeader>
        <CardContent>
          <FileUploader 
            onFileAccepted={handleFileUpload}
            maxSize={10 * 1024 * 1024} // 10MB
          />
        </CardContent>
      </Card>

      {isProcessing && (
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Processing Orders</CardTitle>
            <CardDescription>
              Please wait while we process your orders and generate optimal routes
            </CardDescription>
          </CardHeader>
          <CardContent>
            {/* TODO: Add processing status and progress indicators */}
          </CardContent>
        </Card>
      )}

      {csvData && !isProcessing && (
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Order Preview</CardTitle>
            <CardDescription>
              Review your orders before proceeding to route optimization
            </CardDescription>
          </CardHeader>
          <CardContent>
            <CSVProcessor
              data={csvData}
              onProcessComplete={handleProcessComplete}
              onError={handleProcessError}
            />
          </CardContent>
        </Card>
      )}
    </div>
  )
}
