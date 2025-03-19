import React, { useState, useEffect, useCallback } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import HistoryTable from '../components/HistoryTable';

export default function History() {
  const [history, setHistory] = useState([]);
  const [filteredHistory, setFilteredHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [totalRecords, setTotalRecords] = useState(0);
  const [pageSize, setPageSize] = useState(10);
  const [search, setSearch] = useState('');
  const [filters, setFilters] = useState({
    minPeople: '',
    maxPeople: '',
    dateFrom: '',
    dateTo: '',
  });

  const fetchHistory = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        skip: page * pageSize,
        limit: pageSize,
      });

      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key.replace(/([A-Z])/g, '_$1').toLowerCase(), value);
      });

      const [historyRes, countRes] = await Promise.all([
        fetch(`http://localhost:8386/api/v1/history?${params}`),
        fetch(`http://localhost:8386/api/v1/history/count?${params}`)
      ]);

      if (!historyRes.ok || !countRes.ok) throw new Error('Failed to fetch data from server.');

      const historyData = await historyRes.json();
      const countData = await countRes.json();

      setHistory(historyData);
      setFilteredHistory(historyData); // Hiển thị ban đầu
      setTotalRecords(countData.count);
      setTotalPages(Math.ceil(countData.count / pageSize));
    } catch (err) {
      setError(err.message || 'Failed to load history. Please try again.');
    } finally {
      setLoading(false);
    }
  }, [page, pageSize, filters]);

  useEffect(() => {
    fetchHistory();
  }, [page, pageSize, filters]);

  // Hàm xử lý tìm kiếm
  const searchHistory = (query) => {
    if (!query) {
      setFilteredHistory(history); // Nếu không có từ khóa, hiển thị danh sách gốc
      return;
    }

    const lowerQuery = query.toLowerCase();
    const filtered = history.filter(item => 
      item.original_filename?.toLowerCase().includes(lowerQuery)
    );

    setFilteredHistory(filtered);
  };

  // Xử lý tìm kiếm khi người dùng nhập
  const handleSearch = (e) => {
    const value = e.target.value;
    setSearch(value);
    searchHistory(value); // Lọc trực tiếp
  };

  return (
    <div className="container mx-auto px-6 py-10 max-w-7xl">
      <Head>
        <title>Detection History | Person Detection System</title>
      </Head>

      <header className="mb-8">
        <h1 className="text-4xl font-bold mb-6 text-gray-800 border-b-2 pb-3">Detection History</h1>
        <Link href="/" className="text-blue-600 hover:text-blue-800 font-medium flex items-center transition-all">
          &larr; Back to Upload
        </Link>
      </header>

      {/* Filters Section */}
      <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 mb-8">
        <h2 className="text-xl font-semibold mb-4 text-gray-700">Filters</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { name: 'minPeople', type: 'number', placeholder: 'Min People' },
            { name: 'maxPeople', type: 'number', placeholder: 'Max People' },
            { name: 'dateFrom', type: 'date', placeholder: 'From' },
            { name: 'dateTo', type: 'date', placeholder: 'To' },
          ].map(({ name, type, placeholder }) => (
            <div key={name} className="flex flex-col">
              <label className="block text-sm font-medium text-gray-700">{name.replace(/([A-Z])/g, ' $1')}</label>
              <input
                type={type}
                name={name}
                value={filters[name]}
                onChange={(e) => setFilters((prev) => ({ ...prev, [name]: e.target.value }))}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                placeholder={placeholder}
              />
            </div>
          ))}
        </div>
      </div>

      {/* Search Input */}
      <div className="mb-4">
        <input
          type="text"
          name="search"
          value={search}
          onChange={handleSearch}
          className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
          placeholder="Search file name..."
        />
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-8 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded-md shadow-sm">
          <p>{error}</p>
        </div>
      )}

      {/* Table Section */}
      <div className="table-container">
        <HistoryTable
          history={filteredHistory} // Dùng danh sách đã lọc
          loading={loading}
          page={page}
          totalPages={totalPages}
          pageSize={pageSize}
          totalRecords={totalRecords}
          onPageChange={setPage}
          onPageSizeChange={(e) => setPageSize(Number(e.target.value))}
        />
      </div>
    </div>
  );
}
