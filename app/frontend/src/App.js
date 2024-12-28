import Layout from './components/Layout';
import { theme } from './components/theme';

import React, { useState } from 'react';
import { Button, Card, Container, Grid, TextField, Typography, ThemeProvider, IconButton, Fab } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import axios from 'axios';
import './App.css';

function App() {
  const [objective, setObjective] = useState('');
  const [result, setResult] = useState('');
  const [showResults, setShowResults] = useState(false);

  const handleRunScript = async () => {
    try {
      setShowResults(true); // This will trigger the UI to display the result next to the text box
      const response = await axios.post('http://localhost:5001/runscript', { objective });
      setResult(response.data);
    } catch (error) {
      console.error('Error running script:', error);
      setResult('Error running script');
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      handleRunScript();
    }
  };

  const handleReset = () => {
    setObjective('');
    setResult('');
    setShowResults(false);
  };

  return (
    <Layout>
      <ThemeProvider theme={theme}>
        <Container maxWidth="lg" sx={{ padding: '4% 0', textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom sx={{ mb: 6, color: theme.palette.text.secondary }}>
            <span style={{ fontFamily: 'Pacifico, cursive' }}>Taitris</span> - Influencer Marketing Automation
          </Typography>
        </Container>
        <Container maxWidth="lg" sx={{ padding: '0% 0', textAlign: 'left' }}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={showResults ? 4 : 12}>
              <Card variant="outlined" sx={{ p: 2, mx: 'auto', mb: 3, backgroundColor: theme.palette.background.paper, color: theme.palette.text.primary }}>
                <TextField
                  multiline
                  rows={4}
                  fullWidth
                  label="Describe your campaign"
                  variant="outlined"
                  value={objective}
                  onChange={(e) => setObjective(e.target.value)}
                  onKeyPress={handleKeyPress}
                  autoComplete="off"
                  InputProps={{
                    endAdornment: (
                      <IconButton onClick={handleRunScript}>
                        <SendIcon />
                      </IconButton>
                    ),
                  }}
                />
              </Card>
            </Grid>
            {showResults && (
              <Grid item xs={12} md={8}>
                <Card variant="outlined" sx={{ p: 2, mx: 'auto', mb: 3, backgroundColor: theme.palette.background.paper, color: theme.palette.text.primary, position: 'relative' }}>
                  <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>{result}</Typography>
                  {showResults && (
                    <Fab
                      onClick={handleReset}
                      sx={{
                        position: 'absolute',
                        bottom: 16,
                        right: 16,
                        backgroundColor: theme.palette.background.paper,
                        color: 'white',
                        border: '2px solid white',
                        '&:hover': {
                          backgroundColor: theme.palette.background.paper,
                        },
                      }}
                    >
                      Reset
                    </Fab>
                  )}
                </Card>
              </Grid>
            )}
          </Grid>
        </Container>
      </ThemeProvider>
    </Layout>
  );
}

export default App;