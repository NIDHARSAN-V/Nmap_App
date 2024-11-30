const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const axios = require('axios'); // Import axios for making HTTP requests

const app = express();
const port = 3000;

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Enable CORS
app.use(cors());


app.post('/tocommand', async (req, res) => {
    const { spokenText } = req.body; // Extract spokenText from the request body

    if (!spokenText) {
        return res.status(400).json({ error: 'No spokenText provided' });
    }

    console.log('Received spokenText:', spokenText);

    try {
        // Make a POST request to the Flask app
        const flaskResponse = await axios.post('http://localhost:5000/generate_command', {
            query: spokenText, // Send the spokenText as 'query'
        });

        // Extract the command from Flask response
        const { predicted_command } = flaskResponse.data;

        // Send the response back to the client
        res.json({ command: predicted_command });
    } catch (error) {
        console.error('Error communicating with Flask:', error.message);
        res.status(500).json({ error: 'Error processing the request' });
    }
});



app.post('/tonmap', async (req, res) => {
    console.log("Nmap server.js")
    const { nmapexe } = req.body; // Extract spokenText from the request body

    if (!nmapexe) {
        return res.status(400).json({ error: 'No Nmap provided' });
    }

    console.log('Received NmapText:', nmapexe);

    try {
        // Make a POST request to the Flask app
        const flaskResponse = await axios.post('http://localhost:5000/nmapdesc', {
            query: nmapexe, // Send the spokenText as 'query'
        });

        
        const { nmapdesc } = flaskResponse.data;

        console.log(nmapdesc)
        res.json({desc : nmapdesc });

    } catch (error) {
        console.error('Error communicating with Flask:', error.message);
        res.status(500).json({ error: 'Error processing the request' });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at ${port}`);
});
