import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { 
  Box, 
  Typography, 
  Button, 
  Paper, 
  CircularProgress,
  Alert
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { uploadFile } from '../services/api';

const FileUpload = ({ onResult }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const onDrop = useCallback((acceptedFiles) => {
    setError('');
    const selectedFile = acceptedFiles[0];
    if (selectedFile) {
      const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'video/mp4'];
      if (!allowedTypes.includes(selectedFile.type)) {
        setError('Only JPG, PNG, and MP4 files are allowed');
        return;
      }
      setFile(selectedFile);
    }
  }, []);
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ 
    onDrop,
    accept: {
      'image/jpeg': [],
      'image/png': [],
      'image/jpg': [],
      'video/mp4': []
    },
    multiple: false
  });
  
  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const result = await uploadFile(file);
      onResult(result);
      setFile(null);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload file');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Typography variant="h5" gutterBottom align="center">
        Upload Image or Video
      </Typography>
      
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      
      <Box
        {...getRootProps()}
        sx={{
          border: '2px dashed #ccc',
          borderRadius: 2,
          p: 3,
          textAlign: 'center',
          cursor: 'pointer',
          mb: 2,
          backgroundColor: isDragActive ? 'rgba(63, 81, 181, 0.08)' : 'transparent',
          '&:hover': {
            backgroundColor: 'rgba(63, 81, 181, 0.04)'
          }
        }}
      >
        <input {...getInputProps()} />
        <CloudUploadIcon fontSize="large" color="primary" />
        <Typography variant="body1" sx={{ mt: 1 }}>
          {isDragActive
            ? 'Drop the file here'
            : 'Drag & drop a file here, or click to select'}
        </Typography>
        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
          Supported formats: JPG, PNG, MP4
        </Typography>
      </Box>
      
      {file && (
        <Box sx={{ mt: 2, mb: 2 }}>
          <Typography variant="body2">
            Selected file: {file.name}
          </Typography>
        </Box>
      )}
      
      <Box sx={{ display: 'flex', justifyContent: 'center' }}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleUpload}
          disabled={!file || loading}
          startIcon={loading ? <CircularProgress size={20} color="inherit" /> : null}
        >
          {loading ? 'Processing...' : 'Analyze'}
        </Button>
      </Box>
    </Paper>
  );
};

export default FileUpload; 