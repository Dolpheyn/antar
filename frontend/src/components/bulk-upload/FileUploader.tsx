import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileWarning } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface FileUploaderProps {
  onFileAccepted: (file: File) => Promise<void>
  maxSize?: number
  accept?: string[]
}

export function FileUploader({ 
  onFileAccepted, 
  maxSize = 5 * 1024 * 1024, // 5MB default
  accept = ['.csv']
}: FileUploaderProps) {
  const [uploadProgress, setUploadProgress] = useState(0)
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0]
    if (!file) return

    try {
      setError(null)
      setUploadProgress(0)
      
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return prev
          }
          return prev + 10
        })
      }, 200)

      await onFileAccepted(file)
      
      clearInterval(progressInterval)
      setUploadProgress(100)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to upload file')
      setUploadProgress(0)
    }
  }, [onFileAccepted])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    maxSize,
    accept: {
      'text/csv': accept,
    },
    multiple: false
  })

  return (
    <div className="w-full max-w-xl mx-auto">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-8 text-center cursor-pointer
          transition-colors duration-200 ease-in-out
          ${isDragActive 
            ? 'border-primary bg-primary/5' 
            : 'border-gray-300 hover:border-primary'
          }
        `}
      >
        <input {...getInputProps()} />
        <Upload className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-4 text-lg font-semibold">
          {isDragActive ? 'Drop your file here' : 'Upload your CSV file'}
        </h3>
        <p className="mt-2 text-sm text-gray-500">
          Drag and drop your file here, or click to select
        </p>
        <Button variant="outline" className="mt-4">
          Select File
        </Button>
      </div>

      {uploadProgress > 0 && (
        <div className="mt-4">
          <Progress value={uploadProgress} className="h-2" />
          <p className="text-sm text-gray-500 mt-2">
            {uploadProgress < 100 
              ? 'Uploading...' 
              : 'Upload complete!'
            }
          </p>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-destructive/10 rounded-lg flex items-center gap-2 text-destructive">
          <FileWarning className="h-5 w-5" />
          <p className="text-sm">{error}</p>
        </div>
      )}
    </div>
  )
}
