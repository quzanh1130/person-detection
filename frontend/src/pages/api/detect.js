import { NextApiRequest, NextApiResponse } from 'next';
import fetch from 'node-fetch';
import FormData from 'form-data';
import { Readable } from 'stream';

// Helper function to convert readable stream to buffer
const streamToBuffer = async (stream) => {
  const chunks = [];
  return new Promise((resolve, reject) => {
    stream.on('data', (chunk) => chunks.push(chunk));
    stream.on('end', () => resolve(Buffer.concat(chunks)));
    stream.on('error', reject);
  });
};

export const config = {
  api: {
    bodyParser: false, // Disable the default body parser
    responseLimit: '50mb',
  },
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Get the internal API URL from server-side environment variable
    const apiUrl = process.env.BACKEND_API_URL || 'http://localhost:8386/api/v1/detect';
    
    // Parse the multipart form data
    const buffer = await streamToBuffer(req);
    
    // Create a new FormData object to send to the backend
    const formData = new FormData();
    formData.append('file', buffer, {
      filename: 'image.jpg', // Default filename
      contentType: req.headers['content-type'],
    });

    // Forward the request to the backend API
    const response = await fetch(apiUrl, {
      method: 'POST',
      body: formData,
      headers: {
        ...formData.getHeaders(),
      },
    });

    // Get the response data
    const data = await response.json();

    console.log('Response from backend:', data);

    // Return the response from the backend
    res.status(response.status).json(data);
  } catch (error) {
    console.error('Error in API proxy:', error);
    res.status(500).json({ error: 'Failed to process the request', details: error.message });
  }
}
