import React, { useState, useEffect } from 'react';
import { uploadMaterial, getMaterials } from '../api/materialApi';

const MaterialHubView = () => {
  const [materials, setMaterials] = useState([]);
  const [title, setTitle] = useState('');
  const [courseCode, setCourseCode] = useState('');
  const [fileType, setFileType] = useState('Note');
  const [file, setFile] = useState(null);
  
  
  const token = localStorage.getItem('token') || ''; 

  const fetchMaterials = async () => {
    try {
      const data = await getMaterials(token);
      setMaterials(data);
    } catch (error) {
      console.error("Failed to fetch materials:", error);
    }
  };

  useEffect(() => {
    fetchMaterials();
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please select a file");

    const formData = new FormData();
    formData.append('title', title);
    formData.append('course_code', courseCode);
    formData.append('file_type', fileType);
    formData.append('file', file);

    try {
      await uploadMaterial(token, formData);
      alert("Material uploaded successfully!");
      setTitle('');
      setCourseCode('');
      setFile(null);
      fetchMaterials(); 
    } catch (error) {
      alert(error.message);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Study Material Hub</h2>
      
      {/* Upload Form */}
      <form onSubmit={handleUpload} style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ccc' }}>
        <h3>Upload New Material</h3>
        <div>
          <input type="text" placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} required />
        </div>
        <div style={{ marginTop: '10px' }}>
          <input type="text" placeholder="Course Code (e.g., CSE470)" value={courseCode} onChange={e => setCourseCode(e.target.value)} required />
        </div>
        <div style={{ marginTop: '10px' }}>
          <select value={fileType} onChange={e => setFileType(e.target.value)}>
            <option value="Note">Note</option>
            <option value="Practice Exam">Practice Exam</option>
            <option value="Lecture Slide">Lecture Slide</option>
          </select>
        </div>
        <div style={{ marginTop: '10px' }}>
          <input type="file" onChange={e => setFile(e.target.files[0])} required />
        </div>
        <button type="submit" style={{ marginTop: '15px' }}>Upload Material</button>
      </form>

      {/* Materials List */}
      <h3>Available Materials</h3>
      <ul>
        {materials.map((mat) => (
          <li key={mat.material_id} style={{ marginBottom: '10px' }}>
            <strong>{mat.title}</strong> ({mat.course_code}) - {mat.file_type} 
            <br />
            <small>Version: {mat.version} | Uploaded: {new Date(mat.created_at).toLocaleDateString()}</small>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MaterialHubView;