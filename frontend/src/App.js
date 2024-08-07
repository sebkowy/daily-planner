import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Link, Routes, Navigate } from 'react-router-dom';
import { Button, Container, Box } from '@mui/material';
import MonthlyCalendar from './components/MonthlyCalendar';
import DailyTable from './components/DailyTable';
import Login from './components/Login';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';

function App() {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      setIsAuthenticated(true);
    }
  }, []);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };

  if (!isAuthenticated) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <Router>
      <Container>
        <Box my={4}>
          <Button component={Link} to="/" variant="contained" color="primary" style={{ marginRight: 10 }}>
            Monthly View
          </Button>
          <Button component={Link} to="/daily" variant="contained" color="secondary">
            Daily View
          </Button>
        </Box>

        <Routes>
          <Route 
            path="/" 
            element={
              <MonthlyCalendar 
                year={selectedDate.getFullYear()} 
                month={selectedDate.getMonth() + 1} 
              />
            } 
          />
          <Route 
            path="/daily" 
            element={
              <DailyTable 
                date={selectedDate.toISOString().split('T')[0]} 
              />
            } 
          />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;