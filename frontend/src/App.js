import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import About from './pages/About';
import { Container } from '@mui/material';

function App() {
  return (
    <Router>
      <Header />
      <Container component="main" sx={{ mt: 8, mb: 8, minHeight: '80vh' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </Container>
      <Footer />
    </Router>
  );
}

export default App; 