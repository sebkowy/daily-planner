import React, { useState, useEffect } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Checkbox, Typography, CircularProgress } from '@mui/material';
import axios from 'axios';

const DailyTable = ({ date }) => {
  const [users, setUsers] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [dailyPlans, setDailyPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const usersResponse = await axios.get('/api/users/');
        setUsers(usersResponse.data);

        const tasksResponse = await axios.get('/api/tasks/');
        setTasks(tasksResponse.data);

        const dailyPlanResponse = await axios.get(`/api/daily-plans/?date=${date}`);
        setDailyPlans(dailyPlanResponse.data);
      } catch (err) {
        console.error("Error fetching data:", err);
        setError("Failed to fetch data. Please try again.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [date]);

  const getTaskForUser = (userId, taskId) => {
    const userPlan = dailyPlans.find(plan => plan.user.id === userId);
    if (!userPlan) return null;
    return userPlan.tasks.find(task => task.task.id === taskId);
  };

  const handleTaskToggle = async (userId, taskId, isAssigned) => {
    try {
      let userPlan = dailyPlans.find(plan => plan.user.id === userId);
      
      if (!userPlan && !isAssigned) {
        // Create a new daily plan for the user if it doesn't exist
        const newPlanResponse = await axios.post('/api/daily-plans/', { user: userId, date });
        userPlan = newPlanResponse.data;
        setDailyPlans([...dailyPlans, userPlan]);
      }

      if (isAssigned) {
        // Remove task
        const taskToRemove = getTaskForUser(userId, taskId);
        await axios.delete(`/api/daily-plan-tasks/${taskToRemove.id}/`);
      } else if (userPlan) {
        // Assign task
        await axios.post('/api/daily-plan-tasks/', {
          daily_plan: userPlan.id,
          task: taskId,
          start_time: "09:00:00",  // Default start time
          end_time: "17:00:00"     // Default end time
        });
      }

      // Refresh data
      const dailyPlanResponse = await axios.get(`/api/daily-plans/?date=${date}`);
      setDailyPlans(dailyPlanResponse.data);
    } catch (err) {
      console.error("Error updating task assignment:", err);
      setError("Failed to update task assignment. Please try again.");
    }
  };

  if (loading) return <CircularProgress />;
  if (error) return <Typography color="error">{error}</Typography>;

  return (
    <TableContainer component={Paper}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>User</TableCell>
            {tasks.map(task => (
              <TableCell key={task.id}>{task.name}</TableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {users.map(user => (
            <TableRow key={user.id}>
              <TableCell>{user.first_name} {user.last_name}</TableCell>
              {tasks.map(task => {
                const dailyPlanTask = getTaskForUser(user.id, task.id);
                return (
                  <TableCell key={task.id}>
                    <Checkbox
                      checked={!!dailyPlanTask}
                      onChange={() => handleTaskToggle(user.id, task.id, !!dailyPlanTask)}
                    />
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

export default DailyTable;