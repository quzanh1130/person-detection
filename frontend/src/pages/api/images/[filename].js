import fetch from 'node-fetch';
import { PassThrough } from 'stream';

export const config = {
  api: {
    responseLimit: false,
  },
};

export default async function handler(req, res) {
  const { filename } = req.query;
  
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Construct backend URL using environment variable
    const apiUrl = process.env.BACKEND_API_URL || 'http://backend_api:8386/api/v1/detect';
    const baseUrl = apiUrl.split('/api/v1/detect')[0]; // Extract base URL
    const imageUrl = `${baseUrl}/api/v1/detect/images/${filename}`;
    
    console.log(`Proxying image request to: ${imageUrl}`);
    
    const response = await fetch(imageUrl);
    
    if (!response.ok) {
      throw new Error(`Failed to retrieve image: ${response.status} ${response.statusText}`);
    }

    // Copy content-type header from the backend response
    res.setHeader('Content-Type', response.headers.get('content-type'));
    
    // Stream the image data from backend to client
    const body = await response.buffer();
    res.send(body);
    
  } catch (error) {
    console.error('Error proxying image:', error);
    res.status(500).json({ error: 'Failed to retrieve image', details: error.message });
  }
}
