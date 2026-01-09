const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// Set EJS as the templating engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Serve static files (css, js, images) from a 'public' folder
app.use(express.static(path.join(__dirname, 'public')));

// Main Route
app.get('/', (req, res) => {
    res.render('index', {
        title: 'Seyyul - Education Platform',
        mode: 'Offline/Local Mode'
    });
});

app.listen(PORT, () => {
    console.log(`Seyyul local frontend running at http://localhost:${PORT}`);
});