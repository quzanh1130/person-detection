import React from 'react';

export default function DetectionResult({ result }) {
  if (!result) return null;

  return (
    <div className="mt-8 bg-white shadow-md rounded-lg overflow-hidden">
      <div className="p-4 border-b">
        <h2 className="text-2xl font-bold">Detection Results</h2>
      </div>
      
      <div className="p-4">
        <div className="mb-4">
          <p className="text-lg font-semibold">
            Number of people detected: <span className="text-blue-600">{result.people_count}</span>
          </p>
          <p className="text-sm text-gray-600">
            File: {result.original_filename}
          </p>
          <p className="text-sm text-gray-600">
            Processed on: {new Date(result.timestamp).toLocaleString()}
          </p>
        </div>
        
        <div className="mt-4">
          <h3 className="text-lg font-semibold mb-2">Visualized Result</h3>
          <div className="border rounded p-1">
            <img 
              src={`${process.env.NEXT_PUBLIC_API_URL}${result.result_image_url}`} 
              alt="Detection Result" 
              className="w-full h-auto rounded"
            />
          </div>
        </div>
      </div>
    </div>
  );
}