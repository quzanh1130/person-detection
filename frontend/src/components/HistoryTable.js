import React from 'react';

export default function HistoryTable({ 
  history, 
  loading, 
  page, 
  totalPages, 
  pageSize, 
  totalRecords,
  onPageChange, 
  onPageSizeChange 
}) {
  if (loading) {
    return (
      <div className="py-16 flex flex-col items-center justify-center">
        <div className="relative">
          <div className="h-16 w-16 rounded-full border-t-4 border-b-4 border-blue-500 animate-spin"></div>
        </div>
        <p className="mt-4 text-gray-600 font-medium">Loading results...</p>
      </div>
    );
  }

  if (!history.length) {
    return (
      <div className="py-16 flex flex-col items-center justify-center">
        <p className="mt-4 text-xl text-gray-600 font-medium">No detection records found</p>
        <p className="text-gray-500">Try adjusting your filters to see more results</p>
      </div>
    );
  }

  return (
    <div className="p-4">
      <div className="mb-6 flex flex-wrap justify-between items-center">
        <span className="text-gray-600 font-medium">
          Showing <span className="font-bold text-gray-800">{page * pageSize + 1}</span> to 
          <span className="font-bold text-gray-800">{Math.min((page + 1) * pageSize, totalRecords)}</span> of 
          <span className="font-bold text-gray-800">{totalRecords}</span> results
        </span>
        <div className="flex items-center bg-gray-50 px-3 py-1 rounded-md">
          <span className="mr-3 text-gray-600 font-medium">Items per page:</span>
          <select
            value={pageSize}
            onChange={onPageSizeChange}
            className="border border-gray-300 rounded-md py-1 px-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {[5, 10, 25, 50].map(size => (
              <option key={size} value={size}>{size}</option>
            ))}
          </select>
        </div>
      </div>
      
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white rounded-lg overflow-hidden">
          <thead className="bg-gray-100">
            <tr>
              {['ID', 'Date', 'Filename', 'People Count'].map(header => (
                <th key={header} className="py-3 px-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider border-b">
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {history.map(({ id, timestamp, original_filename, people_count }) => (
              <tr key={id} className="hover:bg-gray-50 transition-colors duration-150">
                <td className="py-3 px-4 text-sm font-medium text-gray-900">{id}</td>
                <td className="py-3 px-4 text-sm text-gray-600">{new Date(timestamp).toLocaleString()}</td>
                <td className="py-3 px-4 text-sm text-gray-600 truncate max-w-[200px]">{original_filename}</td>
                <td className="py-3 px-4 text-center">
                  <span className="px-3 py-1 text-sm font-semibold rounded-full bg-blue-100 text-blue-800">
                    {people_count}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="mt-6 flex flex-wrap justify-center sm:justify-between items-center">
        <nav className="inline-flex rounded-md shadow-sm">
          {[['First', 0], ['Previous', page - 1], ['Next', page + 1], ['Last', totalPages - 1]].map(([label, targetPage], index) => (
            <button
              key={label}
              onClick={() => onPageChange(targetPage)}
              disabled={targetPage < 0 || targetPage >= totalPages}
              className={`px-3 py-2 border text-sm font-medium transition-colors duration-150 rounded-${index === 0 ? 'l' : index === 3 ? 'r' : ''}-md ${
                targetPage < 0 || targetPage >= totalPages ? 'bg-gray-100 text-gray-400 cursor-not-allowed' :
                'bg-white text-gray-700 hover:bg-gray-50 focus:ring-2 focus:ring-blue-500'}
              `}
              aria-label={`${label} page`}
            >
              {label}
            </button>
          ))}
        </nav>
      </div>
    </div>
  );
}