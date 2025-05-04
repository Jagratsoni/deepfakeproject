import React, { useState } from 'react';
import { Box, Typography, Container, Paper, Grid } from '@mui/material';
import FileUpload from '../components/FileUpload';
import ResultDisplay from '../components/ResultDisplay';

const Home = () => {
  const [result, setResult] = useState(null);

  const handleResult = (data) => {
    setResult(data);
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          Deepfake Detection
        </Typography>
        <Typography variant="h6" component="div" gutterBottom align="center">
          Upload an image or video to analyze for potential deepfake manipulation
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <FileUpload onResult={handleResult} />
        </Grid>
        
        {result && (
          <Grid item xs={12}>
            <ResultDisplay result={result} />
          </Grid>
        )}
        
        <Grid item xs={12}>
          <Paper elevation={2} sx={{ p: 3, backgroundColor: 'rgba(63, 81, 181, 0.04)' }}>
            <Typography variant="h6" gutterBottom>
              How it works
            </Typography>
            <Typography variant="body1" paragraph>
              Our deepfake detection system uses advanced AI and machine learning techniques to analyze visual media for signs of manipulation.
            </Typography>
            <Typography variant="body1">
              The system examines subtle inconsistencies in facial movements, lighting, and other details that are often undetectable to the human eye but reveal when content has been artificially generated or manipulated.
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Home; 