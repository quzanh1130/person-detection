import React, { useState } from "react";
import Head from "next/head";
import Link from "next/link";
import ImageUpload from "../components/ImageUpload";
import DetectionResult from "../components/DetectionResult";

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const apiUrl = "http://localhost:8386/api/v1/detect";

  const handleUpload = async (file) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      console.log("Uploading to API:", apiUrl);
      const response = await fetch(apiUrl, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server Error: ${response.status} - ${await response.text()}`);
      }

      const data = await response.json();

      // Ensure valid image path
      if (data?.image_path) {
        const filename = data.image_path.split("/").pop();
        data.image_path = `/api/images/${filename}`;
      }

      setResult(data);
    } catch (err) {
      console.error("Upload failed:", err);
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <Head>
        <title>Person Detection System</title>
        <meta name="description" content="Upload images to detect people" />
      </Head>

      <header className="mb-12 text-center">
        <h1 className="text-4xl font-bold mb-4">Person Detection System</h1>
        <p className="text-lg text-gray-600">Upload an image to detect and count people</p>
      </header>

      <main className="flex flex-col items-center">
        <div className="w-full max-w-2xl">
          <ImageUpload onUpload={handleUpload} loading={loading} />

          {error && (
            <div className="mt-6 p-4 bg-red-100 text-red-700 border border-red-400 rounded-md">
              ❌ {error}
            </div>
          )}

          {result && <DetectionResult result={result} />}
        </div>
      </main>

      <footer className="mt-12 text-center">
        <Link href="/history" className="text-blue-600 hover:text-blue-800 text-lg font-medium">
          View Detection History
        </Link>
      </footer>
    </div>
  );
}
