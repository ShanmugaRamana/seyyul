const express = require('express');
const router = express.Router();

// Landing page
router.get('/', (req, res) => {
    res.render('index', {
        title: 'Seyyul - Education Platform',
        mode: 'Offline/Local Mode'
    });
});

// Home/Dashboard page (protected by client-side check)
router.get('/home', (req, res) => {
    res.render('home');
});

module.exports = router;
