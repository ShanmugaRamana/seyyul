require('dotenv').config({ path: require('path').join(__dirname, '../../server/.env') });

const express = require('express');
const path = require('path');
const setupRoutes = require('./routes/routes');

const app = express();
const PORT = 3000;

// Set EJS as the templating engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Serve static files (css, js, images) from 'public' folder
app.use(express.static(path.join(__dirname, 'public')));

// Parse JSON and URL-encoded bodies
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Setup all routes
setupRoutes(app);

app.listen(PORT, () => {
    console.log(`Seyyul local frontend running at http://localhost:${PORT}`);
    console.log(`Google Client ID: ${process.env.GOOGLE_CLIENT_ID ? 'configured' : 'not set'}`);
});