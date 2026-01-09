const express = require('express');
const router = express.Router();

// Signup page
router.get('/signup', (req, res) => {
    res.render('signup');
});

// Login page
router.get('/login', (req, res) => {
    res.render('login');
});

// Verify page
router.get('/verify', (req, res) => {
    res.render('verify');
});

module.exports = router;
