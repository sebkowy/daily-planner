import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, CircularProgress } from '@mui/material';
import axios from 'axios';

const MonthlyCalendar = ({ year, month }) => {
  const [users, setUsers] = useState([]);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const usersResponse = await axios.get('/api/users/');
        setUsers(usersResponse.data);

        const startDate = new Date(year, month - 1, 1);
        const endDate = new Date(year, month, 0);
        const eventsResponse = await axios.get(`/api/calendar-events/?start=${startDate.toISOString().split('T')[0]}&end=${endDate.toISOString().split('T')[0]}`);
        setEvents(eventsResponse.data);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError("Failed to fetch data. Please try again.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [year, month]);

  const getDaysInMonth = (year, month) => new Date(year, month, 0).getDate();
  const daysInMonth = getDaysInMonth(year, month);

  const getEventForUserAndDay = (userId, day) => {
    return events.find(event => 
      new Date(event.start).getDate() === day && 
      event.userId === userId
    );
  };

  if (loading) return <CircularProgress />;
  if (error) return <Typography color="error">{error}</Typography>;

  return (
    <TableContainer component={Paper} style={{ maxHeight: '80vh' }}>
      <Table stickyHeader size="small">
        <TableHead>
          <TableRow>
            <TableCell style={{ minWidth: 100 }}>User</TableCell>
            {[...Array(daysInMonth)].map((_, index) => (
              <TableCell key={index} align="center" style={{ minWidth: 50 }}>{index + 1}</TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {users.map(user => (
            <TableRow key={user.id}>
              <TableCell>{user.first_name} {user.last_name}</TableCell>
              {[...Array(daysInMonth)].map((_, index) => {
                const event = getEventForUserAndDay(user.id, index + 1);
                return (
                  <TableCell key={index} align="center">
                    {event ? '✓' : ''}
                  </TableCell>
                );
              })}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default MonthlyCalendar;