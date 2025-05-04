import React from 'react';
import { Box, Typography, Container, Paper, Grid, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';

const About = () => {
  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom align="center">
          About This Project
        </Typography>
      </Box>

      <Grid container spacing={4}>
        <Grid item xs={12}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Our Mission
            </Typography>
            <Typography variant="body1" paragraph>
              As deepfake technology becomes increasingly sophisticated, the ability to distinguish between real and manipulated media is more important than ever. Our mission is to provide accessible tools that help verify the authenticity of digital content.
            </Typography>
            <Typography variant="body1">
              This project combines advanced computer vision and deep learning techniques to identify potential signs of manipulation in images and videos, particularly in facial content.
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h5" gutterBottom>
              Technology
            </Typography>
            <List>
              {[
                'Deep Convolutional Neural Networks for image analysis',
                'Temporal analysis for detecting inconsistencies in videos',
                'Facial landmark detection and tracking',
                'State-of-the-art pretrained models (Xception, EfficientNet)',
                'Transfer learning and fine-tuning on large datasets'
              ].map((item, idx) => (
                <ListItem key={idx} disableGutters>
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    <CheckCircleOutlineIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText primary={item} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3, height: '100%' }}>
            <Typography variant="h5" gutterBottom>
              Limitations
            </Typography>
            <Typography variant="body1" paragraph>
              While our technology is constantly improving, no deepfake detection system is perfect. Some limitations include:
            </Typography>
            <List>
              {[
                'New manipulation techniques may not be detected',
                'Low-resolution or compressed images can reduce accuracy',
                'Lighting conditions and camera artifacts can affect results',
                'False positives can occur with certain editing techniques',
                'Model effectiveness varies across different types of deepfakes'
              ].map((item, idx) => (
                <ListItem key={idx} disableGutters>
                  <ListItemIcon sx={{ minWidth: 40 }}>
                    <CheckCircleOutlineIcon color="primary" />
                  </ListItemIcon>
                  <ListItemText primary={item} />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default About; 