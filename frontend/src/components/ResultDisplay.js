import React from 'react';
import { Paper, Typography, Box, LinearProgress, Chip } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';

const ResultDisplay = ({ result }) => {
  if (!result) return null;

  const { confidence, result: message } = result;
  const confidencePercent = confidence * 100;
  const isDeepfake = confidence >= 0.5;

  // Determine color based on confidence level
  let color;
  if (isDeepfake) {
    color = confidence >= 0.8 ? 'error' : 'warning';
  } else {
    color = confidence <= 0.2 ? 'success' : 'info';
  }

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom align="center">
        Analysis Result
      </Typography>
      
      <Box sx={{ textAlign: 'center', mb: 3 }}>
        <Chip
          icon={isDeepfake ? <ErrorIcon /> : <CheckCircleIcon />}
          label={isDeepfake ? 'Likely Deepfake' : 'Likely Authentic'}
          color={color}
          variant="filled"
          size="large"
          sx={{ fontSize: '1.1rem', py: 2.5, px: 1 }}
        />
      </Box>
      
      <Box sx={{ mb: 2 }}>
        <Typography variant="body1" component="div" gutterBottom>
          Confidence Score:
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Box sx={{ width: '100%', mr: 1 }}>
            <LinearProgress 
              variant="determinate" 
              value={confidencePercent} 
              color={color}
              sx={{ height: 10, borderRadius: 5 }}
            />
          </Box>
          <Box sx={{ minWidth: 35 }}>
            <Typography variant="body2" color="text.secondary">
              {confidencePercent.toFixed(1)}%
            </Typography>
          </Box>
        </Box>
      </Box>
      
      <Typography variant="body1" sx={{ mt: 2, fontStyle: 'italic' }}>
        {message}
      </Typography>
      
      <Box sx={{ mt: 3, textAlign: 'center' }}>
        <Typography variant="caption" color="text.secondary">
          Note: This is an automated analysis. Results may not be 100% accurate.
        </Typography>
      </Box>
    </Paper>
  );
};

export default ResultDisplay; 